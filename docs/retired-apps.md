# Retired apps

Retirement of Pricewatch and Visual Status Checker was proposed on 18 November 2026 because the owner no longer uses them and their source repositories are archived. This record preserves their release identities and package history. The retirement PR removes their top-level app directories; they stop being offered after that change is reviewed and merged.

This catalog change does not delete registry images, Git tags, source history, installed-app data or backups. It does not uninstall or stop an existing installation. Neither app was installed on the owner's Umbrel device during the retirement review. Other installations require their own retirement and data-retention decision; do not treat catalog removal as an uninstall operation.

## Final catalog packages

| App | Stable app ID | Last catalog version | Source | Historical package |
| --- | --- | --- | --- | --- |
| Pricewatch | `drumfeet-pricewatch` | `0.1.44` | [Archived repository](https://github.com/drumfeet/pricewatch) | [Complete package snapshot](https://github.com/drumfeet/drumbitslab-umbrel-store/tree/c4b81f2cb2c07cfa16cf6279b75f819c15795205/drumfeet-pricewatch) |
| Visual Status Checker | `drumfeet-visual-status-checker` | `0.1.22` | [Archived repository](https://github.com/drumfeet/visualstatuscheck) | [Complete package snapshot](https://github.com/drumfeet/drumbitslab-umbrel-store/tree/c4b81f2cb2c07cfa16cf6279b75f819c15795205/drumfeet-visual-status-checker) |

The pinned snapshots retain the original manifests, Compose files, hooks, AppArmor/seccomp policies, licenses and static assets. Visual Status Checker's [release metadata](https://github.com/drumfeet/drumbitslab-umbrel-store/blob/c4b81f2cb2c07cfa16cf6279b75f819c15795205/drumfeet-visual-status-checker/release.json) remains available at that immutable commit. No app ID was reassigned.

```text
ghcr.io/drumfeet/pricewatch:0.1.44@sha256:a6abc6ed7cfc3beace3b3b7d63aaf9012a1f88263ea293d5499ab1301c438dd5
ghcr.io/drumfeet/visual-status-checker:0.1.22@sha256:63db052137d6423e17b30fc5c70f55efbeacaaa5f45f27239d3a7481f671f8e0
```

These are the final catalog references, not instructions to install unsupported apps. No registry image, package, digest or tag is removed by the retirement PR. The [November 16 release record](releases/2026-11-16-browser-maintenance.md) retains the source commits, publication/test workflows and previous recovery pins. The [November 7 release record](releases/2026-11-07-private-runtime.md) retains earlier releases and image identities. The [private runtime migration guide](private-runtime-config-migration.md) remains for historical installations and recovery planning. None of these documents substitutes for a current private data backup or a rehearsed restoration.

## Visual Status Checker release record

| Version | Image published | Source commit | Published image digest | Architecture |
| --- | --- | --- | --- | --- |
| `0.1.22` | 2026-11-16 | [`db04226`](https://github.com/drumfeet/visualstatuscheck/commit/db04226da02b0fe2ec8f80d4765f9cc3cd8bf574) | `sha256:63db052137d6423e17b30fc5c70f55efbeacaaa5f45f27239d3a7481f671f8e0` | `linux/amd64` |
| `0.1.21` | 2026-11-07 | [`b6cbcd2`](https://github.com/drumfeet/visualstatuscheck/commit/b6cbcd2ffd4ff7f603ff508df008cc832c865553) | `sha256:eb66b958a168320ffd9ee8f7654e0ffd857f8893498d0c3b7c588b72b4e49f89` | `linux/amd64` |
| `0.1.19` | 2026-10-29 | [`e461b03`](https://github.com/drumfeet/visualstatuscheck/commit/e461b03c42b36121aec2c7141a0dfb68c51596ff) | `sha256:9d3561f720c0cdc923d116b3be8e5254bb507e315188921701eca7ff9b261c3b` | `linux/amd64` |

Historical `0.1.19` verification. Tag: [`v0.1.19`](https://github.com/drumfeet/visualstatuscheck/tree/v0.1.19). The [AMD64 build and startup check](https://github.com/drumfeet/visualstatuscheck/actions/runs/40874431380) and [image publication](https://github.com/drumfeet/visualstatuscheck/actions/runs/40875400616) passed. Anonymous registry access, the published digest, and the AMD64-only image platform were verified. No Visual Status Checker app was installed on the owner's Umbrel device at release time, so no installed-app smoke test was performed.

## Historical Pricewatch overview

Pricewatch tracks supported Klook packages and Google Flights searches, saves price history and schedules, and can send Telegram alerts for new lows. Its provider structure supports adding more sources. New monitors stay paused until started. Google Flights remains experimental and pauses on verification or consent blocks.

The app uses port 3217 and persists its database and private Telegram settings under its own data volume. Back up that directory with the app stopped. Its Chromium process uses the bundled Playwright seccomp profile with browser sandboxing enabled. Umbrel renders `seccomp.json.template` into the app directory so profile updates follow its supported package-update workflow. The source repository is private; this catalog contains only installation metadata and static assets.
