#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "pathname"

ROOT = Pathname(__dir__).join("..").expand_path
SOURCE_ROOT = Pathname(ENV.fetch("ASCII_VJ_SOURCE", "/Users/aindaco1/Library/Mobile Documents/com~apple~CloudDocs/ascii-vj-remix")).expand_path
SOURCE_REPO = ENV.fetch("ASCII_VJ_REPO", "aindaco1/ascii-vj-remix")
BLOB_BASE = "https://github.com/#{SOURCE_REPO}/blob/main/"
TREE_BASE = "https://github.com/#{SOURCE_REPO}/tree/main/"

SOURCE_FILES = {
  readme: "README.md",
  changelog: "CHANGELOG.md",
  rendering: "docs/RENDERING_ENGINE.md",
  contributors: "docs/CONTRIBUTORS.md",
  agents: "docs/AGENTS.md",
  security: "docs/SECURITY.md",
  performance: "docs/PERFORMANCE.md",
  testing: "docs/TESTING.md",
  accessibility: "docs/ACCESSIBILITY.md",
  i18n: "docs/I18N.md",
  roadmap: "docs/ROADMAP.md"
}.freeze

DOCS = [
  ["docs/index.md", "Overview", nil, 1, :docs_index],
  ["docs/overview/ascii-vj-remix.md", "ASCII VJ Remix", "Overview", 1, :product_overview],
  ["docs/overview/features.md", "Feature Set", "Overview", 2, :features],
  ["docs/overview/changelog-baseline.md", "Release Baseline", "Overview", 3, :release_baseline],
  ["docs/development/index.md", "Development", nil, 2, :development_index],
  ["docs/development/quickstart.md", "Quickstart", "Development", 1, :quickstart],
  ["docs/development/architecture.md", "Architecture", "Development", 2, :architecture],
  ["docs/development/rendering-engine.md", "Rendering Engine", "Development", 3, :rendering_engine],
  ["docs/development/contributing.md", "Contributing", "Development", 4, :contributing],
  ["docs/development/agent-guide.md", "Agent Guide", "Development", 5, :agent_guide],
  ["docs/operations/index.md", "Operations", nil, 3, :operations_index],
  ["docs/operations/security.md", "Security", "Operations", 1, :security],
  ["docs/operations/performance.md", "Performance", "Operations", 2, :performance],
  ["docs/operations/testing.md", "Testing", "Operations", 3, :testing],
  ["docs/operations/accessibility.md", "Accessibility", "Operations", 4, :accessibility],
  ["docs/operations/internationalization.md", "Internationalization", "Operations", 5, :internationalization],
  ["docs/operations/release.md", "Release and Updates", "Operations", 6, :release],
  ["docs/reference/index.md", "Reference", nil, 4, :reference_index],
  ["docs/reference/commands.md", "Commands", "Reference", 1, :commands],
  ["docs/reference/roadmap.md", "Roadmap", "Reference", 2, :roadmap],
  ["docs/reference/changelog.md", "Changelog", "Reference", 3, :changelog],
  ["docs/reference/source-map.md", "Source Map", "Reference", 4, :source_map]
].freeze

ALIASES = {
  "README.md" => "/docs/overview/ascii-vj-remix/",
  "CHANGELOG.md" => "/docs/reference/changelog/",
  "docs/RENDERING_ENGINE.md" => "/docs/development/rendering-engine/",
  "docs/CONTRIBUTORS.md" => "/docs/development/contributing/",
  "docs/AGENTS.md" => "/docs/development/agent-guide/",
  "docs/SECURITY.md" => "/docs/operations/security/",
  "docs/PERFORMANCE.md" => "/docs/operations/performance/",
  "docs/TESTING.md" => "/docs/operations/testing/",
  "docs/ACCESSIBILITY.md" => "/docs/operations/accessibility/",
  "docs/I18N.md" => "/docs/operations/internationalization/",
  "docs/ROADMAP.md" => "/docs/reference/roadmap/"
}.freeze

module SyncAsciiDocs
  module_function

  def read_source(relative)
    path = SOURCE_ROOT.join(relative)
    raise "Missing source file: #{path}" unless path.file?
    path.read
  end

  def source_link(relative)
    path = SOURCE_ROOT.join(relative)
    if path.directory?
      "#{TREE_BASE}#{relative}"
    else
      "#{BLOB_BASE}#{relative}"
    end
  end

  def section(markdown, heading)
    escaped = Regexp.escape(heading)
    match = markdown.match(/^##\s+#{escaped}\s*\n(?<body>[\s\S]*?)(?=^##\s+|\z)/)
    match ? match[:body].strip : ""
  end

  def changelog_version(markdown)
    markdown[/^##\s+\[([^\]]+)\]/, 1] || "current"
  end

  def command_rows(package_json)
    scripts = package_json.scan(/"([^"]+)"\s*:\s*"([^"]+)"/)
    return [] if scripts.empty?
    scripts.select { |name, _| name.match?(/^(dev|build|preview|test|check|tauri|release|smoke|lint|format|podman|sync|verify)/) }
           .map { |name, value| "| `npm run #{name}` | `#{value.gsub('|', '\\|')}` |" }
  end

  def package_json
    path = SOURCE_ROOT.join("package.json")
    path.file? ? path.read : ""
  end

  def page_description(title)
    if title == "Overview"
      "Developer overview for ASCII VJ Remix, including source-derived architecture, feature, development, operations, and reference documentation."
    else
      "Source-derived #{title} documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
    end
  end

  def write_page(path, title, parent, nav_order, body)
    target = ROOT.join(path)
    target.dirname.mkpath
    front = ["---", "title: #{title.inspect}", "description: #{page_description(title).inspect}", "nav_order: #{nav_order}"]
    front << "parent: #{parent.inspect}" if parent
    front << "---"
    target.write((front + ["", body.strip, ""]).join("\n"))
  end

  def source_note(files)
    "\n\n## Source Material\n\nThis page is generated from ASCII VJ Remix source material. Primary sources:\n" +
      files.map { |file| "- [#{file}](#{source_link(file)})" }.join("\n") + "\n"
  end

  def pages
    readme = read_source("README.md")
    changelog = read_source("CHANGELOG.md")
    version = changelog_version(changelog)
    pkg = package_json
    commands = command_rows(pkg)

    {
      docs_index: <<~MD,
        # Overview

        These docs are for software developers who want to fork, inspect, extend, package, or contribute to ASCII VJ Remix.

        ASCII VJ Remix is a local-first desktop visualizer and renderer workbench. For users, it exists to give DJs a manageable visualizer and VJs fine-grained ASCII/video filter control. For developers, it is a Tauri desktop application with a dense renderer/control surface, native output path, local media adapters, audio-reactive modulation, and release/update infrastructure.

        The public homepage is written for DJs and VJs. This section is intentionally technical: it describes the app's source model, renderer architecture, desktop packaging boundary, security posture, performance constraints, accessibility expectations, internationalization posture, release workflow, and current #{version} feature baseline.

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

        #{source_note(SOURCE_FILES.values)}
      MD
      overview_index: <<~MD,
        # Overview

        ASCII VJ Remix is a local-first desktop visualizer and renderer workbench. For users, it exists to give DJs a manageable visualizer and VJs fine-grained ASCII/video filter control. For developers, it is a Tauri desktop application with a dense renderer/control surface, native output path, local media adapters, audio-reactive modulation, and release/update infrastructure.

        ## Overview Pages

        - [ASCII VJ Remix](/docs/overview/ascii-vj-remix/) — scope, lineage, release baseline, platform requirements, and project boundary.
        - [Feature Set](/docs/overview/features/) — comprehensive map of sources, rendering, presets, live controls, audio reactivity, Pop Out, packaging, security, and advanced paths.
        - [Release Baseline](/docs/overview/changelog-baseline/) — current release line and recent behavior changes from the changelog.
      MD
      product_overview: <<~MD,
        # ASCII VJ Remix

        ASCII VJ Remix is a local-first native desktop renderer lab for turning images, videos, cameras, and audio-reactive signals into high-performance ASCII and cell-based visuals.

        It is built for VJ-style experimentation: pick a source, choose or build a preset, push the renderer hard, pop output onto another display, and keep tuning the look live while media keeps running.

        Current source docs describe the **#{version}** feature set.

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

        #{source_note(["README.md", "CHANGELOG.md"])}
      MD
      features: <<~MD,
        # Feature Set

        This page describes the current ASCII VJ Remix feature baseline for developers planning forks, ports, integrations, or feature work.

        ## Source Inputs

        - Local image files.
        - Local video files.
        - MKV file selection where the active platform decoder path can handle playback.
        - Camera/webcam input.
        - Multiple simultaneous cameras when the OS and runtime allow concurrent capture.
        - Camera mixer layouts: grid, split row, stack, and picture-in-picture.
        - Camera controls for device selection, capture size, FPS, layout, framing, and mirror.
        - Audio analysis inputs: mic/input, local audio files, and system/display audio where the OS exposes it to the desktop app.

        Selected media and camera frames stay local. The renderer receives playable media URLs or session-local registered ids; it does not receive broad filesystem access.

        ## Rendering Backends

        - WebGPU is the primary quality target on capable desktop runtimes.
        - WebGL2 is the main embedded GPU fallback.
        - Canvas2D remains the compatibility path for traditional glyph-style ASCII output.
        - Pixel Canvas remains available as a compatibility fallback.
        - Native Tauri Pop Out uses a `wgpu` presenter where available:
          - Metal on macOS.
          - D3D12 on Windows.
          - Vulkan/GLES on Linux.
        - Native Pop Out preserves glyph mode and character-set parameters for traditional ASCII presets instead of flattening them into solid cells.

        ## Live Renderer Controls

        The app keeps source selection, presets, WTF mode, audio modulation, native output, and future MIDI work routed through one canonical parameter model.

        Major control groups include:

        - Source mode, media id/URL, media type, and source name.
        - Camera device ids, resolution, FPS, layout, framing, and mirror.
        - Backend selection: auto, WebGPU, WebGL2, Canvas2D, Pixel Canvas.
        - Grid: columns, rows, auto rows, cell dimensions, and aspect correction.
        - Color: saturation, contrast, brightness, gamma, background blend, and quantization.
        - Sampling: FPS, jitter amount, jitter speed, sample position, and smoothing.
        - Glyph/cell behavior: glyph mode, solid mode, compact character set, font family menu, and minimum glyph intensity.
        - UI/performance: stats overlay and transition timing.

        Static renderer-family transitions keep media ownership at the shared runtime layer. Canvas2D, pixel Canvas, WebGL, and WebGPU renderers can crossfade over the same live source instead of destroying and reloading media when backend, glyph, or solid-cell behavior changes.

        ## Presets

        ASCII VJ Remix includes read-only built-in visual presets and user-managed presets.

        Built-in visual families include extreme looks such as Neon Sledgehammer, Gamma Sinkhole, Chrome Wound, Candy Fragmenter, Paper Shredder, Cyberdelic Riot, Acid Snowstorm, Terminal Collapse, and Neon Razorstorm.

        Traditional ASCII presets include Classic Camera ASCII, ANSI Newsprint, Terminal Mono, and Dense Typewriter.

        User presets can be saved, duplicated, updated, deleted, imported, and exported. Presets preserve the active media source unless the user explicitly changes it.

        ## Transitions and WTF Mode

        - Preset transitions crossfade instead of fading to black.
        - Transition time is configurable.
        - Static video/camera transitions can move between GPU, solid/pixel, and Canvas2D glyph renderers while keeping playback live.
        - WTF mode continuously transitions through randomized live-safe settings.
        - WTF mode can anchor randomization around both extreme preset families and traditional ASCII presets.
        - Safe clamps avoid pure black or pure white output during random or audio-driven states.

        ## Audio Reactivity

        Audio reactivity is enabled by default and starts from Mic/Input by default.

        It analyzes bounded features rather than raw audio buffers:

        - RMS.
        - Bass.
        - Low-mid.
        - Mid.
        - High-mid.
        - Treble.
        - Presence.
        - Brightness.
        - Density.
        - Transient energy and flux.
        - Beat pulse.
        - Spectral movement.

        Dense-mix dampening and noise-floor controls help busy tracks stay reactive without pinning jitter and beat response at maximum. Audio modulation affects live effective render params without rewriting saved presets.

        ## Pop Out and External Displays

        Pop Out creates a separate output window for a projector, capture card, or secondary display. The main control window remains available for live tuning.

        The output window is presentation-focused and has a minimal command surface. When Tauri can enumerate displays, output display selection is persisted.

        ## Packaging and Updates

        - Built with Tauri v2.
        - Production runtime is local-only by default.
        - GitHub Releases updater infrastructure is configured.
        - Public macOS release CI requires Developer ID signed and notarized artifacts.
        - Windows 0.9.3 artifacts are explicitly unsigned preview builds.
        - Crash report submission is production-only, reviewed/sanitized, and routed through the Rust desktop layer to the Cloudflare Worker relay.

        ## Advanced Paths

        - Legacy ASCILINE stream work and newer Rust/FFmpeg stream sessions exist but are hidden from the normal Source UI.
        - FFmpeg sidecar policy and codec support live in contributor/release work.
        - MIDI hardware control is planned, with an Evolution/M-Audio UC33e through iConnectivity mioXC named as the first validation target.

        #{source_note(["README.md", "docs/RENDERING_ENGINE.md", "CHANGELOG.md"])}
      MD
      release_baseline: <<~MD,
        # Release Baseline

        Current docs describe the **#{version}** feature set.

        ## 0.9.3 Highlights

        - Public macOS release builds require Developer ID signing and notarization.
        - Windows release artifacts are published as unsigned previews until a signing backend is proven.
        - Audio reactivity has shared defaults, control metadata, presets, feature normalization, dense-mix dampening, and render-parameter modulation.
        - New audio-reactive controls cover transient/flux amount, presence amount, density dampening, and noise floor.
        - Flux and density meters are available alongside a Dense Mix Control audio-reactive preset.
        - Browser preview, Pop Out, stream paths, and native output consume shared audio-reactive modulation rules.
        - Static video/camera transitions crossfade between renderer families without destroying the shared media source.
        - Traditional Canvas2D ASCII presets default to visible static-image jitter.

        ## Security Baseline

        - Future Windows signing uses environment-scoped signing credentials and does not commit certificate files, client secrets, or private signing material.
        - Audio reactivity sends bounded feature vectors through IPC; raw audio, frames, media files, and paths remain local.
        - Release signing and updater signing checks treat macOS public distribution as fail-closed.

        ## Validation Baseline

        The changelog records checks for audio reactivity, Windows Authenticode preparation, desktop/release gates, camera Pop Out behavior, native glyph masking, live renderer transitions, WTF mode, traditional ASCII jitter, and Tauri policy permissions.

        #{source_note(["CHANGELOG.md"])}
      MD
      development_index: <<~MD,
        # Development

        Development docs cover how to work on the app without breaking its local-first desktop product boundary.

        ## Development Pages

        - [Quickstart](/docs/development/quickstart/) — local setup, install, build, and verification commands.
        - [Architecture](/docs/development/architecture/) — ownership map, product boundary, and desktop/runtime architecture.
        - [Rendering Engine](/docs/development/rendering-engine/) — source flow, backend selection, params, audio modulation, Pop Out, and stream paths.
        - [Contributing](/docs/development/contributing/) — contribution workflow, release/updater notes, and FFmpeg sidecar policy.
        - [Agent Guide](/docs/development/agent-guide/) — context-loading and safety guidance for LLM coding agents.
      MD
      quickstart: <<~MD,
        # Quickstart

        ## Prerequisites

        Use the source repository as the working tree:

        ```bash
        git clone https://github.com/aindaco1/ascii-vj-remix.git
        cd ascii-vj-remix
        ```

        Install JavaScript dependencies:

        ```bash
        npm install
        ```

        For desktop work, install the Tauri prerequisites for the target OS. Linux development also needs the WebKitGTK/WebView stack required by Tauri v2.

        ## Common Local Commands

        #{commands.empty? ? "| Command | Purpose |\n| --- | --- |\n| `npm run dev` | Start the development server when defined by the source repo. |\n| `npm run build` | Build the frontend when defined by the source repo. |" : "| Command | Source script |\n| --- | --- |\n" + commands.join("\n")}

        ## First Verification Path

        1. Install dependencies with `npm install`.
        2. Run the source repo's focused checks before changing behavior.
        3. For renderer changes, inspect [Rendering Engine](/docs/development/rendering-engine/) and run renderer-specific checks from [Commands](/docs/reference/commands/).
        4. For desktop packaging or permissions changes, inspect Tauri config, capabilities, macOS plist/entitlements, and release notes.
        5. For user-facing controls, check accessibility and i18n expectations before shipping copy or UI changes.

        ## Development Boundary

        Do not add hosted fonts, CDNs, online decoders, telemetry, or hosted runtime dependencies. Runtime assets should remain bundled locally, and selected user media should stay local.

        #{source_note(["README.md", "docs/CONTRIBUTORS.md", "docs/AGENTS.md"])}
      MD
      architecture: <<~MD,
        # Architecture

        ## Product Shape

        ASCII VJ Remix is a Tauri v2 desktop app with a vanilla/Vite renderer UI, GPU/Canvas rendering paths, native output work, and local media/audio adapters.

        The app should be understood as a desktop performer tool, not a hosted SaaS app. Browser mode helps development and portability, but the packaged desktop app is the product.

        ## High-Level Flow

        ```text
        source selection
          -> source adapter
          -> canonical params
          -> optional live modulation
          -> effective params
          -> renderer runtime
          -> main preview
          -> optional native/browser Pop Out
        ```

        ## Ownership Map

        | Area | Primary source locations |
        | --- | --- |
        | Main UI, params, presets, source controls, WTF, audio UI | `app.js`, `index.html`, `style.css` |
        | GPU renderer and media source abstraction | `renderers/gpu/` |
        | Tauri adapter and output-display helpers | `renderers/desktop/` |
        | Tauri shell, commands, permissions, updater, native audio, native output | `src-tauri/` |
        | Native Pop Out renderer | `src-tauri/src/native_output.rs`, `src-tauri/src/native_output/gpu.rs` |
        | macOS native camera latency path | `src-tauri/src/native_output/native_camera.rs` |
        | Rust media engine and FFmpeg sessions | `src-tauri/src/media_engine/` |
        | Build, smoke, release, Podman, FFmpeg scripts | `scripts/` |
        | User/developer docs | `docs/`, `README.md`, `CHANGELOG.md` |

        ## Non-negotiable Constraints

        - Preserve the app name and native desktop direction.
        - Keep normal runtime local-first and offline by default.
        - Keep renderer quality high; WebGPU/WebGL output is the visual quality target.
        - Preserve fallback paths unless a replacement is implemented and tested.
        - Treat Pop Out performance and latency as critical user-facing behavior.
        - Keep selected local media local.
        - Keep stats overlay user-owned.
        - Keep stream infrastructure hidden until the stream workflow is productized end to end.
        - Do not reduce the control density of the VJ surface when restyling.

        #{source_note(["docs/AGENTS.md", "docs/RENDERING_ENGINE.md", "README.md"])}
      MD
      rendering_engine: copied_page("Rendering Engine", "docs/RENDERING_ENGINE.md", "Development", 3),
      contributing: copied_page("Contributing", "docs/CONTRIBUTORS.md", "Development", 4),
      agent_guide: copied_page("Agent Guide", "docs/AGENTS.md", "Development", 5),
      operations_index: <<~MD,
        # Operations

        Operations docs cover the practices that keep forks reliable: local media boundaries, desktop permissions, renderer performance, release gates, accessibility, and internationalization.

        ## Operations Pages

        - [Security](/docs/operations/security/) — local media, Tauri capability, updater, crash relay, and FFmpeg sidecar boundaries.
        - [Performance](/docs/operations/performance/) — output latency, FPS validation, Pop Out, camera, and renderer budgets.
        - [Testing](/docs/operations/testing/) — source-derived test matrix and release validation.
        - [Accessibility](/docs/operations/accessibility/) — dense control-surface accessibility expectations.
        - [Internationalization](/docs/operations/internationalization/) — copy, locale, and fallback rules.
        - [Release and Updates](/docs/operations/release/) — signing, notarization, updater, Windows preview posture, and crash reporting.
      MD
      security: copied_page("Security", "docs/SECURITY.md", "Operations", 1),
      performance: copied_page("Performance", "docs/PERFORMANCE.md", "Operations", 2),
      testing: copied_page("Testing", "docs/TESTING.md", "Operations", 3),
      accessibility: copied_page("Accessibility", "docs/ACCESSIBILITY.md", "Operations", 4),
      internationalization: copied_page("Internationalization", "docs/I18N.md", "Operations", 5),
      release: <<~MD,
        # Release and Updates

        ## Current Release Posture

        - Current source docs describe the **#{version}** feature set.
        - macOS public release builds require Developer ID signing and notarization.
        - Windows 0.9.3 artifacts are unsigned previews until SignPath Foundation, Azure Artifact Signing, or another signing backend is proven.
        - GitHub Releases updater infrastructure is configured.
        - Updater and release checks must not broaden runtime network capability.

        ## macOS

        Public release CI treats macOS signing/notarization as fail-closed. Local or test builds may still require the normal macOS right-click Open or Open Anyway flow.

        ## Windows

        Windows signing tooling exists for future signed release work, including Azure Artifact Signing, Tauri `signCommand`, and Authenticode verification helpers. The active 0.9.3 release posture remains unsigned preview artifacts.

        ## Crash Reporting

        Production crash reporting is reviewed/sanitized and routed through the Rust desktop layer to the Cloudflare Worker relay at `https://crash.dustwave.xyz`. The webview does not get arbitrary HTTP capability. Reports are bounded and sanitized: media files, frames, raw audio, full paths, tokens, cookies, and private environment values are not included.

        ## Release Validation

        Release checks include desktop checks, renderer math, audio-reactive helper tests, crash relay tests, Tauri policy checks, and signing/updater verification appropriate to each platform.

        #{source_note(["README.md", "CHANGELOG.md", "docs/CONTRIBUTORS.md", "docs/SECURITY.md"])}
      MD
      reference_index: <<~MD,
        # Reference

        Reference pages preserve source-derived command, roadmap, changelog, and source-map material for developers maintaining forks.

        - [Commands](/docs/reference/commands/)
        - [Roadmap](/docs/reference/roadmap/)
        - [Changelog](/docs/reference/changelog/)
        - [Source Map](/docs/reference/source-map/)
      MD
      commands: <<~MD,
        # Commands

        Commands are read from `package.json` when available. Use source scripts as the authority; these docs are regenerated by `scripts/sync_ascii_docs.rb`.

        #{commands.empty? ? "No matching npm scripts were found in package.json." : "| Command | Source script |\n| --- | --- |\n" + commands.join("\n")}

        ## Command Guidance

        - Use focused checks before broad release gates while developing.
        - Run renderer checks after changing shared math, presets, backend behavior, source adapters, transitions, audio modulation, or Pop Out behavior.
        - Run desktop/release checks after changing Tauri capabilities, updater config, signing, crash reporting, native output, or platform packaging.
        - Keep secrets and signing material out of committed source.

        #{source_note(["package.json", "docs/CONTRIBUTORS.md", "docs/TESTING.md", "CHANGELOG.md"])}
      MD
      roadmap: copied_page("Roadmap", "docs/ROADMAP.md", "Reference", 2),
      changelog: copied_page("Changelog", "CHANGELOG.md", "Reference", 3),
      source_map: <<~MD
        # Source Map

        The sync script uses the following source files from the ASCII VJ Remix repository.

        | Source | Destination / use |
        | --- | --- |
        | `README.md` | Product scope, feature set, requirements, packaging, support/contact, and developer entry point. |
        | `CHANGELOG.md` | Current release baseline, recent behavior changes, security notes, and validation expectations. |
        | `docs/RENDERING_ENGINE.md` | Source flow, parameter model, renderer backends, effective params, Pop Out, audio, and stream paths. |
        | `docs/CONTRIBUTORS.md` | Setup, contribution workflow, release/updater notes, FFmpeg sidecar policy. |
        | `docs/AGENTS.md` | Agent context-loading order, constraints, ownership map, and safe-working guidance. |
        | `docs/SECURITY.md` | Local-first boundary, Tauri capabilities, crash reporting, updater, media, and secrets handling. |
        | `docs/PERFORMANCE.md` | Renderer/output latency, camera, FPS, and performance validation. |
        | `docs/TESTING.md` | Source-derived verification matrix. |
        | `docs/ACCESSIBILITY.md` | Control-surface accessibility rules. |
        | `docs/I18N.md` | Internationalization and localization expectations. |
        | `docs/ROADMAP.md` | Planned, deferred, and current direction. |
        | `package.json` | NPM command reference. |

        ## Regenerate Docs

        ```bash
        ruby scripts/sync_ascii_docs.rb
        ```

        ## Rebuild Spanish Docs

        ```bash
        python3 scripts/build_spanish_docs.py
        ```
      MD
    }
  end

  def copied_page(title, source, parent, nav_order)
    content = read_source(source)
    content = content.sub(/\A#\s+.*\n+/, "# #{title}\n\n")
    content = normalize_roadmap_version(content) if source == "docs/ROADMAP.md"
    content = rewrite_links(content, source)
    content + source_note([source])
  end

  def normalize_roadmap_version(content)
    content.gsub("current 0.9.0 feature baseline", "current 0.9.3 feature baseline")
           .gsub("Current Feature Baseline: 0.9.0", "Current Feature Baseline: 0.9.3")
  end

  def rewrite_links(content, current_src)
    content.gsub(/\]\(([^)]+)\)/) do |match|
      target = Regexp.last_match(1)
      next match if target.start_with?("http://", "https://", "mailto:", "#")
      path, suffix = target.split(/(?=[?#])/, 2)
      suffix ||= ""
      current_dir = Pathname(current_src).dirname
      normalized = current_dir.join(path).cleanpath.to_s.sub(%r{\A\./}, "")
      replacement = ALIASES[normalized] || (SOURCE_ROOT.join(normalized).exist? ? source_link(normalized) : target)
      match.sub("(#{target})", "(#{replacement}#{suffix})")
    end
  end

  def run
    raise "Source repo not found: #{SOURCE_ROOT}" unless SOURCE_ROOT.directory?
    SOURCE_FILES.each_value { |file| read_source(file) }
    ROOT.join("docs").rmtree if ROOT.join("docs").directory?
    DOCS.each do |path, title, parent, nav_order, key|
      write_page(path, title, parent, nav_order, pages.fetch(key))
    end
    puts "Synced #{DOCS.length} docs pages from #{SOURCE_ROOT}"
  end
end

SyncAsciiDocs.run
