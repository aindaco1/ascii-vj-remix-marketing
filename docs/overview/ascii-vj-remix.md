---
title: "ASCII VJ Remix"
description: "Source-derived ASCII VJ Remix documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 1
parent: "Overview"
---

# ASCII VJ Remix

ASCII VJ Remix is a local-first native desktop renderer lab for turning images, videos, cameras, and audio-reactive signals into high-performance ASCII and cell-based visuals.

It is built for VJ-style experimentation: pick a source, choose or build a preset, push the renderer hard, pop output onto another display, and keep tuning the look live while media keeps running.

Current source docs describe the **0.9.3** feature set.

## Product Boundary

- The intended product is the packaged desktop app for macOS, Windows, and Linux.
- Browser/Vite mode is useful for development, smoke tests, and renderer portability, but it is not the main product framing.
- Runtime is local-first and offline by default.
- User-selected media, camera frames, and audio remain local.
- Intentional online paths are limited to the GitHub Releases updater and production-only reviewed/sanitized crash report submission.
- Stream infrastructure exists, but the normal Source UI hides stream mode until it is ready as a standalone user feature.
- MIDI hardware control is planned, but is not part of the current normal-user feature set.

## Project Lineage

ASCII VJ Remix combines three source lineages:

- **ASCILINE**: high-performance ASCII video streaming, adaptive frame encoding, Python/OpenCV experiments, terminal ideas, and Canvas fallback lineage.
- **ascii-point-and-click**: high-quality WebGPU/WebGL visual output and local browser media-source architecture.
- **ASCII VJ Remix desktop work**: Tauri packaging, native media/audio adapters, native Pop Out output, local release/update infrastructure, crash reporting, and the dense VJ control surface.

## System Requirements

### macOS

- Minimum: Apple Silicon Mac, macOS 13 Ventura or newer, 8 GB RAM, Metal-capable GPU, and about 2 GB free disk space.
- Optimal: M1 Pro/Max, M2 Pro/Max, M3 Pro/Max, or newer; 16 GB RAM or more; macOS 14 Sonoma, macOS 15 Sequoia, or newer; external display/projector for Pop Out.
- Intel Mac support is not the current release target.
- Camera, microphone, and audio capture require explicit macOS privacy grants.
- Public macOS release builds should be Developer ID signed and notarized.

### Windows

- Minimum: Windows 10 22H2 or Windows 11, x64 CPU, WebView2 runtime, D3D12 or WebGL2-capable GPU, 8 GB RAM, and about 2 GB free disk space.
- Optimal: Windows 11, recent Intel/AMD/NVIDIA GPU with current drivers, 16 GB RAM or more, hardware media decode, and dedicated output display.
- Windows 0.9.3 artifacts are published as unsigned previews until a signing backend is proven.

### Linux

- Minimum: modern x86_64 Linux distribution, WebKitGTK 4.1 runtime, Mesa or vendor GPU drivers with WebGL2, 8 GB RAM, and about 2 GB free disk space.
- Optimal: Ubuntu 24.04, Fedora 40, Arch, or comparable current distro; Wayland or well-configured X11; recent Mesa/NVIDIA drivers; Vulkan-capable GPU; PipeWire for future capture work.
- GPU behavior varies by distro, WebKitGTK version, and graphics driver.

## Practical Hardware Guidance

The renderer can be demanding. Higher grid sizes, multiple cameras, audio reactivity, and native output windows all increase load.

For live camera work, stable USB cameras, direct USB ports or a powered hub, good lighting, AC power, and a dedicated output display often matter more than raw CPU alone.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
