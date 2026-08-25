---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **0.9.6** feature set.

## 0.9.6 Highlights

- Native macOS Pop Out uploads decoded source frames only when their source-frame version changes while presentation and live parameters continue at display refresh.
- WebGPU reuses uniform backing storage, texture views, and stable bind groups; WebGL2 caches its 18 shader uniform locations after linking.
- Numeric preset and WTF transitions update changing controls during the tween, then synchronize the complete source/camera/control surface once at completion.
- The measured macOS test path removed about 60% of duplicate RGB conversion and texture-upload work for a 24 FPS source presented near 60 FPS without changing renderer math, source/output resolution, shader behavior, or quality controls.
- Version 0.9.5 added 23 credited ascii.today-inspired character presets and experimental native UC-33e/mioXC MIDI with four pages, soft takeover, MIDI Learn, numeric preset selection, and bounded SysEx capture/restore.
- Normal development bundles now use the separate `ASCII VJ Remix Dev` name and `com.asciline.remix.dev` identifier.
- The macOS DMG and updater path validate the drag-to-Applications layout, production identity, signed updater payload, and real application-driven replacement.

## Security Baseline

- MIDI permissions remain confined to the main control window and the first native adapter accepts only mioXC-named ports.
- Development builds cannot replace the production app or inherit its macOS privacy grants.
- Public macOS artifacts must retain the production bundle identifier, Developer ID team, hardened runtime, and stable designated requirement across updates.

## Validation Baseline

The 0.9.6 changelog records optimized app validation, renderer/static/audio/MIDI/Tauri checks, 47 Rust tests, source-upload counters, bounded transition UI work, DMG layout tests, app-identity tests, and published-release updater smoke.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
