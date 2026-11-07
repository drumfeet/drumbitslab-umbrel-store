# Private runtime configuration release pins

Published images verified on 2026-11-07. Catalog preparation does not deploy these releases. All three images support Linux AMD64 only and permit anonymous pulls.

| App | Version | Source commit | Publication |
| --- | --- | --- | --- |
| Pricewatch | `0.1.43` | `2c0741e549a64a8338e049b6ded177cdf9ab5f7d` | [Passed](https://github.com/drumfeet/pricewatch/actions/runs/42396199308) |
| Atlas Almanac Collector | `0.5.3` | `67a6d5fb6940f864cabc45b4d8db19aa822f45c1` | [Passed](https://github.com/drumfeet/atlas-almanac-collector/actions/runs/42396203320) |
| Visual Status Checker | `0.1.21` | `b6cbcd2ffd4ff7f603ff508df008cc832c865553` | [Passed](https://github.com/drumfeet/visualstatuscheck/actions/runs/42396206304) |

## New image pins

```text
ghcr.io/drumfeet/pricewatch:0.1.43@sha256:33b665dfe884226b22ab6f9aee851720682e32ddd3da98021ff99640811afb3f
ghcr.io/drumfeet/atlas-almanac-collector:0.5.3@sha256:5a4d86b5a1558ac38dd5b1b58035994d4433386f9099c4745a58458c78f52e59
ghcr.io/drumfeet/visual-status-checker:0.1.21@sha256:eb66b958a168320ffd9ee8f7654e0ffd857f8893498d0c3b7c588b72b4e49f89
```

## Previous image pins

Keep these available for a rehearsed recovery procedure. Do not overwrite current data with an older backup while an app is running.

```text
ghcr.io/drumfeet/pricewatch:0.1.42@sha256:ce3635875fb1acdeb274f2cd03a40990d8af6f6bd521d12893fb854e9abc365e
ghcr.io/drumfeet/atlas-almanac-collector:0.5.2@sha256:ea8b3c56ea08e8a11a10cf1bc84f31820e036c58e48f8e9018bd193c56817a5e
ghcr.io/drumfeet/visual-status-checker:0.1.20@sha256:aa620b4547bdf1a536b70a22bbf8a1d1a9921a9f4f63c3416a39801ca9262043
```

The publication workflows supplied each image digest. Independent anonymous registry verification checked manifest/config and layer integrity, the AMD64 platform, every native image layer and attached provenance metadata. All copied application source files matched the reviewed release commits. Final privacy checks found no unresolved private-preset, runtime-data or credential findings. Public cryptographic self-test fixtures were distinguished by exact fingerprints and library path.

Complete the [private runtime configuration migration](../private-runtime-config-migration.md) before updating an existing installation. Exported presets, credentials, backups, diagnostic logs and private migration receipts are not part of this public release record.
