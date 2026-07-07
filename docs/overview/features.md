---
title: "Feature Set"
description: "Source-derived Feature Set documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 2
parent: "Overview"
---

# Feature Set

This page describes the current ASCII VJ Remix feature baseline for developers planning forks, ports, integrations, or feature work.

## Source Inputs

- Local image files.
- Local video files.
- MKV file selection where the active platform decoder path can handle playback.
- Camera/webcam input.
- Multiple simultaneous cameras when the OS and runtime allow concurrent capture.
- Camera mixer layouts: grid, split row, stack, and picture-in-picture.
- Camera controls for device selection, capture size, FPS, layout, framing, and mirror.
- Audio analysis inputs: mic/input, local audio files, and system/display audio where the OS exposes it to the desktop app.

Selected media and camera frames stay local. The renderer receives playable media URLs or session-local registered ids; it does not receive broad filesystem access.

## Rendering Backends

- WebGPU is the primary quality target on capable desktop runtimes.
- WebGL2 is the main embedded GPU fallback.
- Canvas2D remains the compatibility path for traditional glyph-style ASCII output.
- Pixel Canvas remains available as a compatibility fallback.
- Native Tauri Pop Out uses a `wgpu` presenter where available:
  - Metal on macOS.
  - D3D12 on Windows.
  - Vulkan/GLES on Linux.
- Native Pop Out preserves glyph mode and character-set parameters for traditional ASCII presets instead of flattening them into solid cells.

## Live Renderer Controls

The app keeps source selection, presets, WTF mode, audio modulation, native output, and future MIDI work routed through one canonical parameter model.

Major control groups include:

- Source mode, media id/URL, media type, and source name.
- Camera device ids, resolution, FPS, layout, framing, and mirror.
- Backend selection: auto, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
- Grid: columns, rows, auto rows, cell dimensions, and aspect correction.
- Color: saturation, contrast, brightness, gamma, background blend, and quantization.
- Sampling: FPS, jitter amount, jitter speed, sample position, and smoothing.
- Glyph/cell behavior: glyph mode, solid mode, compact character set, font family menu, and minimum glyph intensity.
- UI/performance: stats overlay and transition timing.

Static renderer-family transitions keep media ownership at the shared runtime layer. Canvas2D, pixel Canvas, WebGL, and WebGPU renderers can crossfade over the same live source instead of destroying and reloading media when backend, glyph, or solid-cell behavior changes.

## Presets

ASCII VJ Remix includes read-only built-in visual presets and user-managed presets.

Built-in visual families include extreme looks such as Neon Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder, Cyberdelic Riot, Acid Snowstorm, Terminal Collapse, and Neon Razorstorm.

Traditional ASCII presets include Classic Camera ASCII, ANSI Newsprint, Terminal Mono, and Dense Typewriter.

User presets can be saved, duplicated, updated, deleted, imported, and exported. Presets preserve the active media source unless the user explicitly changes it.

## Transitions and WTF Mode

- Preset transitions crossfade instead of fading to black.
- Transition time is configurable.
- Static video/camera transitions can move between GPU, solid/pixel, and Canvas2D glyph renderers while keeping playback live.
- WTF mode continuously transitions through randomized live-safe settings.
- WTF mode can anchor randomization around both extreme preset families and traditional ASCII presets.
- Safe clamps avoid pure black or pure white output during random or audio-driven states.

## Audio Reactivity

Audio reactivity is enabled by default and starts from Mic/Input by default.

It analyzes bounded features rather than raw audio buffers:

- RMS.
- Bass.
- Low-mid.
- Mid.
- High-mid.
- Treble.
- Presence.
- Brightness.
- Density.
- Transient energy and flux.
- Beat pulse.
- Spectral movement.

Dense-mix dampening and noise-floor controls help busy tracks stay reactive without pinning jitter and beat response at maximum. Audio modulation affects live effective render params without rewriting saved presets.

## Pop Out and External Displays

Pop Out creates a separate output window for a projector, capture card, or secondary display. The main control window remains available for live tuning.

The output window is presentation-focused and has a minimal command surface. When Tauri can enumerate displays, output display selection is persisted.

## Packaging and Updates

- Built with Tauri v2.
- Production runtime is local-only by default.
- GitHub Releases updater infrastructure is configured.
- Public macOS release CI requires Developer ID signed and notarized artifacts.
- Windows 0.9.3 artifacts are explicitly unsigned preview builds.
- Crash report submission is production-only, reviewed/sanitized, and routed through the Rust desktop layer to the Cloudflare Worker relay.

## Advanced Paths

- Legacy ASCILINE stream work and newer Rust/FFmpeg stream sessions exist but are hidden from the normal Source UI.
- FFmpeg sidecar policy and codec support live in contributor/release work.
- MIDI hardware control is planned, with an Evolution/M-Audio UC33e through iConnectivity mioXC named as the first validation target.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
