# Source ingestion notes

These are dated records. See [Site Maintenance](README.md) for the current
refresh procedure and [Source Map](../reference/source-map.md) for guide ownership.

Generated with the `product-marketing-docs-builder` operating pattern.

## Sources read

- ASCII VJ Remix: README, CHANGELOG, AGENTS, SECURITY, PERFORMANCE, ACCESSIBILITY, I18N, TESTING, CONTRIBUTORS, RENDERING_ENGINE, package scripts, Tauri config, Cargo manifest, style.css, demo assets, and the approved canonical app icon.
- Architecture reference: pool-marketing-docs Jekyll/just-the-docs layout, Sass, includes, Gemfile, GitHub Pages workflow, docs taxonomy.

## Style extraction

- ASCII VJ Remix: dark background `#040506`, panels `#090a0c` / `#101216`, cyan `#00e5ff`, pink `#ff2bd6`, white text, VCR OSD Mono, square controls, console/control-surface density.

## 1.0.3 refresh

- Verified the published [v1.0.3 release](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.3) and its macOS, Windows, Linux, and updater assets on 2026-09-05.
- The source changelog entry is dated 2026-09-02; GitHub publication occurred on 2026-09-05 UTC. `_data/product.yml` retains the changelog date used by the sync pipeline.
- Read the source [1.0.3 acceptance record](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.0.3.md) alongside the durable guides. Windows development-candidate hardware acceptance is recorded; Ubuntu/Fedora camera hardware testing remains deferred.
- Checked the source preset backend contract (71 total, 43 accelerated, 28 Canvas) and README palette catalog (17 palettes). Refreshed both homepages and the English/Spanish documentation, including 1.0.1 playlists, PNG capture, and manual diagnostics and the 1.0.2 output-worker fixes.
- Preserved the existing artwork, video, layout, and shared support/download components.

## Claims policy

This site only makes claims supported by ASCII VJ Remix source docs/config/scripts. It does not claim signed Windows artifacts or completed release builds beyond source repo documentation.

The mother repository owns technical truth. The marketing repository owns the
curated public narrative, generated presentation, localization, and deployment;
its sync script copies canonical sections and the approved icon rather than
maintaining parallel technical descriptions.

## 2026-09-06 documentation consolidation

- Read the clean mother checkout at `0d19eac669752b3661bafe07b156ad083effc9e9`
  (`docs: consolidate guides and organize release records`) and its maintained
  documentation index, user, contributor, release, agent, testing, and renderer
  guides. This records the local source snapshot, not a new publication check.
- Updated feature/requirement imports to `docs/USER_GUIDE.md` and release
  procedures to `docs/RELEASING.md`; historical release links now resolve under
  `docs/releases/`. Release metadata remains on the dated 1.0.3 changelog entry.
- Consolidated website procedures in this directory, retained existing public
  routes, and reduced Quickstart to canonical setup plus links to check selection
  and the full command reference.
