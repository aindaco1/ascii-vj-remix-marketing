---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

The latest dated changelog entry is **1.1.0**. This page excludes Unreleased entries; the [Changelog](/docs/reference/changelog/) retains them when present. Other developer guides follow merged `main`, which can include changes after the published desktop tag.

[Download v1.1.0 and read its publication and platform-validation notes](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.1.0). The changelog date records the source release entry; GitHub Releases records when the downloads were published.

See the [Feature Set](/docs/overview/features/) for current controls and the upstream [release records](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) for version-specific validation and platform coverage.

## 1.1.0 Release Notes

- Accept Windows and Unix line endings when loading shared native shaders, preventing a Windows Pop Out shader initialization panic.
- Hold decoded video frames through WebGPU submission to avoid transient external-texture bind failures. Keep the render loop recoverable after errors and count only submitted frames.
- Make Audio Reactivity Stop cancel unfinished capture requests and serialize native Stop/Start. Restore audio slider tuning when selecting a preset, show custom tuning explicitly, and apply audio changes during Pop Out transitions.
- Add eleven original presets: Neon Night Drive, Media Corridor, Wet Coast, Neon Cathedral, Orbital Chamber, Ashen Ruins, Fractal Dive, Mandelbulb Bloom, Mandelbox Passage, Edge Etching and Phosphor Echo. Brightness Relief is removed from the built-in catalog; its visual mode remains compatible with saved looks. Orbital Chamber no longer has an Experimental label.
- Start all built-in presets, including Ashen Ruins, in Flat Media. Keep scene recipes available for manual Space / Motion selection and saved custom looks. WTF independently chooses Flat Media 80% of the time and shares the other 20% equally among all ten spatial modes; preset anchors, safety retries and fallback retain that choice.
- Reduce audio response delay with 120 Hz feature polling, smaller supported native input buffers, immediate attacks and a shared time-based release envelope. Smoothing zero now fully disables smoothing. Ignore stale capture replies and avoid applying audio modulation twice in Pop Out.
- Add a shared GPU scene shader for WebGPU, WebGL2 and native Pop Out: variable-height grid geometry, roof visibility, floors/ceilings, stable facade textures, fog, directional/contact shading, window emission, wet reflections and depth-tested rain. Canvas has a bounded software reference.
- Map the selected image, playing video or camera onto larger scene surfaces with aspect-aware repeat/fit/crop controls. Optional scene recipes use 80–95% media, and material glyphs fade to preserve source shapes. Presets retain source identity and playback.
- Add signed travel speed, freeze/reset, route selection, material glyphs, edge-directed ASCII with hysteresis, and reusable floating-point feedback history with elapsed-time decay, zoom and rotation.
- Reuse the shared transport and bounded audio features for scene modulation; expose visual controls and transport actions to MIDI without adding source/capture/output actions.
- Add a global Bright output toggle, off by default, that strongly lifts dark media before color/glyph selection and stays set across presets and launches. Turning it off retains the previous color response.
- Give optional scene recipes distinct camera heights/tilts, speeds and framing, plus a narrow corridor, pitched cathedral roof, low shoreline and rotating orbital view. Add shared bounded recursive-ruin, Mandelbrot, Mandelbulb and Mandelbox scenes with zoom, detail and shape controls.
- Keep manual visual and MIDI edits made during a preset transition instead of letting the transition overwrite them; retain the current Custom look and playing media.
- Preserve the default Classic Camera ASCII selection, Auto backend preference and density limits. The preset ownership contract is now 90 total / 62 accelerated / 28 explicit Canvas.
- Add geometric, transport, CPU/GPU pixel-parity, trail-decay and video-continuity checks. See [release scope and acceptance](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md).



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
