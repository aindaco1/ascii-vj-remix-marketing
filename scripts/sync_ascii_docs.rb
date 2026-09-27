#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "digest"
require "pathname"
require "json"

ROOT = Pathname(__dir__).join("..").expand_path
SOURCE_ROOT = Pathname(ENV.fetch("ASCII_VJ_SOURCE", ROOT.join("../ascii-vj-remix").to_s)).expand_path
SOURCE_REPO = ENV.fetch("ASCII_VJ_REPO", "aindaco1/ascii-vj-remix")
BLOB_BASE = "https://github.com/#{SOURCE_REPO}/blob/main/"
TREE_BASE = "https://github.com/#{SOURCE_REPO}/tree/main/"
ICON_SOURCE = "src-tauri/icons/icon.png"
ICON_DESTINATION = "assets/images/ascii-vj-remix-app-icon.png"

SOURCE_FILES = {
  readme: "README.md",
  index: "docs/README.md",
  user_guide: "docs/USER_GUIDE.md",
  releasing: "docs/RELEASING.md",
  release_records: "docs/releases/README.md",
  changelog: "CHANGELOG.md",
  rendering: "docs/RENDERING_ENGINE.md",
  contributors: "docs/CONTRIBUTORS.md",
  shared_desktop: "docs/SHARED_DESKTOP_MIGRATION.md",
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
  ["docs/development/shared-desktop-services.md", "Shared Desktop Services", "Development", 6, :shared_desktop],
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
  "docs/SHARED_DESKTOP_MIGRATION.md" => "/docs/development/shared-desktop-services/",
  "docs/AGENTS.md" => "/docs/development/agent-guide/",
  "docs/SECURITY.md" => "/docs/operations/security/",
  "docs/PERFORMANCE.md" => "/docs/operations/performance/",
  "docs/TESTING.md" => "/docs/operations/testing/",
  "docs/ACCESSIBILITY.md" => "/docs/operations/accessibility/",
  "docs/I18N.md" => "/docs/operations/internationalization/",
  "docs/RELEASING.md" => "/docs/operations/release/",
  "docs/ROADMAP.md" => "/docs/reference/roadmap/"
}.freeze

# These guides are excerpted across pages. Only mirrored sections get local
# links; other anchors keep pointing to the complete upstream guide.
SECTION_ALIASES = {
  "README.md#what-this-project-is" => "/docs/overview/ascii-vj-remix/#what-this-project-is",
  "README.md#current-capabilities" => "/docs/overview/features/#current-capabilities",
  "docs/USER_GUIDE.md#current-capabilities" => "/docs/overview/features/#current-capabilities",
  "docs/USER_GUIDE.md#system-requirements" => "/docs/overview/ascii-vj-remix/#system-requirements",
  "docs/USER_GUIDE.md#hardware-guidance" => "/docs/overview/ascii-vj-remix/#hardware-guidance",
  "docs/USER_GUIDE.md#battery-and-heat-warning" => "/docs/overview/ascii-vj-remix/#battery-and-heat-warning"
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

  def released_version(markdown)
    markdown[/^##\s+\[([^\]]+)\]\s+-\s+\d{4}-\d{2}-\d{2}\s*$/, 1] ||
      raise("No dated release found in CHANGELOG.md")
  end

  def released_date(markdown, version)
    markdown[/^##\s+\[#{Regexp.escape(version)}\]\s+-\s+(\d{4}-\d{2}-\d{2})\s*$/, 1] || ""
  end

  def released_body(markdown, version)
    escaped = Regexp.escape(version)
    match = markdown.match(/^##\s+\[#{escaped}\]\s+-\s+\d{4}-\d{2}-\d{2}\s*\n(?<body>[\s\S]*?)(?=^##\s+|\z)/)
    raise "Missing release notes for #{version}" unless match

    match[:body].strip
  end

  def source_sections(source, headings)
    markdown = read_source(source)
    headings.map do |heading|
      body = section(markdown, heading)
      raise "Missing section #{heading.inspect} in #{source}" if body.empty?

      "## #{heading}\n\n#{rewrite_links(body, source, excerpt: true)}"
    end.join("\n\n")
  end

  def sync_app_icon
    source = SOURCE_ROOT.join(ICON_SOURCE)
    raise "Missing source icon: #{source}" unless source.file?

    destination = ROOT.join(ICON_DESTINATION)
    destination.dirname.mkpath
    FileUtils.cp(source, destination)
    Digest::SHA256.file(destination).hexdigest
  end

  def command_rows(package_json)
    JSON.parse(package_json).fetch("scripts").map do |name, value|
      public_value = value.gsub(%r{media/point-click-test(?:-30s)?\.mp4}, "media/<bundled-test-fixture>.mp4")
      "| `npm run #{name}` | `#{public_value.gsub('|', '\\|')}` |"
    end
  end

  def package_json
    read_source("package.json")
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
    changelog = read_source("CHANGELOG.md")
    version = released_version(changelog)
    pkg = package_json
    commands = command_rows(pkg)

    {
      docs_index: <<~MD,
        # Overview

        These docs are for software developers who want to fork, inspect, extend, package, or contribute to ASCII VJ Remix.

        ASCII VJ Remix is a local-first desktop visualizer and renderer workbench. For users, it exists to give DJs a manageable visualizer and VJs fine-grained ASCII/video filter control. For developers, it is a Tauri desktop application with a dense renderer/control surface, native output path, local media adapters, audio-reactive modulation, and release/update infrastructure.

        These guides follow merged changes on the mother repository's `main` branch. The [Release Baseline](/docs/overview/changelog-baseline/) identifies the latest dated release, **#{version}**. Changes after that release are labeled separately; source, CI, desktop publication, relay deployment, and hardware acceptance are distinct.

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
      product_overview: <<~MD,
        # ASCII VJ Remix

        These sections follow the mother repository's `main` branch. See the [Release Baseline](/docs/overview/changelog-baseline/) for **#{version}** release notes. Product identity, requirements, and hardware guidance are selected directly from their canonical guides.

        #{source_sections("README.md", ["What This Project Is"])}

        #{source_sections("docs/USER_GUIDE.md", ["System Requirements", "Hardware Guidance", "Battery and Heat Warning"])}

        For installation, permissions, privacy, and troubleshooting, use the complete [User Guide](#{source_link("docs/USER_GUIDE.md")}).

        #{source_note(["README.md", "docs/USER_GUIDE.md", "CHANGELOG.md"])}
      MD
      features: <<~MD,
        # Feature Set

        This page describes the current ASCII VJ Remix feature baseline for developers planning forks, ports, integrations, or feature work. The capability map is generated from the mother repository's User Guide.

        #{source_sections("docs/USER_GUIDE.md", ["Current Capabilities"])}

        #{source_note(["docs/USER_GUIDE.md"])}
      MD
      release_baseline: <<~MD,
        # Release Baseline

        The latest dated changelog entry is **#{version}**. This page excludes Unreleased entries; the [Changelog](/docs/reference/changelog/) retains them when present. Other developer guides follow merged `main`, which can include changes after the published desktop tag.

        [Download v#{version} and read its publication and platform-validation notes](https://github.com/#{SOURCE_REPO}/releases/tag/v#{version}). The changelog date records the source release entry; GitHub Releases records when the downloads were published.

        For the release's shared-service maintenance context, see [Shared Desktop Services](/docs/development/shared-desktop-services/). That guide distinguishes later relay/dependency changes from the published desktop artifacts.

        ## #{version} Release Notes

        #{rewrite_links(released_body(changelog, version), "CHANGELOG.md")}

        #{source_note(["CHANGELOG.md"])}
      MD
      development_index: <<~MD,
        # Development

        Development docs cover how to work on the app without breaking its local-first desktop product boundary.

        ## Development Pages

        - [Quickstart](/docs/development/quickstart/) — local setup, install, build, and verification commands.
        - [Architecture](/docs/development/architecture/) — ownership map, product boundary, and desktop/runtime architecture.
        - [Rendering Engine](/docs/development/rendering-engine/) — source flow, backend selection, params, audio modulation, Pop Out, and stream paths.
        - [Contributing](/docs/development/contributing/) — local development, app identity, contribution workflow, FFmpeg, and Podman.
        - [Agent Guide](/docs/development/agent-guide/) — context-loading and safety guidance for LLM coding agents.
        - [Shared Desktop Services](/docs/development/shared-desktop-services/) — pinned Platform dependencies, updater/relay ownership, validation, and rollback.
        - [Release and Updates](/docs/operations/release/) — packaging, signing, publication, and artifact acceptance.
      MD
      quickstart: <<~MD,
        # Quickstart

        Use the source repository as the working tree:

        ```bash
        git clone https://github.com/aindaco1/ascii-vj-remix.git
        cd ascii-vj-remix
        ```

        #{source_sections("docs/CONTRIBUTORS.md", ["Prerequisites", "First-Time Setup"])}

        ## First Verification Path

        Choose the [recommended check set](/docs/operations/testing/#recommended-check-sets) for the change. Use [Contributing](/docs/development/contributing/) for development identity, local signing, FFmpeg, and Podman, and [Commands](/docs/reference/commands/) for the complete npm script catalog.

        For packaging, signing, publication, or updater work, follow [Release and Updates](/docs/operations/release/).

        ## Development Boundary

        Do not add hosted fonts, CDNs, online decoders, telemetry, or hosted runtime dependencies. Keep runtime assets bundled locally and selected user media local.

        #{source_note(["docs/CONTRIBUTORS.md", "docs/TESTING.md", "docs/RELEASING.md"])}
      MD
      architecture: <<~MD,
        # Architecture

        This page assembles the architecture contract from the mother repository's agent and rendering guides instead of maintaining a parallel ownership model here.

        #{source_sections("docs/AGENTS.md", ["Project Identity"])}

        #{source_sections("docs/RENDERING_ENGINE.md", ["Architecture Properties", "High-Level Data Flow", "Parameter Model"])}

        #{source_sections("docs/AGENTS.md", ["Repository Ownership Map", "Non-Negotiable Constraints", "Behavior and Ownership Constraints"])}

        #{source_note(["docs/AGENTS.md", "docs/RENDERING_ENGINE.md"])}
      MD
      rendering_engine: copied_page("Rendering Engine", "docs/RENDERING_ENGINE.md", "Development", 3),
      contributing: copied_page("Contributing", "docs/CONTRIBUTORS.md", "Development", 4),
      agent_guide: copied_page("Agent Guide", "docs/AGENTS.md", "Development", 5),
      shared_desktop: copied_page("Shared Desktop Services", "docs/SHARED_DESKTOP_MIGRATION.md", "Development", 6),
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
      release: copied_page("Release and Updates", "docs/RELEASING.md", "Operations", 6),
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

        Commands are read from the complete `package.json` scripts object. Use source scripts as the authority; these docs are regenerated by `scripts/sync_ascii_docs.rb`.

        Bundled media fixture paths are generalized in this public reference. Use `package.json` when inspecting the exact script implementation.

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
        | `README.md` | Product scope and lineage; upstream installation and first-run entry point. |
        | `docs/README.md` | Upstream documentation ownership and navigation. |
        | `docs/USER_GUIDE.md` | Detailed feature set, system requirements, hardware, and thermal guidance. Full usage, permissions, and troubleshooting remain linked upstream. |
        | `CHANGELOG.md` | Current release baseline, recent behavior changes, security notes, and validation expectations. |
        | `docs/RENDERING_ENGINE.md` | Source flow, parameter model, renderer backends, effective params, Pop Out, audio, and stream paths. |
        | `docs/CONTRIBUTORS.md` | Quickstart, local app identity, contribution workflow, FFmpeg, and Podman. |
        | `docs/SHARED_DESKTOP_MIGRATION.md` | Shared Desktop Services: package ownership, validation, rollback, and post-release source changes. Exact pins remain in the linked `platform-desktop.json`. |
        | `docs/RELEASING.md` | Reusable packaging, signing, publication, updater, and artifact acceptance procedure. |
        | `docs/releases/README.md` | Linked index of historical release records; not current procedure or live acceptance status. |
        | `docs/AGENTS.md` | Agent context-loading order, constraints, ownership map, and safe-working guidance. |
        | `docs/SECURITY.md` | Local-first boundary, Tauri capabilities, crash reporting, updater, media, and secrets handling. |
        | `docs/PERFORMANCE.md` | Renderer/output latency, camera, FPS, and performance validation. |
        | `docs/TESTING.md` | Source-derived verification matrix. |
        | `docs/ACCESSIBILITY.md` | Control-surface accessibility rules. |
        | `docs/I18N.md` | Internationalization and localization expectations. |
        | `docs/ROADMAP.md` | Prospective direction only. |
        | `package.json` | NPM command reference. |
        | `src-tauri/icons/icon.png` | Approved canonical app icon copied into the marketing site. |

        ## Guide Ownership

        The [upstream documentation index](#{source_link("docs/README.md")}) owns the full guide map, including MIDI, character-preset credits, Linux VM QA, component docs, and benchmark evidence. These specialized guides remain linked to their canonical source files.

        [Release records](#{source_link("docs/releases/README.md")}) preserve dated decisions and evidence. Use [Release and Updates](/docs/operations/release/) for the current procedure, [Testing](/docs/operations/testing/) for verification, and [Roadmap](/docs/reference/roadmap/) for prospective work.

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
    content = rewrite_links(content, source)
    content + source_note([source])
  end

  def rewrite_links(content, current_src, excerpt: false)
    content.gsub(/\]\(([^)]+)\)/) do |match|
      target = Regexp.last_match(1)
      next match if target.match?(%r{\A(?:[a-z][a-z0-9+.-]*:|//)}i)
      if target.start_with?("#")
        next match unless excerpt

        replacement = SECTION_ALIASES["#{current_src}#{target}"] || "#{source_link(current_src)}#{target}"
        next match.sub("(#{target})", "(#{replacement})")
      end
      path, suffix = target.split(/(?=[?#])/, 2)
      suffix ||= ""
      current_dir = Pathname(current_src).dirname
      normalized = current_dir.join(path).cleanpath.to_s.sub(%r{\A\./}, "")
      section_target = SECTION_ALIASES["#{normalized}#{suffix}"]
      next match.sub("(#{target})", "(#{section_target})") if section_target

      # The overview only includes selected README sections.
      local_target = ALIASES[normalized] unless normalized == "README.md" && !suffix.empty?
      replacement = local_target || (SOURCE_ROOT.join(normalized).exist? ? source_link(normalized) : nil)
      raise "Unresolved source link #{target.inspect} in #{current_src}" unless replacement

      match.sub("(#{target})", "(#{replacement}#{suffix})")
    end
  end

  def run
    raise "Source repo not found: #{SOURCE_ROOT}" unless SOURCE_ROOT.directory?
    SOURCE_FILES.each_value { |file| read_source(file) }
    changelog = read_source("CHANGELOG.md")
    version = released_version(changelog)
    # Resolve every source section/link before mutating generated pages or data.
    generated_pages = pages
    icon_sha256 = sync_app_icon
    product_data = ROOT.join("_data/product.yml")
    product_data.dirname.mkpath
    product_data.write(<<~YAML)
      latest_release:
        version: #{version.inspect}
        date: #{released_date(changelog, version).inspect}
      app_icon:
        path: #{("/" + ICON_DESTINATION).inspect}
        sha256: #{icon_sha256.inspect}
    YAML
    DOCS.each do |path, title, parent, nav_order, key|
      write_page(path, title, parent, nav_order, generated_pages.fetch(key))
    end
    puts "Synced #{DOCS.length} docs pages from #{SOURCE_ROOT}"
  end
end

SyncAsciiDocs.run if $PROGRAM_NAME == __FILE__
