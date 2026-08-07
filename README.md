# Drumfeet Apps

This is the owner-controlled Umbrel Community App Store for Visual Status Checker. The app is installed from a public, digest-pinned GitHub Container Registry image; the image is public so umbrelOS can pull it without GitHub credentials.

Add `https://github.com/drumfeet/visual-status-checker-umbrel-store` in umbrelOS under **Community App Stores**. Updates are discovered from this repository and are applied from Umbrel's app update interface.

## Releasing Visual Status Checker

1. Update the release version and notes in `drumfeet/visualstatuscheck`, validate it, and push its matching `v<version>` tag.
2. Wait for the source repository's image-publishing workflow to succeed, then download its `image-digest` artifact.
3. In `drumfeet-visual-status-checker/`, update `umbrel-app.yml` with the same version and release notes. Update `docker-compose.yml` to the exact `ghcr.io/drumfeet/visual-status-checker:<version>@<digest>` image reference.
4. Commit and push this store repository. umbrelOS will discover the update; apply it from the installed app's update interface.

Never publish a mutable tag without its sha256 digest. Do not place promo codes, Discord webhooks, access tokens, `.env` files, screenshots, or `/data` contents in the image or this store repository. Runtime configuration stays in the app's mounted `/data` directory.
