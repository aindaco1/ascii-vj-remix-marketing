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
```

## Prerequisites

Minimum development tools:

- Node.js 24 or newer.
- npm.
- Rust stable toolchain with Cargo.
- Git.
- A current browser. Chromium is preferred for WebGPU testing.

Platform-specific desktop prerequisites:

- macOS: Xcode command line tools.
- Windows: Visual Studio Build Tools with the C++ workload and WebView2
  runtime.
- Linux: WebKitGTK 4.1 development packages, appindicator, ALSA development
  headers, librsvg, OpenSSL, patchelf, and build tools.

Optional but useful:

- Podman for the reproducible Linux dev shell and Python/OpenCV experiments.
- FFmpeg/ffprobe for media-engine development.
- Playwright dependencies for browser smoke tests.
- GitHub CLI for release secret management.

## First-Time Setup

Install JavaScript dependencies:

```bash
npm ci
```

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

On macOS workspaces stored under iCloud Drive, the Tauri build helper redirects
target output to `/private/tmp/ascii-vj-remix-tauri-target` so iCloud extended
attributes do not break app signing. You can override the build directory with
`ASCILINE_TAURI_TARGET_DIR` or `CARGO_TARGET_DIR`.

## First Verification Path

Choose the [recommended check set](/docs/operations/testing/#recommended-check-sets) for the change. Use [Contributing](/docs/development/contributing/) for development identity, local signing, FFmpeg, and Podman, and [Commands](/docs/reference/commands/) for the complete npm script catalog.

For packaging, signing, publication, or updater work, follow [Release and Updates](/docs/operations/release/).

## Development Boundary

Do not add hosted fonts, CDNs, online decoders, telemetry, or hosted runtime dependencies. Keep runtime assets bundled locally and selected user media local.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
- [docs/RELEASING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RELEASING.md)
