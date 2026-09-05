---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

Current docs describe the **1.0.3** feature set. The newest dated changelog entry is the release authority; the Unreleased section is intentionally excluded.

[Download v1.0.3 and read its publication and platform-validation notes](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.3). The changelog date records the source release entry; GitHub Releases records when the downloads were published.

## 1.0.3 Release Notes

### Added

- Added ASCII City Nightshift, an original preset inspired by
  [tweakyourpc's ASCII City](https://tweakyourpc.github.io/ascii-city/), with a
  shared City Nightshift palette, near-black shadows, amber/sage highlights,
  and gently jittering dense terminal glyphs for the selected image, video, or
  camera. Still images animate without audio input.
- Added ASCII World Mint, an original preset inspired by
  [yeahpython's ASCII World](https://yeahpython.github.io/game/game.html), with
  thin mint ASCII glyphs, a dark teal background, and continuous jitter for the
  current image, video, or camera source.
- Added native single-camera Pop Out capture on Windows through Media
  Foundation and on Linux through the bundled local FFmpeg V4L2 input. Both
  feed the existing native `wgpu` renderer and avoid WebView canvas readback
  and per-frame Tauri IPC in the normal path.
- Added Windows DirectShow and Linux V4L2 camera-input fallbacks inside the
  bundled FFmpeg runtime, plus packaging gates that require the corresponding
  input device to be present before release artifacts are accepted.
- Added bounded mirror timing, throughput, and accepted-FPS diagnostics to
  manual reports so physical-machine fallback behavior is measurable.
- Added a Windows-only native camera preview bridge for devices that reject two
  camera clients. One Media Foundation owner now supplies the native Pop Out
  and a latest-frame, binary JPEG preview capped at 640x360 and 30 FPS for the
  existing WebGPU main renderer.

### Changed

- Windows opens one Media Foundation camera session and keeps the main preview
  live through the native preview bridge; Linux keeps its
  exclusive V4L2 flow. Exclusive sessions now finish native worker shutdown
  before the app retries browser capture, with bounded reopen attempts.
- Windows camera selection accepts Chromium's trailing USB model identifier
  when it unambiguously matches the Media Foundation friendly name. Manual
  diagnostics retain the native-open failure reason when mirror fallback is
  required.
- Windows/Linux camera-mirror fallback uses a latest-frame, one-request-in-
  flight 640x360 profile capped at 30 FPS. Other mirror paths retain their
  previous dimensions and 15 FPS cap.
- Manual diagnostics now preserve their reviewed report kind/surface through
  the relay and include native-output runtime state in generated GitHub issues.
  Windows reports retain the failed shared-open reason and the preview bridge's
  accepted FPS, encoded throughput, read, encode, and decode timings.

### Fixed

- WebGL2 palette lookup uploads now preserve row order independently of source
  image orientation, keeping dark and bright colors consistent with the shared
  palette mapping during startup and live palette changes.
- Windows native output now uses the primary renderer's max-coverage glyph
  masks for tiny cells, preserving the pixel-like Acid Snowstorm appearance.
- Windows preview texture, grid, and canvas dimensions update together when
  the native camera changes frame size, preventing stale aspect ratios and
  uncovered right-edge bars after preset changes.
- Windows image/video/camera switches serialize native ownership before loading
  the next main preview. Camera reads are asynchronous and capture is decoupled
  from GPU presentation, so a stalled read cannot block ordinary worker teardown.
- Windows camera startup retains its first capture session instead of probing,
  closing, and reopening the device. GPU driver discovery runs off the UI thread
  and its instance is reused across opens; startup phase timings are logged.
- DirectShow fallback strips Chromium's USB model suffix and escapes device-name
  separators; diagnostics preserve the original native capture failure too.
- Granted the main window the narrow Tauri permission required to read frames
  from the Windows native camera preview bridge. The desktop policy gate now
  verifies every frontend Tauri command has both a generated permission and a
  main-window capability, preventing packaged builds from silently denying a
  newly added command.

### Preserved

- macOS single-camera Pop Out remains on the existing AVFoundation/display-link
  implementation. No macOS capture or presentation code was changed.
- Multi-camera output and unsupported native-device cases retain the bounded
  mirror fallback.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
