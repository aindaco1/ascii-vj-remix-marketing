---
title: "Release and Updates"
description: "Source-derived Release and Updates documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 6
parent: "Operations"
---

# Release and Updates

Current source docs describe the **0.9.12** release line. Release mechanics and security posture are copied from their canonical mother-repository guides.

## Release Security Posture

The current release line includes these security hardening rules:

- Production CSP allows only the app origin, Tauri IPC, and the Tauri asset
  protocol needed for selected local media. Localhost HTTP/WebSocket endpoints
  exist only in the development CSP; stream mode is not a production source.
- Crash report submission is implemented in Rust, not webview `fetch`, so the
  production CSP does not gain arbitrary remote `connect-src` access.
- GitHub Actions updater signing secrets are scoped to the updater-secret check
  and Tauri packaging steps. Do not place `TAURI_SIGNING_PRIVATE_KEY`,
  `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`, Apple certificate values, or keychain
  passwords in job-level workflow environment blocks.
- Public macOS release CI fails closed when Apple Developer ID signing or
  notarization is incomplete. Public 0.9.12 macOS artifacts are signed,
  notarized, stapled, and Gatekeeper-validated; Windows 0.9.12 artifacts are
  unsigned previews.
- Public macOS artifacts must retain Team ID `PWT3Q52LZ2` and the stable
  identifier/team designated requirement. CI validates both the built app and
  the extracted updater archive and rejects ad-hoc or code-hash-only identity.
- Local launch tooling requires the separate `ASCII VJ Remix Dev` identity and
  a stable local signing certificate. It never synchronizes into the production
  application path.
- GitHub Actions macOS jobs are pinned to `macos-26` instead of
  `macos-latest`. The native `wgpu`/`apple-metal` stack needs the macOS 26
  Metal SDK, and the moving `macos-latest` alias can select an older SDK.
- Frontend app state retains the derived playback URL or media id instead of the
  selected local path. Diagnostics redact file and asset URLs before writing
  `/tmp/asciline-media-diagnostics.log`.
- Tauri media registrations and asset grants are session-local. The
  `forget_media_file` command revokes a path grant after its final registration
  is removed; persisted custom-source metadata does not preserve path access
  across app restarts.
- Preset imports must be bounded, schema-checked, clamped through the shared
  control metadata, and stripped of source/media fields before they can affect
  renderer state.
- Glyph-mode native output treats `charset` and custom ramps as untrusted data.
  Resolved ramps are restricted to supported BMP coverage, sanitized as Unicode
  scalars, and capped at 96 ids before reaching renderer buffers. Keep
  `fontFamily` out of native font-loading or resource-lookup paths.
- The neutral glyph atlas is generated offline from a pinned, checksummed source
  retained with its license files. Runtime code may load only the 16 bundled
  atlas pages; it never resolves system fonts or remote font resources.
- Dependency audits cover npm and Rust. `cargo audit` warnings from
  Tauri's current GTK/WebKit transitive stack are tracked as upstream desktop
  framework risk; actionable direct/transitive advisories must be fixed before
  release when an upgrade is available.

## Release and Updater Work

ASCII VJ Remix desktop builds must remain standalone at runtime. The Tauri
updater is an intentional online path: the production app invokes it once in
the background at launch and when the user requests a manual recheck. A current
or failed launch check stays silent. Downloading, installation, and relaunch
remain explicit user actions through the existing Update control.

Releases are published by `.github/workflows/release-desktop.yml`. The release
matrix builds macOS, Windows, and Linux artifacts, verifies them, writes updater
manifest fragments, merges those fragments into `latest.json`, and uploads
installers, updater packages, signatures, and `latest.json` to GitHub Releases.
The workflow builds from the requested `v*` tag so release artifacts match the
tagged source, not whatever happens to be at `main` later.

`.github/workflows/auto-version-release.yml` automates the common release path.
When `package.json`, `package-lock.json`, `src-tauri/Cargo.toml`,
`src-tauri/tauri.conf.json`, or `CHANGELOG.md` changes on `main`, it validates
that the app versions match with `npm run release:version:check`, creates
`vX.Y.Z` when that tag does not already exist, and dispatches the desktop
release workflow with that tag. If the tag already exists, it skips release
dispatch so repeated pushes do not overwrite a published version accidentally.

The GitHub Releases updater reads:

```text
https://github.com/aindaco1/ascii-vj-remix/releases/latest/download/latest.json
```

Updater packages are signed with a minisign key pair. The public key is
committed in `src-tauri/tauri.conf.json`. The private key must be stored as the
GitHub Actions secret `TAURI_SIGNING_PRIVATE_KEY`; never commit it.
`TAURI_SIGNING_PRIVATE_KEY_PASSWORD` is required for the current encrypted
release key.

The current public key was generated with a password-protected key:

```bash
npm run tauri -- signer generate --ci -w /private/tmp/ascii-vj-remix-updater.key -p "$(cat /private/tmp/ascii-vj-remix-updater.password)"
```

For this local workspace, the generated private key is expected at
`/private/tmp/ascii-vj-remix-updater.key` and the password is expected at
`/private/tmp/ascii-vj-remix-updater.password`. Never commit either file.

Set/check the updater key with GitHub CLI:

```bash
npm run updater:secret:check
npm run updater:secret:set
npm run release:secrets:check
npm run release:secrets:check:public
```

The updater secret script passes values to `gh secret set` over stdin, not as
command-line arguments. Use `-- --repo owner/repo` or `-- --key /path/to/key`
after the npm script if the defaults are wrong.

`release:secrets:check:public` requires updater signing and macOS Developer ID
notarization readiness. The current Windows release path publishes unsigned
preview artifacts and does not require Windows signing secrets.

For an updater-disabled local development bundle:

```bash
npm run bundle:debug
```

Production-shaped release packaging still requires the updater key and must not
be installed as a local permission-testing build.

The base config retains `bundle.macOS.signingIdentity = "-"` for portable
packaging defaults, but normal local commands layer
`src-tauri/tauri.dev.conf.json` to change the app name and identifier and disable
production updates. Public macOS release builds use
`src-tauri/tauri.notarized.conf.json` and fail if Developer ID signing and
notarization credentials are missing.

`scripts/run_local_desktop_app.sh` requires the stable local identity by
default. Override `ASCILINE_CODESIGN_IDENTITY` only when deliberately testing a
different stable signing identity:

```bash
npm run desktop:codesign:local
npm run desktop:run-local -- --build
```

Developer ID signing and notarization require Apple Developer Program
membership, a base64 Developer ID Application `.p12`, its password, a CI
keychain password, and either App Store Connect API credentials or Apple ID
notarization credentials. Check readiness or upload App Store Connect API
credentials with:

```bash
npm run release:secrets:check:notarized
npm run release:secrets:set:macos -- \
  --certificate /path/to/developer-id-application.p12 \
  --certificate-password-file /path/to/p12-password.txt \
  --api-key ABCDE12345 \
  --api-issuer 00000000-0000-0000-0000-000000000000 \
  --api-key-file /path/to/AuthKey_ABCDE12345.p8
```

Apple ID credentials are also supported:

```bash
npm run release:secrets:set:macos -- \
  --certificate /path/to/developer-id-application.p12 \
  --certificate-password-file /path/to/p12-password.txt \
  --apple-id-file /path/to/apple-id-email.txt \
  --apple-password-file /path/to/app-specific-password.txt \
  --apple-team-id TEAMID12345
```

When `--keychain-password-file` is omitted, the script generates a random
temporary keychain password and stores it in `KEYCHAIN_PASSWORD`.

The repository contains an inactive Azure Artifact Signing path in
`src-tauri/tauri.windows-signed.conf.json`, which invokes
`src-tauri/windows-artifact-sign.cmd`; that wrapper calls
`scripts/windows_artifact_sign.ps1`. This signs Windows artifacts before Tauri
creates updater signatures. The current Windows release path does not use this
config and publishes unsigned Windows preview artifacts. Configure the Azure
values only after Windows signing is enabled as a release policy:

```bash
npm run release:secrets:set:windows -- \
  --client-id "<app-client-id>" \
  --tenant-id "<tenant-id>" \
  --client-secret-file /path/to/azure-client-secret.txt \
  --endpoint "https://<region>.codesigning.azure.net/" \
  --account "<signing-account-name>" \
  --certificate-profile "<certificate-profile-name>"
node scripts/check_github_release_secrets.mjs --require-windows-signing
```

The helper stores `AZURE_CLIENT_SECRET` as a GitHub Actions secret and the other
Azure IDs as GitHub repository variables. The Azure client secret is the only
required Windows signing secret; keep it out of shell history and chat logs.
Provider selection and Windows signing rollout remain roadmap decisions; the
inactive tooling does not describe the current distribution posture.

Use these checks before publishing release changes:

```bash
npm run check:desktop
npm run test:desktop-updater
npm run test:updater-manifest
npm run check:bundle:debug
```

On this macOS iCloud Drive workspace, Tauri build output is redirected to
`/private/tmp/ascii-vj-remix-tauri-target` to avoid iCloud extended attributes
breaking `codesign`. Normal CI and non-iCloud workspaces continue to use
`src-tauri/target`. Override with `ASCILINE_TAURI_TARGET_DIR` or
`CARGO_TARGET_DIR` when needed.

Local release builds run `npm run ffmpeg:build-sidecar` before
`npm run check:release`. Public release CI keeps the same pinned official FFmpeg
8.1.2 source, completed-download promotion, source SHA-256, disabled network
protocols, and LGPL-compatible resource checks, but builds that runtime in
parallel with `tauri build --no-bundle`. It requires the exact commit's
successful main-push `Desktop` workflow, then hands both outputs to the bundle
jobs as immutable one-day workflow artifacts. The restored app binary is
verified against its commit, platform, version, byte size, and SHA-256 before
`tauri bundle` packages it without recompiling. Runtime builds remain offline;
CI may download official source during release builds, but the packaged app
never downloads FFmpeg, codecs, or renderer assets at runtime.

The release workflow also runs `scripts/smoke_tauri_release_install.mjs` on
macOS, Windows, and Linux after publishing. It downloads artifacts from GitHub
Releases instead of reusing local build directories, catching missing assets,
bad `latest.json` URLs, installer layout issues, a hidden Update control, and
broken signed updater downloads. macOS additionally extracts consecutive
updater archives, requires the DMG to contain the real app, exact
`/Applications` link, and reviewed Tauri Finder metadata; validates the
downloaded DMG and mounted app; extracts
consecutive updater archives; requires the stable production designated
requirement; performs a true updater self-replacement; and validates the
resulting app identity. Release upload does not replace already-published
artifact bytes for the same tag. CI-only smoke hooks are inactive unless these
environment variables are set:

The updater-hop smoke defaults to `ASCILINE_UPDATER_SMOKE_MIN_VERSION=0.9.0`.
Older `0.1.x` releases used an incompatible updater signing key, so they can be
kept as historical releases but cannot be used as a cryptographic updater-hop
baseline for the current app line.

- `ASCILINE_DESKTOP_SMOKE=launch`: bounded launch smoke with a report.
- `ASCILINE_DESKTOP_SMOKE=updater-ui`: requires the packaged production Update
  and Reports controls to remain visible after initialization and requires the
  duplicate top-bar backend readout to be absent.
- `ASCILINE_CRASH_REPORT_SMOKE=submit`: production-only acceptance canary. It
  refuses to run with an existing pending report or an `off` preference,
  captures one hard-coded sanitized report, submits it through the Rust relay
  path, and requires the queue to return to empty.
- `ASCILINE_UPDATER_SMOKE=download`: checks `latest.json`, downloads the signed
  updater package, verifies its signature, writes a report, and exits.
- `ASCILINE_UPDATER_SMOKE=install`: downloads and verifies the updater package,
  writes a pre-install report, and invokes Tauri's installer path.
- `ASCILINE_UPDATER_SMOKE_FORCE_FROM_VERSION`: records the forced older-version
  hop used by CI.

The true app-driven updater hop needs a previous release that already contains
`ASCILINE_UPDATER_SMOKE=install`. Releases before v0.1.5 can only participate in
direct install and updater download smoke.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
