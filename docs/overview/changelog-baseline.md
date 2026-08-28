---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **0.9.12** feature set. The newest dated changelog entry is the release authority; the Unreleased section is intentionally excluded.

## 0.9.12 Release Notes

### Fixed

- Restored visible primary-view output for every built-in Demo Image preset by
  correcting WebGL glyph-page uploads and using cached max-coverage atlas mips
  for glyphs rendered into very small cells.
- Kept solid, pixel, and glyph preset canvases at the source aspect ratio by
  resolving static row counts from the actual cell width and height.
- Added an all-preset primary-view smoke matrix covering activation, visible
  output, WebGL errors, lazy glyph-page completion, and canvas aspect.
- Prevented blank primary-view glyph canvases in the macOS Apple WebKit runtime
  by selecting the existing bounded Canvas2D glyph path there. Solid/pixel
  primary presets retain WebGPU, compatible runtimes retain GPU glyphs, and the
  native Pop Out renderer is unchanged.
- Made the packaged desktop performance smoke reject an advancing renderer
  whose primary canvas has no visible pixel signal.
- Added a packaged Apple WebKit sweep that activates all 69 built-in Demo Image
  presets and checks primary-view visibility, renderer family, running state,
  GPU errors, and source/canvas aspect for each final surface.

Version 0.9.12 restores every built-in preset in the primary app view while
preserving the source aspect ratio and the native Pop Out path. Version 0.9.11
adds performance-budgeted project palettes, ordered dithering,
multilingual glyph controls, custom Unicode ramps, density guardrails, and
renderer/native-output parity. Version 0.9.10 replaces the legacy television artwork with one canonical app
icon generated for every packaged platform and carries the post-0.9.9 Reports
acceptance correction. Version 0.9.9 keeps crash-report preferences reachable
with an empty queue,
removes the duplicate top-bar backend readout, and extends packaged UI smoke to
cover both controls. Version 0.9.8 restores the production Update control and
launch check, adds a packaged UI regression smoke, and shortens release builds
by compiling the app and FFmpeg runtime concurrently before verified artifact
reuse. Version 0.9.7 adds the silent launch-check controller while retaining
user-approved installation and strengthens release transport resilience.
Version 0.9.6 continues the experimental MIDI commissioning work, removes
measured renderer/output hot-path overhead without changing visual math or
quality, and hardens the macOS drag-to-Applications release path. Version 0.9.5
adds 23 credited ascii.today-inspired character presets and
experimental native DIN MIDI control for an Evolution/M-Audio UC-33e through an
iConnectivity mioXC, including four complete controller pages, soft takeover,
numeric preset selection, MIDI Learn, and full-bank SysEx capture/restore.
Version 0.9.3 moves public desktop releases to signed/notarized macOS
distribution, publishes Windows as an unsigned preview while signing is
deferred, and expands audio reactivity with dense-mix controls that reduce
overreaction on busy music. Version 0.9.0 remains the first documentation
baseline for the current ASCII VJ Remix feature set.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
