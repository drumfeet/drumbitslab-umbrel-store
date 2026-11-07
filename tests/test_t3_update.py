import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('t3_update', Path(__file__).parents[1] / 'scripts/t3-update.py')
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


class T3UpdateTests(unittest.TestCase):
    def test_only_new_stable_packages_are_candidates(self):
        self.assertEqual(update.latest_tag(['0.1.9', '0.1.10', '0.1.11-nightly', 'latest', 'untrusted'], '0.1.0'), '0.1.10')
        self.assertIsNone(update.latest_tag(['0.1.0', '0.0.9'], '0.1.0'))

    def test_rejects_untrusted_source_mismatched_version_and_wrong_architecture(self):
        config = {'os': 'linux', 'architecture': 'amd64', 'config': {'Labels': {
            'org.opencontainers.image.source': update.SOURCE,
            'org.opencontainers.image.version': '0.1.1',
            'org.opencontainers.image.revision': 'a' * 40,
        }}}
        metadata = update.image_metadata('0.1.1', b'manifest', {'layers': [1]}, config)
        self.assertRegex(metadata['image'], r'^ghcr.io/drumfeet/t3code-umbrel:0.1.1@sha256:[a-f0-9]{64}$')
        for field, value in [('org.opencontainers.image.source', 'https://evil.test'), ('org.opencontainers.image.version', '0.2.0'), ('org.opencontainers.image.revision', 'not-a-commit')]:
            changed = json.loads(json.dumps(config))
            changed['config']['Labels'][field] = value
            with self.assertRaises(ValueError):
                update.image_metadata('0.1.1', b'manifest', {'layers': [1]}, changed)
        config['architecture'] = 'arm64'
        with self.assertRaises(ValueError):
            update.image_metadata('0.1.1', b'manifest', {'layers': [1]}, config)

    def test_catalog_update_preserves_app_identity_and_volume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / 'drumfeet-t3code'
            folder.mkdir()
            (folder / 'umbrel-app.yml').write_text('id: drumfeet-t3code\nversion: "0.1.0"\nreleaseNotes: >-\n  Old notes.\ndependencies: []\n')
            (folder / 'docker-compose.yml').write_text('services:\n  server:\n    image: ghcr.io/drumfeet/t3code-umbrel:0.1.0@sha256:old\n    volumes:\n      - ${APP_DATA_DIR}/data:/data\n')
            metadata = {'version': '0.1.1', 'image': 'ghcr.io/drumfeet/t3code-umbrel:0.1.1@sha256:' + 'a' * 64}
            update.update(root, metadata)
            manifest = (folder / 'umbrel-app.yml').read_text()
            self.assertIn('id: drumfeet-t3code', manifest)
            self.assertIn('version: "0.1.1"', manifest)
            self.assertIn('dependencies: []', manifest)
            self.assertIn('${APP_DATA_DIR}/data:/data', (folder / 'docker-compose.yml').read_text())
