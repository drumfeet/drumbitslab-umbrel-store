# drumbitsLab

This is the owner-controlled Umbrel Community App Store for drumbitsLab apps. Its apps use public, digest-pinned GitHub Container Registry images. The images are public so umbrelOS can pull them without GitHub credentials.

Add `https://github.com/drumfeet/drumbitslab-umbrel-store` in umbrelOS under **Community App Stores**. Updates are discovered from this repository and are applied from Umbrel's app update interface.

## Adding an app

Add each app in its own top-level directory. Every app needs an `umbrel-app.yml` manifest and a `docker-compose.yml` file that references its own public, digest-pinned image for its declared architectures. The active catalog contains Atlas Almanac Collector and T3 Code. Both currently support Linux AMD64 only. Keep app IDs stable after installation so Umbrel can continue to identify and update existing apps.

Never publish a mutable tag without its sha256 digest. Do not place promo codes, Discord webhooks, access tokens, `.env` files, screenshots, or `/data` contents in the image or this store repository. Runtime configuration stays in the app's mounted `/data` directory.

## Private runtime configuration releases

The historical private runtime releases, Pricewatch 0.1.43, Atlas Almanac Collector 0.5.3 and Visual Status Checker 0.1.21, introduced private preset files. Historical installations need their preserved configuration staged before updating. Fresh installations start empty. The [migration plan](docs/private-runtime-config-migration.md) describes backup, rehearsal, settings preservation and rollback. Personal exports and runtime files stay outside this public repository.

The images are already published. Preparing a catalog PR does not merge the changes or update an installed app. See the [verified release pins](docs/releases/2026-11-07-private-runtime.md) for source commits, workflow evidence and immutable images.

## Browser maintenance releases

The [November 16 browser maintenance release pins](docs/releases/2026-11-16-browser-maintenance.md) preserve Pricewatch 0.1.44 and Visual Status Checker 0.1.22, their successful source release workflows and verified AMD64 images. These are historical records for the retired apps. Existing installations that have not completed private runtime preset migration still need that migration before any separately reviewed update.

## Retired apps

Pricewatch and Visual Status Checker are retired and are no longer offered in this catalog. Their final image pins, release records and complete historical package snapshots are preserved in [the retired-app record](docs/retired-apps.md). Catalog removal does not uninstall an existing app or delete its data, backups or registry images.

## Public-store safeguards

### T3 Code package update PRs

`Check published T3 package updates` runs Mondays at 08:47 UTC (09:47 Madrid in winter, 10:47 in summer), or on manual dispatch after a release. It checks anonymous GHCR access, manifest/config digests, AMD64 compatibility and source/version/revision labels, then prepares one review PR for `drumfeet-t3code` when a newer stable package tag exists. The T3 source release pipeline publishes tagged images only after container checks and the image audit pass. Runtime nightly tags are not catalog package versions. Existing open bot PRs are preserved. New PRs get an explicit read-only validation dispatch because token-generated pushes do not trigger normal push workflows.

Manually reviewed release-candidate catalog PRs may use a published prerelease pin. The updater still discovers stable package tags only; after a manual RC it can select the matching final release or a later stable package. It does not automatically select newer RC tags. See the [T3 0.1.2-rc.1 release record](docs/releases/2026-11-15-t3-0.1.2-rc.1.md) for its verified image and separate runtime-activation requirements.

No automatic approval, merge, or Umbrel installation is enabled. Review the source release and store PR, merge it through the existing review policy, and install using Umbrel's Update button. The catalog workflow has no Umbrel credentials or private-source access; it only reads the published public image and writes this store's PR branch. Failures appear in GitHub Actions. The temporary token needs repository contents, PR creation, and workflow dispatch permissions.

`main` is protected: store changes require a pull request, one approval, and a successful **Validate public catalog** check. The check rejects tracked `.env` files plus runtime directories such as `data/`, `local-data/`, `artifacts/`, and `screenshots/`. GitHub secret scanning and push protection provide an additional safeguard, but maintainers must still review every release diff before merging.

Run `./scripts/verify-public-catalog.sh` and `python3 -B -m unittest discover -s tests -p 'test_*.py' -v` to check the catalog and its guard locally. The tests use disposable Git indexes and require only Python 3 and Git. Fixtures force-stage synthetic files and bound Git discovery to their temporary root, so global ignore rules and ancestor checkouts cannot change the results. They cover allowed sources, blocked runtime files, filenames containing spaces or newlines, and Git failures. The guard refuses publication if it cannot list tracked files.
