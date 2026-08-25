---
title: "Release and Updates"
description: "Source-derived Release and Updates documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 6
parent: "Operations"
---

# Release and Updates

## Current Release Posture

- Current source docs describe the **0.9.6** feature set.
- Public 0.9.6 macOS artifacts are Developer ID signed, notarized, stapled, and Gatekeeper-validated.
- Public 0.9.6 Windows artifacts are unsigned previews.
- GitHub Releases updater infrastructure is configured.
- Updater and release checks must not broaden runtime network capability.

## macOS

Public release CI treats macOS signing/notarization as fail-closed. The 0.9.6 artifacts passed signing, notarization, stapling, and Gatekeeper validation. Local or test builds may still require the normal macOS right-click Open or Open Anyway flow.

## Windows

Inactive Windows signing configuration and Authenticode verification helpers remain in the source tree, but the 0.9.6 public release workflow does not use them. Its Windows artifacts are unsigned previews.

## Crash Reporting

Production crash reporting is reviewed/sanitized and routed through the Rust desktop layer to the Cloudflare Worker relay at `https://crash.dustwave.xyz`. The webview does not get arbitrary HTTP capability. Reports are bounded and sanitized: media files, frames, raw audio, full paths, tokens, cookies, and private environment values are not included.

## Release Validation

Release checks include desktop checks, renderer math, audio-reactive helper tests, crash relay tests, Tauri policy checks, and signing/updater verification appropriate to each platform.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
