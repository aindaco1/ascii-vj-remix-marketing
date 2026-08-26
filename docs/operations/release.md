---
title: "Release and Updates"
description: "Source-derived Release and Updates documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 6
parent: "Operations"
---

# Release and Updates

## Current Release Posture

- Current source docs describe the **0.9.9** feature set.
- Public 0.9.9 macOS artifacts are Developer ID signed, notarized, stapled, and Gatekeeper-validated.
- Public 0.9.9 Windows artifacts are unsigned previews.
- Production builds check GitHub Releases metadata once at launch without blocking startup; newer signed releases appear in the existing Update control.
- Manual rechecks remain available, while download, installation, and relaunch require explicit user action.
- Updater and release checks must not broaden runtime network capability.

## macOS

Public release CI treats macOS signing/notarization as fail-closed. The 0.9.9 artifacts passed signing, notarization, stapling, and Gatekeeper validation. Versions 0.9.6 and 0.9.7 require a one-time manual DMG upgrade to 0.9.9 because their production capability set hid the Update control. Local or test builds may still require the normal macOS right-click Open or Open Anyway flow.

## Windows

Inactive Windows signing configuration and Authenticode verification helpers remain in the source tree, but the 0.9.9 public release workflow does not use them. Its Windows artifacts are unsigned previews.

## Crash Reporting

Production crash reporting is reviewed/sanitized and routed through the Rust desktop layer to the Cloudflare Worker relay at `https://crash.dustwave.xyz`. The webview does not get arbitrary HTTP capability. Reports are bounded and sanitized: media files, frames, raw audio, full paths, tokens, cookies, private environment values, and arbitrary diagnostic logs are not included. The Reports control stays visible with an empty queue so the preference can be reviewed without creating or submitting a report.

## Release Validation

Release CI resolves one immutable tag commit, requires the exact commit's successful desktop workflow, builds the app and pinned FFmpeg runtime concurrently, and verifies restored artifacts before packaging. Published-release smoke then launches the packaged app on macOS, Windows, and Linux, requires Update and Reports to remain visible, requires the duplicate backend readout to stay absent, and retains installer, signing, notarization, updater-signature, and real replacement checks appropriate to each platform.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
