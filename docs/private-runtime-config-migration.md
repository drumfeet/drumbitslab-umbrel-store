# Private runtime configuration migration

This plan covers Pricewatch 0.1.43, Atlas Almanac Collector 0.5.3 and Visual Status Checker 0.1.21. Their personal presets are supplied through private files in persistent app storage. Publishing images or preparing a catalog PR does not apply this migration. Keep the PR unmerged until the owner authorizes the maintenance and catalog release.

## Configuration locations

Each app keeps its existing `${APP_DATA_DIR}/data:/data` mount. Paths below are inside its own container, not shared between apps.

| App | Default private file | Optional existing path override | Presets moved out of the image |
| --- | --- | --- | --- |
| Pricewatch | `/data/private-presets.json` | `PRICEWATCH_PRESETS_FILE` | Monitor templates, flight routes and searches, provider preset values |
| Atlas Almanac Collector | `/data/private-watchlist.json` | `ATLAS_WATCHLIST_FILE` | Watchlist symbols and planning levels |
| Visual Status Checker | `/data/private-presets.json` | `VSC_PRESETS_FILE` | Show IDs, event URL, sections, labels and frame origins |

Use the matching release's loader to validate the format. Pricewatch and VSC use format version 1; Collector uses format version 2. Preserve an existing owner-edited private file and any explicit path override. Do not substitute legacy defaults for current edits or create an empty file merely to make a populated installation start.

These files supplement saved application data. They do not replace databases, schedules, thresholds, passwords, credentials, notification settings, custom booking links, receipts, archives or browser profiles. A missing private file beside existing data stops loading instead of silently resetting the installation. A genuinely fresh installation can remain empty. Collector accepts an intentional empty watchlist and continues collection and refresh while skipping watchlist alerts. Empty VSC installations disable monitoring and booking-link editing.

## Prepare privately before updating

1. Record the current version, exact image pin, enabled schedules and monitors, stable IDs, intervals, alert preferences, thresholds and representative history. Keep the baseline private. Keep the previous image pins in the [release record](releases/2026-11-07-private-runtime.md) available.
2. Preserve and validate any existing private config first. Otherwise obtain the matching migration exporter from the app maintainer and export the currently installed old release's built-in presets. Run an exporter offline against that exact old source or image, without starting its app entrypoint. Record the export checksum and refuse any overwrite. The new images cannot export presets that have already been removed from them.
3. Keep exports, tools containing private values and migration receipts outside this repository, public issues, release assets and Docker build contexts. Use private storage with restricted access. The owner-maintained private migration bundle contains the prepared payloads and staging tools; it is not distributed here. Those preset exports are not a backup of live settings or credentials.

## Authorized maintenance window

Perform this for one app at a time after the owner authorizes execution. This document does not authorize a production update.

1. Choose an idle boundary. For Collector, drain active publication and reconcile uncertain receipts before stopping it. A timeout does not prove that an external write failed. Preserve its schedule and source settings and keep a single ingestion owner.
2. Stop the app through Umbrel and wait for completion. Take a consistent private backup of its complete mounted app data, preserving numeric ownership, permissions and symlinks. Keep Pricewatch's database and any WAL/SHM files together. Include its credentials, preferences, profiles and evidence; Collector's settings, archives, credentials and receipts plus its separate `tunnel` directory; and VSC's authentication, saved links, webhook settings, history and artifacts. Do not copy an active database as a standalone file.
3. Rehearse on a disposable copy of that stopped-app backup with providers, schedulers and notification transports disabled. Do not start an app with live credentials merely to test migration. Validate the private file with the candidate loader. The private staging helper checks the payload checksum, creates only the fixed target filename, uses mode `0600` and the existing data directory's UID/GID, and refuses existing files and symlinks. Its default is a check without writes; applying requires an explicit stopped-and-backed-up acknowledgement. Preserve an existing file rather than overwriting it.
4. Compare pre-existing file hashes, ownership, modes, symlink targets and stable application state on the copy. Verify retained monitor or show IDs, schedules, intervals, thresholds, alert preferences, history, credential references and receipts. Rehearse the previous compatible reader against the copy as well. Adding the validated private file should not reset saved state. Do not lower schema versions, edit receipts, reset browser profiles or trigger retention cleanup as a workaround.
5. Only after that rehearsal passes, stage the validated private file in the stopped production app's persistent data directory under the authorized migration. Preserve the existing app-data owner and mode `0600`. Keep any configured path override. Do not replace the data volume or overwrite an existing private file. Preserve the original backup separately.
6. Obtain the catalog's required validation and review before a separately authorized merge. Preserve app IDs, ports, volumes, environment and security options. Collector's `data_init` and `web` services must use the same new app image; its Cloudflared image, token-file mount and tunnel configuration stay unchanged. Apply the offered update through Umbrel's supported update interface. Do not edit installed Compose files manually.
7. Verify startup and retained settings through read-only checks. Confirm the expected private presets loaded; an unexpectedly empty owner configuration is not a successful migration. Existing enabled work may resume according to normal restart behavior. If the drain temporarily paused a setting, restore only its recorded prior value. VSC keeps its existing manual monitoring restart behavior. Do not enable additional schedules or send live test notifications as part of these checks.

## Recovery

Stop the app and retain a separate copy of the failed-upgrade state. Reconcile uncertain publications and notification receipts before another attempt. Rehearse the previous immutable image against a copy before using the supported package recovery procedure. These releases add private configuration without replacing saved-state formats, but container startup alone does not prove rollback compatibility.

Restore a complete consistent compatible backup only if needed and separately authorized. Never restore individual database files into an active volume. Preserve the private config and failed-upgrade evidence until recovery is understood. An older backup can restore messages or records that have already been processed, so reconcile those effects before resuming work.

Old images and Git history retain their earlier contents. This migration removes personal defaults from future images; it does not erase earlier publications.
