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

## 2026-09-29 — 1.1.0 Spatial ASCII refresh

- Read merged app source at `03b1b02f1643a67f657a3dcc6b2e4aa8585edf39`,
  including the maintained guides, changelog, preset/palette contracts and
  [1.1.0 release record](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.1.0.md).
- Verified the public [v1.1.0 release](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.1.0),
  published September 29 at 19:49 UTC, with fourteen assets. Its tag resolves to
  `19f9350a505c379cfc2302f484373dbd9467e25a`. Matched both homepages' generated
  macOS, Windows and Linux download targets against the published asset URLs.
- Corrected stale unpublished/local-build wording and interim 87/59/28 counts
  in the canonical app guides, repaired the local-validation anchor, and matched
  Linux install examples to published filenames. These documentation corrections
  are committed upstream at `14753ff`; source exports confirm 90 presets
  (62 accelerated, 28 Canvas) and 21 palettes.
- Refreshed both homepages for eleven new looks, optional spatial/fractal modes,
  Bright Output and audio/live-control fixes. Kept the current design and media
  at the owner's request. All built-ins start in Flat Media, spatial modes are
  opt-in, and Bright Output starts off while preserving saved choices.
- Extended the existing feature import to include Spatial visuals and trails;
  refreshed renderer, testing, performance, contributor, architecture, roadmap,
  changelog and command pages. Added reviewed translations for all 121 new
  Spanish segments, retaining app labels, code and source links.
- Validation: ten pipeline tests, production Jekyll build, current-state,
  52-page internal-link, SEO, support and performance audits passed. Both
  generators reproduced identical output. Changed upstream paths and release
  anchors resolve; maintenance records remain absent from public routes, search
  and sitemap. `git diff --check` passed in both repositories.
- Visually checked both release sections, language switching, the Spanish
  release notes and the spatial-control table locally. Published installers,
  updater hops and physical hardware were not retested in this website refresh;
  their evidence and remaining coverage belong to the upstream release record.


## 2026-10-05 — 1.2.0 Fractal Accents refresh

- Read the clean app checkout at merged `main`
  `a524e80babfb410993faa9bdba350bd6709810de`, confirmed against fetched
  `origin/main`. Reviewed the documentation map, current user/developer and
  release guides, changes since the prior ingestion, Fractal Accents local
  validation, and the published 1.2.0 acceptance record.
- Verified GitHub's latest public release is
  [v1.2.0 — Fractal Accents](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.2.0),
  published October 5 at 01:37 UTC (October 4 at 19:37 in America/Denver),
  with fourteen uploaded assets. The tag resolves to
  `323a62169eff9b2d639112d5dfe999a0e2b45fc4`. Product data retains the
  changelog date, 2026-10-04. Matched all three generated platform download
  targets on each homepage to the published asset URLs.
- Checked source exports: 96 presets (68 eligible for acceleration, 28 explicit
  Canvas) and 21 palettes. Read the six preset definitions and their retention
  and independent WTF selection behavior alongside the canonical guides.
- Updated both homepages for Threadlight, Silver Etching, Contour Silk, Julia
  Glass, Chromatic Undertow and Phosphor Lace, persistent accents, global
  Subtle Limit, and WTF's 95% Flat Media / 5% optional scene selection plus
  visibility checks. Retained existing design, media and shared components.
- Added the canonical Fractal Accents section to the feature importer and local
  link aliases. Refreshed release notes, renderer architecture and uniform
  layout, 96/68/28 backend ownership, performance and regression guidance, and
  the command reference including `smoke:wtf`. Unchanged guides regenerate
  without differences; historical release evidence retains its dated scope.
- Added 61 reviewed Spanish translation segments and protected the new preset
  and control names. Extended existing pipeline checks for accent links/names
  and current-state auditing for the catalog, controls and WTF probabilities.
- Validation: all ten pipeline tests, production Jekyll build, current-state
  audit, 52-page internal-link audit, SEO, support and performance audits passed.
  Both generators reproduced identical files. `git diff --check` passed.
  Visually reviewed the English/Spanish release sections, Spanish release notes,
  both feature tables and language switching with the section anchor preserved.
- This website refresh does not rebuild or retest desktop installers, updater
  transactions, native output or physical hardware. Their acceptance evidence
  and remaining coverage are linked from the upstream
  [1.2.0 release record](https://github.com/aindaco1/ascii-vj-remix/blob/main/docs/releases/RELEASE_1.2.0.md).
  The app checkout remains unchanged. Website publication is verified separately
  through the publishing commit's Pages workflow and live routes.

## 2026-10-13 — Upcoming 1.3.0 Native Video I/O

- Read the app's documentation map, agent guidance, README, candidate changelog,
  release record, and changes to the user, contributor, renderer, security,
  performance, testing, release and roadmap guides since the 1.2.0 ingestion.
  Reviewed package scripts and native component notices alongside those guides.
- The candidate remains on `feat/native-video-io`, ahead of `main`. Imported a
  fixed export of commit `512974b25a9a768c8d4cd253e3988f33578fdf86` while app
  preparation continued independently. Verified that commit on GitHub and
  confirmed no later documentation changes before completing this refresh.
  This task did not edit the app checkout.
- Queried GitHub's latest public release: **v1.2.0**, published
  `2026-10-05T01:37:21Z`, with fourteen assets. Verified the three platform
  download targets against that asset list. Product data retains its
  `2026-10-04` changelog date. No 1.3.0 release, installer or updater is claimed.
- Extended the existing importer to pin source links, retain the dated download
  baseline, and expose versioned Unreleased entries as a separate upcoming
  release. All 23 English and 23 Spanish developer pages identify the candidate
  and point to its exact source and acceptance record. Quickstart checks out
  that revision before setup. Native sharing anchors resolve locally; Linux
  troubleshooting and detailed acceptance records remain linked upstream.
- Refreshed native NDI/Syphon controls, shared output architecture, alpha,
  explicit LAN sharing, runtime staging and notices, Apple team signing,
  Linux Avahi requirements and source/CI/installed/hardware acceptance limits.
  Presets remain 96 total / 68 accelerated / 28 Canvas, with 21 palettes.
- Added upcoming-release sections, release-status links, search/social
  descriptions and support priorities in both languages. Preserved the
  Fractal Accents published-release summary, artwork and download components.
  NDI links and attribution accompany the new copy; video-only transport,
  macOS-only Syphon, opt-in sharing and the 1080p60 target are explicit.
- Added 77 reviewed Spanish segments, including technical headings, prose and
  unchanged command cells. Translation lookup reuses reviewed text when only
  a source commit URL changes, restores the exact pinned links, and prioritizes
  reviewed wording over cached service results. App control names stay intact.
- Validation: all 14 pipeline tests, production Jekyll build, current-state,
  52-page internal-link, SEO, support and performance audits passed. Both
  generators reproduced identical output. `git diff --check` passed.
- Visually reviewed the English and Spanish upcoming sections and the Spanish
  native-sharing guide, checked desktop and 390px mobile layouts, and verified
  language switching retains `#native-video-sharing`. Corrected the new prose
  and status links to use the existing cyan color after the visual check.
- This is a local website/documentation refresh. Desktop acceptance remains in
  the pinned candidate record; no desktop build, release publication or website
  deployment was performed. The maintenance guide records the copy changes
  needed when 1.3.0 is actually published.

### 1.3.0 launch-copy assumption

The owner subsequently requested treating 1.3.0 as imminently released and
presuming its download links. This supersedes the earlier candidate presentation:

- `_data/release_target.yml` selects 1.3.0 without changing the app repository's
  Unreleased entry or inventing a publication date. Regeneration retains the
  approved launch presentation until the upstream release is dated.
- Both homepages, metadata, support copy, release baseline and generated English
  and Spanish docs now present 1.3.0 as the current release. Candidate banners
  are removed; Fractal Accents remains a feature section.
- Downloads target the expected v1.3.0 macOS DMG, Windows EXE and Linux AppImage.
  Generic download actions and mobile/unknown-platform fallbacks point to the
  v1.3.0 release page. These URLs are presumed by request, not newly verified
  published assets. Technical performance and compatibility limits remain intact.
- Added nine reviewed Spanish segments and a launch-target pipeline regression.
  The previous source pin and desktop-validation evidence remain unchanged.
- Launch-copy validation: all 15 pipeline tests, the production build and all
  site audits passed. Refreshed browser checks
  confirmed v1.3.0 asset URLs, removed candidate banners and no horizontal
  overflow on both 390px homepages. `git diff --check` passed.

### Homepage editorial pass

At the owner's request, removed the homepage's repeated performance/setup
caveat and shortened the native-sharing cards in English and Spanish. Built-in
Looks now covers the breadth of the 96 presets, 21 palettes, customization,
playlists and WTF transitions instead of Fractal Accents recipes and 95/5
probabilities. Detailed limits remain in the developer guides. Updated the
homepage audit markers to match the broader copy. The production build,
current-state, 52-page link, SEO and performance audits passed; rendered
English desktop and Spanish mobile checks found no horizontal overflow.

## 2026-10-28 — 1.3.1 TLS security refresh

- Read the website maintenance/import/localization contracts and the app's
  documentation map, agent guide, README, changelog, user and security guides,
  contributor/release changes, shared-service guide, and published 1.3.0
  acceptance record. Reviewed the 1.3.1 Cargo dependency changes, package
  commands and `src-tauri/tests/tls_trust.rs` for the patch's scope.
- Imported the clean app checkout at
  `ab93bbd6b4d1634d3ee90e05dea743686b83d366`, verified against remote `main`
  and the peeled `v1.3.1` tag. The app checkout remains unchanged.
- Verified that GitHub's latest public release is
  [v1.3.1](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.3.1),
  published October 21 at 23:31:43 UTC (17:31:43 America/Denver), with fourteen
  uploaded assets. Both homepages' generated macOS DMG, Windows EXE and Linux
  AppImage URLs match the published assets. Product data uses the changelog
  date, `2026-10-21`.
- Removed the 1.3.0 launch override. Both homepages and their metadata now
  describe 1.3.1 as a certificate-trust security update; native NDI/Syphon
  sharing remains a separate feature section identified as introduced in 1.3.0.
  Existing media, styling, support and platform download components are retained.
- Refreshed all 23 English and 23 Spanish developer pages through the existing
  generators, with source links pinned to the release commit. Added the TLS
  command and source-linked guidance: it is opt-in, contacts public endpoints,
  requires a valid HTTPS control and `CertDistrusted` on twelve test chains,
  and does not accept generic network failure as proof of certificate rejection.
- The source README still names 1.3.0 as current, and its User Guide retains
  candidate wording for native sharing. Site release identity comes from the
  dated changelog; the importer normalizes that specific candidate sentence
  only for dated releases or explicit launch targets. A regression covers an
  older dated release alongside a genuinely unreleased future version.
- Added 23 reviewed Spanish translation segments. Updated maintenance guidance,
  source attribution and current-state checks for the release and TLS command.
- Validation: all 16 pipeline tests passed, including with the sibling app
  checkout unavailable as in CI. The production Jekyll build, current-state,
  52-page internal-link, SEO, support and performance audits passed. Both
  generators reproduced identical output, and `git diff --check` passed.
- Visually reviewed the new English/Spanish release sections and release notes,
  verified language switching and checked both homepages at 390px with no
  horizontal overflow. Desktop installers, live TLS acceptance and updater
  transactions were not rerun in this website task. These are local website
  changes; publication is a separate step.

## 2026-10-29 — 1.3.2 video soundtrack playback refresh

- Read the current app documentation map, agent guide, README, changelog,
  User Guide, rendering, testing and release-guide changes, and the published
  1.3.2 acceptance record. Checked the playback parameter exclusions, WTF
  changes, new smoke command and FFmpeg fallback against their implementations.
- Imported the clean app checkout at
  `eebf5bdca6c88c66a04cacd9a2a8256112880fdb`, matching remote `main`.
  This revision includes the publication evidence added after the released
  source commit `63d8a7421b220cb94261aa62559e3a8db6debe5c`, which the peeled
  `v1.3.2` tag still identifies. Generated source links pin the imported revision.
- Verified GitHub's latest public release as
  [v1.3.2](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.3.2),
  published October 29 at 08:11:31 UTC (02:11:31 America/Denver), with fourteen
  uploaded assets. The generated macOS DMG, Windows EXE and Linux AppImage
  targets match those assets and returned HTTP 200. The public updater manifest
  reports 1.3.2 with nine platform entries. Product data uses the dated changelog
  entry, `2026-10-29`.
- Updated both homepages, release labels and metadata for playback volume,
  mute and looping remaining user-controlled across presets, playlists, WTF
  and older saved presets. The shared download component now selects 1.3.2.
- Regenerated all 23 English and 23 Spanish developer pages. The source refresh
  adds playback ownership, the `smoke:video-playback` command and its inclusion
  in `smoke:static`, local-file soak options, and the checksum-pinned MacPorts
  fallback for FFmpeg source downloads. Explicit custom source URLs remain
  exclusive. Added a Commands cross-reference to the canonical testing guidance
  and 17 reviewed Spanish translation segments.
- Preserved the test coverage boundary: Chromium platform identities do not
  certify Windows/Linux native decoders or audio devices, and local-file signal
  summaries do not measure physical speakers. Desktop installation, updater
  and listening acceptance remain in the upstream release record; this website
  task did not rerun those checks.
- Validation: all 16 pipeline tests passed with the sibling app checkout
  unavailable as in CI. The production Jekyll build, current-state audit,
  52-page internal-link audit, SEO, support and performance audits passed.
- Both generators reproduced identical output. Reviewed both homepages and
  release-note pages in the browser, verified language switching, and checked
  the new release headings at a narrow 325-CSS-pixel viewport with no horizontal
  overflow. Restored the normal viewport and retained a local preview screenshot.
  `git diff --check` passed. This validation preceded website publication;
  deployment verification and cleanup receipts are recorded separately.
