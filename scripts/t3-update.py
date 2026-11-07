"""Prepare a T3 catalog PR from an anonymously pullable, published image."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

REPO = 'drumfeet/drumbitslab-umbrel-store'
IMAGE = 'drumfeet/t3code-umbrel'
SOURCE = 'https://github.com/drumfeet/t3code-umbrel'
VERSION = re.compile(r'\d+\.\d+\.\d+')
MEDIA = ','.join(['application/vnd.oci.image.index.v1+json', 'application/vnd.docker.distribution.manifest.list.v2+json', 'application/vnd.oci.image.manifest.v1+json', 'application/vnd.docker.distribution.manifest.v2+json'])


def version_key(value):
    if not VERSION.fullmatch(value):
        raise ValueError('Invalid package version')
    return tuple(map(int, value.split('.')))


def latest_tag(tags, current):
    candidates = [tag for tag in tags if VERSION.fullmatch(tag) and version_key(tag) > version_key(current)]
    return max(candidates, key=version_key) if candidates else None


def image_metadata(version, manifest_bytes, image_manifest, config):
    labels = config.get('config', {}).get('Labels', {})
    revision = labels.get('org.opencontainers.image.revision', '')
    if (config.get('os'), config.get('architecture')) != ('linux', 'amd64'):
        raise ValueError('Expected linux/amd64')
    if labels.get('org.opencontainers.image.source') != SOURCE or labels.get('org.opencontainers.image.version') != version or not re.fullmatch('[a-f0-9]{40}', revision):
        raise ValueError('Image release labels do not match the trusted source/version')
    if not image_manifest.get('layers'):
        raise ValueError('Missing image layers')
    return {
        'version': version, 'sourceCommit': revision, 'sourceTag': 'v' + version,
        'image': f'ghcr.io/{IMAGE}:{version}@sha256:' + hashlib.sha256(manifest_bytes).hexdigest(),
        'platforms': ['linux/amd64'], 'sourceRepository': SOURCE,
    }


def registry_request(path, token=None):
    headers = {'Accept': MEDIA}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    with urllib.request.urlopen(urllib.request.Request(path, headers=headers), timeout=30) as response:
        if response.headers.get('Link'):
            raise ValueError('Registry pagination requires review before expanding the bound')
        return response.read()


def discover(current):
    token = json.loads(registry_request(f'https://ghcr.io/token?service=ghcr.io&scope=repository:{IMAGE}:pull'))['token']
    def get(path):
        return registry_request(f'https://ghcr.io/v2/{IMAGE}/{path}', token)
    version = latest_tag(json.loads(get('tags/list?n=1000'))['tags'], current)
    if version is None:
        return None
    raw = get('manifests/' + version)
    manifest = json.loads(raw)
    if 'manifests' in manifest:
        candidates = [item for item in manifest['manifests'] if item.get('platform') == {'os': 'linux', 'architecture': 'amd64'}]
        other_platforms = [item['platform'] for item in manifest['manifests'] if item.get('platform', {}).get('architecture') not in ('amd64', 'unknown')]
        if len(candidates) != 1 or other_platforms:
            raise ValueError('Unexpected image architecture set')
        child = get('manifests/' + candidates[0]['digest'])
        if 'sha256:' + hashlib.sha256(child).hexdigest() != candidates[0]['digest']:
            raise ValueError('Child manifest digest mismatch')
        manifest = json.loads(child)
    config_raw = get('blobs/' + manifest['config']['digest'])
    if 'sha256:' + hashlib.sha256(config_raw).hexdigest() != manifest['config']['digest']:
        raise ValueError('Image configuration digest mismatch')
    return image_metadata(version, raw, manifest, json.loads(config_raw))


def update(root, metadata):
    folder = root / 'drumfeet-t3code'
    manifest = folder / 'umbrel-app.yml'
    text, count = re.subn(r'^version: "[^"\n]+"$', f'version: "{metadata["version"]}"', manifest.read_text(), flags=re.M)
    if count != 1:
        raise ValueError('Expected one manifest version')
    text = re.sub(r'releaseNotes: >-\n(?:[ \t]+.*\n)+', 'releaseNotes: >-\n  Container maintenance refresh with validated nightly compatibility and persistence.\n  Updates the package without resetting your projects or T3 Connect preference.\n', text)
    manifest.write_text(text)
    compose = folder / 'docker-compose.yml'
    text, count = re.subn(r'^    image: ghcr\.io/drumfeet/t3code-umbrel:.*$', '    image: ' + metadata['image'], compose.read_text(), flags=re.M)
    if count != 1:
        raise ValueError('Expected one T3 image')
    compose.write_text(text)
    (folder / 'release.json').write_text(json.dumps(metadata, indent=2) + '\n')


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True).strip()


def main():
    if os.environ.get('GITHUB_REPOSITORY') != REPO or os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise ValueError('Must run from trusted store main')
    branch = 'automation/t3code-package-update'
    existing = json.loads(gh('pr', 'list', '--repo', REPO, '--head', branch, '--state', 'open', '--json', 'url'))
    if existing:
        print('Existing catalog PR awaits review:', existing[0]['url'])
        return
    current = json.loads(Path('drumfeet-t3code/release.json').read_text())['version']
    metadata = discover(current)
    if metadata is None:
        print('No newer published T3 package; catalog is current.')
        return
    subprocess.run(['git', 'switch', '-c', branch], check=True)
    update(Path('.'), metadata)
    subprocess.run(['git', 'add', 'drumfeet-t3code'], check=True)
    subprocess.run(['bash', 'scripts/verify-public-catalog.sh'], check=True)
    subprocess.run(['python3', '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], check=True)
    subprocess.run(['git', '-c', 'user.name=github-actions[bot]', '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com', 'commit', '-m', 'Update published T3 Code package'], check=True)
    subprocess.run(['git', 'push', '--force-with-lease', 'origin', f'HEAD:refs/heads/{branch}'], check=True)
    body = Path('/tmp/t3-catalog-pr.md')
    body.write_text(f'Updates T3 Code packaging to `{metadata["version"]}` from the published AMD64 image. Anonymous manifest/config access, digest integrity, platform, and release labels were checked.\n\nImage: `{metadata["image"]}`\nSource commit: `{metadata["sourceCommit"]}`\n\nReview the source release and catalog validation before merging. After merge, install manually through Umbrel. This workflow never contacts your Umbrel or changes its T3 Connect setting.\n')
    print(gh('pr', 'create', '--repo', REPO, '--base', 'main', '--head', branch, '--title', f'Update T3 Code package to {metadata["version"]}', '--body-file', str(body), '--assignee', 'drumfeet'))
    gh('workflow', 'run', 'validate-public-catalog.yml', '--repo', REPO, '--ref', branch)


if __name__ == '__main__':
    main()
