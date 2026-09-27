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


## 2026-09-27 developer documentation refresh

- Compared the previous `0d19eac669752b3661bafe07b156ad083effc9e9` ingestion
  with fetched `origin/main` at `8dc3a0553145d18da1c82f4c3baf60b9d3d85584`.
  The source checkout matched that commit before the documentation corrections below.
- Verified GitHub's latest public release is [v1.0.6](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.0.6),
  published September 25, 2026 at 11:50 UTC, with 14 assets covering macOS,
  Windows, Linux and the updater. The tag resolves to
  `55545b67c4376f190fcc6f89ab57f6e12d65eb87`. This is publication evidence;
  installers, updater transactions and physical hardware were not retested here.
- Reviewed the 1.0.4 color-cycling implementation, shared palette/preset contracts,
  renderer resource reuse and native presentation checks; the 1.0.5 macOS floor,
  static-image recovery, selected Podman engine and license-provenance changes;
  and the Jev development commands and shared desktop migration in 1.0.6.
- Checked the live source exports: 21 palettes and 79 presets, with 51 eligible
  for acceleration and 28 explicitly using Canvas. Corrected the upstream User
  Guide's old palette count and labeled the earlier 71-preset performance sweep
  as historical instead of turning it into new acceptance evidence.
- Corrected the upstream README's old package version and Testing's old Platform
  pin/rollback description. Exact current pins stay in `platform-desktop.json`.
  Documented the existing Jev `testCoreVersion` metadata mismatch without changing
  the evaluator or running hosted evaluation.
- Grouped the later Record relay adapter and compatible Desktop Core 0.2.0 pin
  under 1.0.6 shared-service maintenance, as requested. The shared dependency diff
  changes relay issue markers and grouping initialization; the desktop updater
  helpers are unchanged. The published desktop tag/installers are unchanged.
- Added Shared Desktop Services through the existing importer, refreshed English
  and Spanish guides and commands, and updated the shared release metadata plus
  factual homepage counts/summary. Canonical documentation corrections are
  committed upstream at `caefa8ec9708ff782af9a6a1a4b7946a8953046c` for reproducible source refreshes.
- Removed the stale, untracked `es/docs/operations/release 2.md` iCloud copy at
  the user’s request; checked both repositories for additional source/document
  conflict copies and found none.
- Validation: all 10 documentation-pipeline tests, the production Jekyll build,
  current-state audit, internal-link audit (52 HTML pages), SEO audit, support
  audit, and performance audit passed. Re-running both generators produced
  identical files. `git diff --check` passed in both repositories, and changed
  upstream documentation paths resolve locally.
- Visually reviewed the generated Shared Desktop Services page in English and
  Spanish and verified the language switch. These checks preceded publication.
  The website deployment is tracked by the Pages workflow for the publishing
  commit; this documentation refresh does not rebuild the desktop release or
  deploy the relay.
