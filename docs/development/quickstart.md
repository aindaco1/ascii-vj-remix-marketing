---
title: "Quickstart"
description: "Source-derived Quickstart documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 1
parent: "Development"
---

# Quickstart

Use the source repository as the working tree:

```bash
git clone https://github.com/aindaco1/ascii-vj-remix.git
cd ascii-vj-remix
git checkout eebf5bdca6c88c66a04cacd9a2a8256112880fdb
```

## Prerequisites

Minimum development tools:

- Node.js 24 or newer.
- npm.
- Rust stable toolchain with Cargo.
- Git.
- A current browser. Chromium is preferred for WebGPU testing.

Platform-specific desktop prerequisites:

- macOS: full Xcode and its Metal toolchain for Syphon.
- Windows: Visual Studio Build Tools with the C++ workload and WebView2
  runtime.
- Linux: WebKitGTK 4.1 development packages, appindicator, ALSA development
  headers, librsvg, OpenSSL, patchelf, and build tools. Native NDI discovery also
  requires the Avahi client/common libraries and a running `avahi-daemon` service.

Optional but useful:

- Podman for the reproducible Linux dev shell and Python/OpenCV experiments.
- FFmpeg/ffprobe for media-engine development.
- Playwright dependencies for browser smoke tests.
- GitHub CLI for release secret management.

## First-Time Setup

Install JavaScript dependencies:

```bash
git submodule update --init shared/dust-wave-platform
npm ci
npm run video-io:stage
```

SDK staging downloads pinned build inputs from official sources. It supports
macOS arm64 and Windows/Linux x64, and must run before desktop builds/checks.
The browser-only development path does not use native transports. See
[native runtime packaging](/docs/operations/release/#native-video-runtime-packaging).

Run the browser dev server:

```bash
npm run dev
```

Open:

```text
http://127.0.0.1:8010/
```

Run the static smoke test:

```bash
npm run smoke:static
```

Run the desktop app in development mode:

```bash
npm run tauri:dev
```

Run the main desktop validation gate:

```bash
npm run check:desktop
```

Use `npm test` for standard development testing: the existing desktop gate,
static browser smoke, and live Jev review of synthetic behavior evidence.
`npm test -- --offline` explicitly skips the hosted review. See
[Jev development testing](/docs/operations/testing/#jev-development-testing) for local setup.

On macOS workspaces stored under iCloud Drive, the Tauri build helper redirects
target output to `/private/tmp/ascii-vj-remix-tauri-target` so iCloud extended
attributes do not break app signing. You can override the build directory with
`ASCILINE_TAURI_TARGET_DIR` or `CARGO_TARGET_DIR`.

## First Verification Path

Choose the [recommended check set](/docs/operations/testing/#recommended-check-sets) for the change. Use [Contributing](/docs/development/contributing/) for development identity, local signing, FFmpeg, and Podman, and [Commands](/docs/reference/commands/) for the complete npm script catalog.

For packaging, signing, publication, or updater work, follow [Release and Updates](/docs/operations/release/).

## Development Boundary

Do not add hosted fonts, CDNs, online decoders, telemetry, or hosted runtime dependencies. Keep runtime assets bundled locally. Media stays local unless the user enables video sharing: NDI uses the LAN; Syphon shares with apps on the same Mac. Transport audio is not supported.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/CONTRIBUTORS.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/TESTING.md)
- [docs/RELEASING.md](https://github.com/aindaco1/ascii-vj-remix/blob/eebf5bdca6c88c66a04cacd9a2a8256112880fdb/docs/RELEASING.md)
