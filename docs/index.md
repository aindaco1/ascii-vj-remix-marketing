---
title: "Overview"
description: "Developer overview for ASCII VJ Remix, including source-derived architecture, feature, development, operations, and reference documentation."
nav_order: 1
---

# Overview

These docs are for software developers who want to fork, inspect, extend, package, or contribute to ASCII VJ Remix.

ASCII VJ Remix is a local-first desktop visualizer and renderer workbench. For users, it exists to give DJs a manageable visualizer and VJs fine-grained ASCII/video filter control. For developers, it is a Tauri desktop application with a dense renderer/control surface, native output path, local media adapters, audio-reactive modulation, and release/update infrastructure.

The public homepage is written for DJs and VJs. This section is intentionally technical: it describes the app's source model, renderer architecture, desktop packaging boundary, security posture, performance constraints, accessibility expectations, internationalization posture, release workflow, and current 0.9.3 feature baseline.

## Start Here

1. [ASCII VJ Remix overview](/docs/overview/ascii-vj-remix/) for product scope, release baseline, platform requirements, and current capabilities.
2. [Feature Set](/docs/overview/features/) for a comprehensive source-derived map of what the app can do.
3. [Quickstart](/docs/development/quickstart/) for local setup and first verification commands.
4. [Architecture](/docs/development/architecture/) and [Rendering Engine](/docs/development/rendering-engine/) before changing source, renderer, preset, audio, camera, or Pop Out behavior.
5. [Security](/docs/operations/security/), [Performance](/docs/operations/performance/), [Testing](/docs/operations/testing/), [Accessibility](/docs/operations/accessibility/), and [Internationalization](/docs/operations/internationalization/) before shipping a fork.

## Overview Pages

- [ASCII VJ Remix](/docs/overview/ascii-vj-remix/) — scope, lineage, release baseline, platform requirements, and project boundary.
- [Feature Set](/docs/overview/features/) — comprehensive map of sources, rendering, presets, live controls, audio reactivity, Pop Out, packaging, security, and advanced paths.
- [Release Baseline](/docs/overview/changelog-baseline/) — current release line and recent behavior changes from the changelog.

## Source-derived sections

- [Development](/docs/development/) covers local setup, architecture, rendering internals, contribution workflow, and LLM-agent guidance.
- [Operations](/docs/operations/) covers security, performance, testing, accessibility, i18n, packaging, updates, and crash reporting.
- [Reference](/docs/reference/) covers commands, roadmap, changelog, and source-to-docs mapping.



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [README.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/README.md)
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/CHANGELOG.md)
- [docs/RENDERING_ENGINE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/RENDERING_ENGINE.md)
- [docs/CONTRIBUTORS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/CONTRIBUTORS.md)
- [docs/AGENTS.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/AGENTS.md)
- [docs/SECURITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/SECURITY.md)
- [docs/PERFORMANCE.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/PERFORMANCE.md)
- [docs/TESTING.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/TESTING.md)
- [docs/ACCESSIBILITY.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ACCESSIBILITY.md)
- [docs/I18N.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/I18N.md)
- [docs/ROADMAP.md](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/ROADMAP.md)
