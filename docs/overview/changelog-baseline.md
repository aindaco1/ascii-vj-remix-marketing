---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

The current release is **1.3.0**. The [Changelog](/docs/reference/changelog/) contains the full version history.

[Download v1.3.0](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.3.0).

See the [Feature Set](/docs/overview/features/) for current controls and the upstream [release records](https://github.com/aindaco1/ascii-vj-remix/blob/512974b25a9a768c8d4cd253e3988f33578fdf86/docs/releases/README.md) for version-specific validation and platform coverage.



## 1.3.0 Release Notes

Release scope and platform validation are tracked in the
[1.3.0 release record](https://github.com/aindaco1/ascii-vj-remix/blob/512974b25a9a768c8d4cd253e3988f33578fdf86/docs/releases/RELEASE_1.3.0.md).

- Add native [NDI®](https://ndi.video/) video input/output on the desktop platform paths and native
  Syphon Metal input/output on macOS, with one selected live input and concurrent
  NDI, Syphon and Pop Out destinations. No transport audio.
- Add compact Video I/O controls, explicit source discovery, reconnect handling,
  720p/1080p output formats, and sharing disabled on fresh launch.
- Preserve source transparency independently of glyph selection through GPU,
  Canvas, native output and crossfades; procedural scenes can add visible content.
- Bundle pinned native runtimes and notices, validate staging and sign nested Mac
  libraries. See [Dev evidence and remaining release gates](https://github.com/aindaco1/ascii-vj-remix/blob/512974b25a9a768c8d4cd253e3988f33578fdf86/docs/releases/NATIVE_VIDEO_IO_DEV.md).

NDI® is a registered trademark of Vizrt NDI AB.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/512974b25a9a768c8d4cd253e3988f33578fdf86/CHANGELOG.md)
