---
title: "ASCII VJ Remix"
description: "Source-derived ASCII VJ Remix documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 1
parent: "Overview"
---

# ASCII VJ Remix

Current source docs describe the **0.9.12** feature set. The sections below are selected directly from the mother repository so product identity, requirements, and hardware guidance do not drift into a second hand-maintained contract.

## What This Project Is

ASCII VJ Remix combines several renderer and desktop-tooling ideas:

- It started from [ASCILINE](https://github.com/YusufB5/ASCILINE), which
  provides a high-performance ASCII video streaming pipeline, Python/FastAPI
  server code, OpenCV frame preparation, adaptive WebSocket frame encoding,
  terminal playback experiments, and Canvas rendering fallbacks.
- It includes high-quality WebGPU/WebGL rendering alongside Canvas compatibility
  paths.
- It keeps the local-first spirit of a standalone creative tool. The Tauri app
  packages the renderer, demo media, fonts, native output path, and local media
  adapters so day-to-day use does not require online services.
- It uses an extreme black, white, grey, neon pink, and neon blue VJ control
  surface with compact VCR-style typography and sharp rectangular controls.

The result is a live renderer workbench for stylized ASCII/cell video output.

## System Requirements

These requirements are practical guidance for the current renderer, not a
contract. Higher grid sizes, multiple cameras, audio reactivity, and native
output windows all increase load.

### macOS

| Level | Requirement |
| --- | --- |
| Minimum | Apple M1 or newer, macOS 13 Ventura or newer, 16 GB RAM, Metal-capable GPU, 2 GB free disk space. Official macOS builds are Apple Silicon first. |
| Optimal | M1 Pro/Max, M2 Pro/Max, M3 Pro/Max, or newer; 16 GB RAM or more; macOS 14 Sonoma, macOS 15 Sequoia, or newer; external display/projector for Pop Out. |

Notes:

- Intel Mac support is not the current release target. It may work from source
  if you build a compatible bundle yourself, but it is not the tested path.
- Camera, microphone, and audio capture require explicit macOS privacy grants.
- Public 0.9.12 release builds are Developer ID signed, notarized, stapled, and
  accepted by Gatekeeper. Local or test builds may require the normal macOS
  right-click Open or Open Anyway flow.

### Windows

| Level | Requirement |
| --- | --- |
| Minimum | Windows 10 22H2 or Windows 11, x64 CPU, WebView2 runtime, integrated GPU broadly comparable to Apple M1 graphics with D3D12 or WebGL2 support, 16 GB RAM, 2 GB free disk space. |
| Optimal | Windows 11, recent Intel/AMD/NVIDIA GPU with current drivers, 16 GB RAM or more, hardware media decode, dedicated output display. |

Notes:

- Most current Windows 10/11 systems already include WebView2. If an installer
  reports that WebView2 is missing, install the Microsoft WebView2 Runtime once.
- Native WASAPI system-audio loopback is not implemented. Current system/display
  audio behavior depends on the capture path exposed by the runtime; verify it
  on the target machine before a live session.

### Linux

| Level | Requirement |
| --- | --- |
| Minimum | Modern x86_64 Linux distribution, WebKitGTK 4.1 runtime, Mesa or vendor GPU drivers with WebGL2, 8 GB RAM, 2 GB free disk space. |
| Optimal | Ubuntu 24.04, Fedora 40, Arch, or comparable current distro; Wayland or well-configured X11; recent Mesa/NVIDIA drivers; Vulkan-capable GPU. |

Notes:

- Linux Tauri uses the system WebKitGTK stack, so GPU feature support varies by
  distribution, WebKitGTK version, and graphics driver.
- WebGL2 may be the practical Linux fallback even when WebGPU is not available.
- Native Linux camera/audio/output coverage is limited outside CI and varies by
  distribution and hardware.

## Hardware Guidance

| Level | Hardware |
| --- | --- |
| Minimum | Apple M1-class or comparable 4-core-plus CPU/integrated GPU, 16 GB RAM, WebGL2/Metal/D3D12/Vulkan/GLES support, 1080p display, one camera or one local media source at a time. |
| Optimal | 8 or more performance cores, 16 to 32 GB RAM, Apple Silicon Pro/Max or a recent discrete GPU, hardware video decode, SSD storage, external display/projector, USB or HDMI capture hardware, class-compliant audio interface. |

For live camera work, the best upgrade is often not raw CPU. Use stable USB
cameras, direct USB ports or a powered hub, good lighting, and a machine on AC
power.

## Battery and Heat Warning

ASCII VJ Remix can be demanding. WebGPU/WebGL rendering, high column counts,
multiple cameras, audio analysis, and native output windows can keep the CPU,
GPU, camera, and media decoder active continuously.

On laptops:

- Expect higher battery drain than a normal media player.
- Use AC power for performances or long sessions.
- Lower columns, FPS, camera resolution, and jitter if the machine gets hot.
- Leave Advanced Density off for the performance-guarded range; high column
  counts can increase total cells sharply when auto rows are active.
- Close Pop Out when you do not need a second output surface.
- Prefer the built-in Demo Image or a single video when testing on battery.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
