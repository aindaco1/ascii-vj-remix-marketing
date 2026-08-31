---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **1.0.0** feature set. The newest dated changelog entry is the release authority; the Unreleased section is intentionally excluded.

## 1.0.0 Release Notes

### Added

- Added live preset-name search with separate, independently alphabetized
  Built-in and My Presets sections, result status, keyboard clearing, and
  no-results states.
- Added release-profile pull-request packages for physical QA: an unsigned,
  updater-disabled Windows development installer plus AppImage, deb, and rpm
  Linux development packages retained for 14 days. Each package set includes
  the pinned, platform-built, verified FFmpeg/ffprobe resources.
- Added a non-destructive Hyper-V bootstrap and acceptance guide for Ubuntu
  26.04.1 and Fedora 44 x86_64 test VMs on Windows 11 Pro.
- Added a PE subsystem gate that rejects a Windows release-mode executable
  unless it is marked as a graphical application.

### Changed

- Promoted the synchronized source/package metadata to the stable 1.0.0
  release.
- Made Classic Camera ASCII the default visual state for a clean profile while
  preserving persisted profiles, and renamed the Point & Click Default display
  label to Dense Color ASCII without changing its stable preset id.
- Standardized sidebar select widths, heights, label columns, row spacing, and
  value presentation; removed the redundant one-option Atlas Style control.
- Labeled Advanced Density with its `Up to 900 columns` and no-30-FPS-guarantee
  constraint directly in the control row.
- Pinned Linux build and release acceptance runners to Ubuntu 24.04.

### Fixed

- Bound remote crash submission to both the production bundle identifier and a
  release build. Optimized `ASCII VJ Remix Dev` QA packages now keep reports
  local, label that state in the Reports UI, and cannot submit as production.
- Added real RFC 3339 capture timestamps plus safe script/line/column and
  requested/resolved renderer context to diagnostic issues without exposing
  local paths. Native WebKit stack frames are no longer mistaken for emails.
- Contained blocked Canvas2D pixel readback, including WebKit `SecurityError`
  code 18, inside the renderer instead of escalating it as a global app error.
- Added Linux-owned 1000x680 startup geometry with a 900x600 minimum instead of
  inheriting the larger macOS/Windows window, while deriving the development
  window title from its product identity rather than duplicating geometry.
- Added platform-owned built-in Demo Video formats: H.264/MP4 for macOS and
  Windows webviews, and VP8/WebM for clean Ubuntu and Fedora installations that
  lack optional H.264 GStreamer codecs. Existing saved Demo Video selections
  migrate to the correct platform asset, while both shipped demo formats and
  user-selected videos retry through bundled FFmpeg if the platform decoder
  rejects them. Exact bundled source ids preserve the existing narrow file
  access boundary.
- Treat unavailable or disconnected microphone devices as an expected hardware
  condition. The app can attempt its browser fallback and no longer queues a
  crash report merely because a VM has no usable microphone; legacy reports for
  that exact condition are pruned on the next launch.
- Made the Podman wrappers reuse an already-healthy default connection before
  starting their fallback VM, avoiding macOS's one-active-machine collision
  with other project checkouts.
- Decoupled the clean-profile Classic Camera ASCII look from the global
  renderer preference. Built-ins that do not explicitly request a compatibility
  backend now start from Auto and resolve to WebGPU/WebGL2 when available on
  every packaged desktop host.
- Restored real WebGPU glyph rendering in the packaged macOS Apple WebKit view.
  Glyph pages now decode through the bundled asset URL and compact the active
  maximum-96-scalar ramp plus its coverage mips into a two-row RGBA texture
  below WebKit's problematic wide-texture boundary. The installed preset sweep
  resolves 41 built-ins to WebGPU and 28 intentional compatibility presets to
  Canvas2D, with all 69 visible; Paper Shredder explicitly retains Canvas2D to
  preserve the look it predates glyph-atlas parity with.
- Increased the packaged preset sweep's primary-canvas sample resolution so
  sparse Braille, kana, Hangul, and box-drawing strokes are evaluated before
  thumbnail downsampling can average them away.
- Synchronized primary-view and native Pop Out transitions on one timestamped
  clock. Numeric transitions now use the same easing progress on both surfaces,
  renderer-family changes use the same crossfade curve, and native presentation
  uses minimum swapchain buffering instead of trailing by queued parameter
  round trips.
- Timestamped the primary video playback handoff so the native decoder advances
  its initial seek by the time spent opening the output window and starting the
  decoder, removing avoidable Pop Out playback lag.
- Pinned native Pop Out to a browser-parity non-sRGB unorm surface format when
  the platform supports it, preventing platform format order from applying an
  extra sRGB conversion to the shared renderer colors.
- Prevented release-mode Windows app and FFmpeg/ffprobe child processes from
  opening visible console windows. Debug builds retain normal diagnostic
  console behavior.
- Retired the blanket Windows WebView2 glyph-to-Canvas policy now that the
  compact active-ramp glyph texture is shared by the repaired WebGPU path.
  Auto presets again attempt WebGPU on Windows, with WebGL2 and Canvas2D kept as
  real construction fallbacks. A centralized 69 total / 41 accelerated / 28
  explicit Canvas contract, a collapsed-seven unit regression, the visible
  preset sweep, and the Windows CI matrix guard this ownership boundary.
- Made the preset overflow menu focus its first action, close with Escape, and
  restore focus to its trigger.
- Made the local signing bootstrap import its temporary PKCS#12 identity with a
  Keychain-compatible password, and made the local launcher refuse to delete a
  bundle when its source and install paths are the same.

Version 1.0.0 completes the first stable desktop release with a polished preset
workflow, cross-platform packaged media handling, synchronized native Pop Out
transitions and color, and one explicit 69 total / 41 accelerated / 28 Canvas
built-in renderer contract. macOS artifacts remain Developer ID signed,
notarized, stapled, and Gatekeeper-validated; Windows artifacts remain clearly
documented unsigned previews.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
