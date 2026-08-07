# Drumfeet Apps

This is the owner-controlled Umbrel Community App Store for Visual Status Checker.

Add `https://github.com/drumfeet/visual-status-checker-umbrel-store` in umbrelOS under **Community App Stores**. Updates are discovered from this repository and are applied from Umbrel's app update interface.

## Releasing Visual Status Checker

1. Publish a tagged image from `drumfeet/visualstatuscheck`.
2. Pin the published image digest and update the app version and release notes in `drumfeet-visual-status-checker/`.
3. Commit and push this store repository.
4. Use Umbrel to apply the available app update.
