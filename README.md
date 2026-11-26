# drumbitsLab

This is the owner-controlled Umbrel Community App Store for drumbitsLab apps. Its apps use public, digest-pinned GitHub Container Registry images. The images are public so umbrelOS can pull them without GitHub credentials.

Add `https://github.com/drumfeet/drumbitslab-umbrel-store` in umbrelOS under **Community App Stores**. Updates are discovered from this repository and are applied from Umbrel's app update interface.

## Adding an app

Add each app in its own top-level directory. Every app needs an `umbrel-app.yml` manifest and a `docker-compose.yml` file that references its own public, digest-pinned image for its declared architectures. The active catalog offers Atlas Almanac Collector for Linux AMD64. Keep app IDs stable after installation so Umbrel can continue to identify and update existing apps.

Never publish a mutable tag without its sha256 digest. Do not place promo codes, Discord webhooks, access tokens, `.env` files, screenshots, or `/data` contents in the image or this store repository. Runtime configuration stays in the app's mounted `/data` directory.

## Private runtime configuration releases

The historical private runtime releases, Pricewatch 0.1.43, Atlas Almanac Collector 0.5.3 and Visual Status Checker 0.1.21, introduced private preset files. Historical installations need their preserved configuration staged before updating. Fresh installations start empty. The [migration plan](docs/private-runtime-config-migration.md) describes backup, rehearsal, settings preservation and rollback. Personal exports and runtime files stay outside this public repository.

The images are already published. Preparing a catalog PR does not merge the changes or update an installed app. See the [verified release pins](docs/releases/2026-11-07-private-runtime.md) for source commits, workflow evidence and immutable images.

## Browser maintenance releases

The [November 16 browser maintenance release pins](docs/releases/2026-11-16-browser-maintenance.md) preserve Pricewatch 0.1.44 and Visual Status Checker 0.1.22, their successful source release workflows and verified AMD64 images. These are historical records for the retired apps. Existing installations that have not completed private runtime preset migration still need that migration before any separately reviewed update.

## Retired apps

Pricewatch, Visual Status Checker and T3 Code Nightly are retired. Their final image pins, release records and complete historical package snapshots are preserved in [the retired-app record](docs/retired-apps.md). Manage any existing installations and their data through Umbrel separately.

## Public-store safeguards

`main` is protected: store changes require a pull request, one approval, and a successful **Validate public catalog** check. The check rejects tracked `.env` files plus runtime directories such as `data/`, `local-data/`, `artifacts/`, and `screenshots/`. GitHub secret scanning and push protection provide an additional safeguard, but maintainers must still review every release diff before merging.

Run the same checks locally before opening a catalog PR.

```sh
./scripts/verify-public-catalog.sh
python3 -m venv ~/.venvs/drumbitslab-catalog
. ~/.venvs/drumbitslab-catalog/bin/activate
python -m pip install -r tests/requirements.txt
python -B -m unittest discover -s tests -p 'test_*.py' -v
```

The publication guard tests use disposable Git indexes. Fixtures force-stage synthetic files and bound Git discovery to their temporary root, so global ignore rules and ancestor checkouts cannot change the results. They cover allowed sources, blocked runtime files, filenames containing spaces or newlines, and Git failures. The guard refuses publication if it cannot list tracked files.

The package tests use PyYAML to read the actual catalog. They check the store identity, app IDs and release metadata, immutable service image references, and the matching Atlas web and data-initialization images. Release verification still requires checking the published digest and supported architectures in the registry.
