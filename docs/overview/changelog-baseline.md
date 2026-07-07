---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **0.9.3** feature set.

## 0.9.3 Highlights

- Public macOS release builds require Developer ID signing and notarization.
- Windows release artifacts are published as unsigned previews until a signing backend is proven.
- Audio reactivity has shared defaults, control metadata, presets, feature normalization, dense-mix dampening, and render-parameter modulation.
- New audio-reactive controls cover transient/flux amount, presence amount, density dampening, and noise floor.
- Flux and density meters are available alongside a Dense Mix Control audio-reactive preset.
- Browser preview, Pop Out, stream paths, and native output consume shared audio-reactive modulation rules.
- Static video/camera transitions crossfade between renderer families without destroying the shared media source.
- Traditional Canvas2D ASCII presets default to visible static-image jitter.

## Security Baseline

- Future Windows signing uses environment-scoped signing credentials and does not commit certificate files, client secrets, or private signing material.
- Audio reactivity sends bounded feature vectors through IPC; raw audio, frames, media files, and paths remain local.
- Release signing and updater signing checks treat macOS public distribution as fail-closed.

## Validation Baseline

The changelog records checks for audio reactivity, Windows Authenticode preparation, desktop/release gates, camera Pop Out behavior, native glyph masking, live renderer transitions, WTF mode, traditional ASCII jitter, and Tauri policy permissions.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
