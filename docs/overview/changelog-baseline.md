---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

The latest dated changelog entry is **1.2.0**. This page excludes Unreleased entries; the [Changelog](/docs/reference/changelog/) retains them when present. Other developer guides follow merged `main`, which can include changes after the published desktop tag.

[Download v1.2.0 and read its publication and platform-validation notes](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.2.0). The changelog date records the source release entry; GitHub Releases records when the downloads were published.

See the [Feature Set](/docs/overview/features/) for current controls and the upstream [release records](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/README.md) for version-specific validation and platform coverage.

## 1.2.0 Release Notes

- WTF now selects Flat Media 95% of the time (5% total for optional scenes).
- WTF validates glyph visibility, dim footage and audio response, checks its fallback, and shares shadow-preserving limits with native Pop Out.
- Add six subtle Flat Media presets: Threadlight, Silver Etching, Contour Silk, Julia Glass, Chromatic Undertow and Phosphor Lace.
- Add Fractal Accents with independent Amount/Coverage, edge/midtone/quiet-area/trail placement, scale, slow drift, restrained audio response, six curated variations and a MIDI-learnable Another variation action.
- Make accents visible in glyph and monochrome looks, retain them across ordinary built-in preset changes, and apply them to all optional scene modes. Add an explicit Off choice and automatic short trails when echo is zero.
- Integrate all six accent recipes into WTF, with an independent 65% accent / 35% Off choice retained across safety retries. Increase preset strength while keeping bounded source visibility.
- Default the persistent global Subtle Limit on; preserve it across presets, saves, imports and WTF. Bound accent brightness, color, glyph changes and displacement without changing the clean-profile Classic Camera ASCII look.
- Share bounded accent math across WebGPU, WebGL2, native wgpu and Canvas. Extend parity, source-continuity, freeze, bypass, audio, trail-decay and preset-matrix checks; the catalog is now 96 total / 68 accelerated / 28 explicit Canvas.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
