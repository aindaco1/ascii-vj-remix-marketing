---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **0.9.9** feature set.

## 0.9.9 Highlights

- The Reports control remains visible with an empty queue so users can review the existing `ask`, `always`, and `off` preference before an error occurs. Pending reports still add a count and warning state.
- The duplicate right-side backend readout is removed. The center Backend selector remains the canonical control, and the user-owned Stats Overlay retains resolved runtime diagnostics.
- Packaged updater UI smoke listeners bind before device initialization so camera or audio startup cannot race an early smoke request.
- Published-release smoke launches packaged macOS, Windows, and Linux builds, requires Update and Reports to remain visible, and requires the duplicate backend readout to stay absent.
- The recent release line also includes the 0.9.8 updater and release-pipeline fixes, the 0.9.6 renderer and native-output optimizations, and the presets and experimental UC-33e/mioXC MIDI introduced in 0.9.5.

## Security Baseline

- Reports continue to contain only bounded, sanitized crash data. Local media diagnostics and arbitrary logs are not attached or submitted.
- The opt-in production acceptance canary refuses to run when a user report is already pending and submits only a hard-coded synthetic payload.
- The launch update check sends no media, camera, audio, preset, MIDI, crash-report, or local-path data and does not block app startup when the network is unavailable.
- Updater packages remain signed, and installation never starts without a user action.
- Development builds cannot replace the production app, inherit its macOS privacy grants, or use the production updater endpoint.
- Public macOS artifacts must retain the production bundle identifier, Developer ID team, hardened runtime, and stable designated requirement across updates; current Windows artifacts remain unsigned previews.

## Validation Baseline

The 0.9.9 changelog records deterministic crash-report UI state tests plus packaged checks for Update, Reports, and the single backend control on macOS, Windows, and Linux. The broader release gate retains renderer, audio, MIDI, Tauri policy, signing, notarization, installer, and updater replacement checks.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
