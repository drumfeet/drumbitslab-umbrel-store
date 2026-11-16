# Browser maintenance release pins

Pricewatch 0.1.44 and Visual Status Checker 0.1.22 were published and verified on November 16, 2026. Both images support Linux AMD64 only and permit anonymous registry access. This catalog PR does not merge the changes, migrate private configuration or update an installed app. Collector and Hermes are unchanged.

| App | Source tag | Source commit | Successful release workflow |
| --- | --- | --- | --- |
| Pricewatch 0.1.44 | `v0.1.44` | `4bfcfd8ca81122f6e2946b3406f9b78e24a5ed0a` | [43814711061](https://github.com/drumfeet/pricewatch/actions/runs/43814711061) |
| Visual Status Checker 0.1.22 | `v0.1.22` | `db04226da02b0fe2ec8f80d4765f9cc3cd8bf574` | [43814721144](https://github.com/drumfeet/visualstatuscheck/actions/runs/43814721144) |

## Verified image pins

```text
ghcr.io/drumfeet/pricewatch:0.1.44@sha256:a6abc6ed7cfc3beace3b3b7d63aaf9012a1f88263ea293d5499ab1301c438dd5
ghcr.io/drumfeet/visual-status-checker:0.1.22@sha256:63db052137d6423e17b30fc5c70f55efbeacaaa5f45f27239d3a7481f671f8e0
```

Both release workflows built and tested their AMD64 candidate once, passed their HIGH/CRITICAL vulnerability gates and verified immutable artifact handoff before publishing that tested image without rebuilding. Pricewatch passed 480 built-image tests with one intentional skip, including sandboxed browser, private viewer, API and restart-persistence checks. Visual Status Checker passed all 51 source tests and all four browser tests, including its protected API/viewer, adequate non-root Chrome sandbox and password persistence.

Independent anonymous registry reads verified matching tag/digest manifest bytes, their SHA-256 and registry digest headers, configuration digests, filesystem layer identities, Linux AMD64 platform and source/version labels against the release receipts. Those checks were repeated before preparing this catalog change. No runtime data or credentials are part of this record.

The catalog preserves both app IDs, AMD64 declarations, ports, environment, data mounts, AppArmor profiles, seccomp policies and startup hooks. The profiles and hooks match the source packages used by the release tests. Only manifest versions/release notes and Compose image pins change app packaging. Visual Status Checker's release metadata and this documentation record the new verified release.

## Existing installation prerequisite

These releases retain private runtime preset files. Preserve any existing private file and path override. An installation that has not completed the [private runtime configuration migration](../private-runtime-config-migration.md) needs its presets exported and restored before updating. Pricewatch uses private monitor presets; Visual Status Checker uses private show presets and frame origins. Fresh installations can remain empty. Preparing this PR does not perform or establish a live migration, backup or rollback rehearsal.

## Previous catalog pins

Keep these identities available for a separately authorized, rehearsed recovery. Do not run an older image against active data or restore individual database files into a running app.

```text
ghcr.io/drumfeet/pricewatch:0.1.43@sha256:33b665dfe884226b22ab6f9aee851720682e32ddd3da98021ff99640811afb3f
ghcr.io/drumfeet/visual-status-checker:0.1.21@sha256:eb66b958a168320ffd9ee8f7654e0ffd857f8893498d0c3b7c588b72b4e49f89
```

Merge, private migration and installation require separate owner authorization. Any later installation must use Umbrel's supported update interface and verify retained state. No live provider check, notification, merge or deployment was performed for this catalog preparation.
