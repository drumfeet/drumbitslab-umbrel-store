# drumbitsLab

This is the owner-controlled Umbrel Community App Store for drumbitsLab apps. It publishes Visual Status Checker and Pricewatch from public, digest-pinned GitHub Container Registry images. The images are public so umbrelOS can pull them without GitHub credentials.

Add `https://github.com/drumfeet/drumbitslab-umbrel-store` in umbrelOS under **Community App Stores**. Updates are discovered from this repository and are applied from Umbrel's app update interface.

## Adding an app

Add each app in its own top-level directory. Every app needs an `umbrel-app.yml` manifest and a `docker-compose.yml` file that references its own public, digest-pinned multi-architecture image. Keep app IDs stable after installation so Umbrel can continue to identify and update existing apps.

## Releasing Visual Status Checker

1. Update the release version and notes in `drumfeet/visualstatuscheck`, validate it, and push its matching `v<version>` tag.
2. Wait for the source repository's image-publishing workflow to succeed, then download its `image-digest` artifact.
3. In `drumfeet-visual-status-checker/`, update `umbrel-app.yml` with the same version and release notes. Update `docker-compose.yml` to the exact `ghcr.io/drumfeet/visual-status-checker:<version>@<digest>` image reference.
4. Commit and push this store repository. umbrelOS will discover the update; apply it from the installed app's update interface.

Never publish a mutable tag without its sha256 digest. Do not place promo codes, Discord webhooks, access tokens, `.env` files, screenshots, or `/data` contents in the image or this store repository. Runtime configuration stays in the app's mounted `/data` directory.

## Visual Status Checker release record

| Version | Image published | Source commit | Published image digest | Architecture |
| --- | --- | --- | --- | --- |
| `0.1.19` | 2026-10-29 | [`e461b03`](https://github.com/drumfeet/visualstatuscheck/commit/e461b03c42b36121aec2c7141a0dfb68c51596ff) | `sha256:9d3561f720c0cdc923d116b3be8e5254bb507e315188921701eca7ff9b261c3b` | `linux/amd64` |

Tag: [`v0.1.19`](https://github.com/drumfeet/visualstatuscheck/tree/v0.1.19). The [AMD64 build and startup check](https://github.com/drumfeet/visualstatuscheck/actions/runs/40874431380) and [image publication](https://github.com/drumfeet/visualstatuscheck/actions/runs/40875400616) passed. Anonymous registry access, the published digest, and the AMD64-only image platform were verified. No Visual Status Checker app was installed on the owner's Umbrel device at release time, so no installed-app smoke test was performed.

## Public-store safeguards

`main` is protected: store changes require a pull request, one approval, and a successful **Validate public catalog** check. The check rejects tracked `.env` files plus runtime directories such as `data/`, `local-data/`, `artifacts/`, and `screenshots/`. GitHub secret scanning and push protection provide an additional safeguard, but maintainers must still review every release diff before merging.

Run `./scripts/verify-public-catalog.sh` and `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` to check the catalog and its guard locally. The tests use disposable Git indexes and require only Python 3 and Git. Fixtures force-stage synthetic files and bound Git discovery to their temporary root, so global ignore rules and ancestor checkouts cannot change the results. They cover allowed sources, blocked runtime files, filenames containing spaces or newlines, and Git failures. The guard refuses publication if it cannot list tracked files.

## Pricewatch

Pricewatch tracks supported Klook packages and Google Flights searches, saves price history and schedules, and can send Telegram alerts for new lows. Its provider structure supports adding more sources. New monitors stay paused until started. Google Flights remains experimental and pauses on verification or consent blocks.

The app uses port 3217 and persists its database and private Telegram settings under its own data volume. Back up that directory with the app stopped. Its Chromium process uses the bundled Playwright seccomp profile with browser sandboxing enabled. Umbrel renders `seccomp.json.template` into the app directory so profile updates follow its supported package-update workflow. The source repository is private; this catalog contains only installation metadata and static assets.
