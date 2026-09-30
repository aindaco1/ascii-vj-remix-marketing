# Site Maintenance

This guide is for maintainers of the marketing and documentation website.
The public developer guides describe the desktop application. This directory
is repository-only and is excluded from Jekyll and Spanish generation.

## Ownership and Layout

| Location | Owner / purpose |
| --- | --- |
| Root `README.md` | Repository entry point, preview, refresh, and validation commands. |
| `index.md`, `support.md`, `support/`, `es/index.md`, `es/support.md`, `es/support/` | Website routes and curated bilingual marketing/support copy. |
| `docs/overview/`, `docs/development/`, `docs/operations/`, `docs/reference/`, `docs/index.md` | Generated English app documentation; edit the upstream guide or importer. |
| `es/docs/` | Generated Spanish app documentation; edit reviewed translation overrides or the translation script. |
| `docs/maintenance/` | Website procedures and dated evidence; never generated or translated. |
| `_data/`, `_includes/`, `_layouts/`, `_sass/`, `assets/` | Shared site data, components, styling, and media. |

Keep one maintained procedure for each subject and link to it. The
[source notes](source-notes.md) record ingestion evidence; the
[support design QA](support-design-qa.md) records the 2026-08-25 review. Neither
is a current validation report.

## Source Refresh Contract

`scripts/sync_ascii_docs.rb` reads a local source checkout. Its default is the
sibling `../ascii-vj-remix`; set `ASCII_VJ_SOURCE` to use another checkout and
`ASCII_VJ_REPO` to change generated GitHub links for a fork. The script does not
fetch or update the source checkout. Inspect its branch, commit, and working
tree before refreshing.

Public developer guides follow merged `main`, while the release badge and
download links use the newest dated changelog entry. Clearly label post-release
source changes in their canonical upstream guide. Verify the published tag
separately; a newer source pin or relay adapter is not part of an older desktop
artifact. Correct stale upstream facts at their source before importing them.

The [public Source Map](../reference/source-map.md) documents the imported files:

- Root upstream `README.md` supplies product identity and lineage.
- `docs/USER_GUIDE.md` supplies detailed capabilities, spatial controls and trails, system requirements,
  hardware, and thermal guidance. Full usage, permissions, privacy, and
  troubleshooting remain linked upstream, along with the README's install steps.
- `docs/CONTRIBUTORS.md` supplies Quickstart and local development procedures.
  The complete npm script catalog is generated from `package.json` in Commands.
- `docs/SHARED_DESKTOP_MIGRATION.md` supplies Shared Desktop Services. Exact
  dependency versions remain owned by its linked `platform-desktop.json`;
  component-specific relay contracts remain in the upstream relay README.
- `docs/RELEASING.md` supplies Release and Updates. `docs/releases/` contains
  historical evidence and stays linked upstream; pending historical rows do not
  become current release claims.
- Architecture, agent, security, performance, testing, accessibility, i18n,
  roadmap, and changelog content comes from the corresponding maintained guide.

The importer resolves required files, sections, and relative source links before
writing pages or product data. When upstream splits or moves a guide, update
`SOURCE_FILES`, selected sections, and link aliases together. Only mirrored
sections get local fragment links; other sections link to the full upstream guide.
Keep existing public page URLs stable when changing their source ownership.

The newest **dated** changelog entry supplies the release badge; Unreleased is
excluded. `_data/product.yml` also records the copied canonical icon SHA-256.
The date is the changelog date and may differ from publication time. Verify the
release and platform assets on GitHub Releases before publishing updated claims.

## Spanish Documentation

Run `python3 scripts/build_spanish_docs.py` after the English sync. It translates
public docs only, applies reviewed translations before cache/service results,
and preserves source/attribution URLs, code blocks, and technical tokens.
The existing translation service receives uncached public prose. Local cached
translations live in the ignored `.translation-cache/` directory.

Reviewed passages live in `scripts/spanish-docs-overrides.json`, keyed by the full
English paragraph or table cell. Add an entry when wording changes or a technical
translation needs correction; generated Spanish pages are overwritten on rerun.

The translation step uses the site's bundled Kramdown engine through
`scripts/docs_heading_ids.rb`. It retains Spanish heading IDs and adds English
anchor aliases, so translated internal links keep working when upstream adds
cross-references. External GitHub anchors remain unchanged. Run `bundle install`
before translation on a new checkout.

For a focused refresh, set `ASCII_VJ_TRANSLATION_FILES` to comma-separated paths
such as `operations/release.md,development/quickstart.md`. Use
`ASCII_VJ_TRANSLATION_WORKERS` to control concurrency (default 1). Review the
generated diff and run the link and current-state audits after every refresh.

## Validation and Publication

The root [README](../../README.md#refresh-and-validate) owns the full refresh and
build command sequence. The current-state audit checks release labels, feature
markers, canonical guide ownership, Spanish source links, and the icon hash and
dimensions. The built-site audits check internal links and anchors, SEO, support
contracts, and performance budgets.

When changing the import or localization scripts, run their focused regressions:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

The performance audit protects inline homepage critical CSS, route-scoped
animation, content-addressed assets, responsive video metadata, and font/video
size budgets. Documentation moves also require checking old path references and
confirming that maintenance files are absent from `_site`, search, and sitemap.

`.github/workflows/workflow.yml` builds and audits pushes to `main` and manual
dispatches before deploying to GitHub Pages. A local build is local validation;
verify the deployed site separately after publication.

## Shared Support and Download Components

`_data/support.yml` is the single source for the support brand and checkout
options. Both support pages render `_includes/support-options.html`. The
contract supports a customer-chosen one-time amount (suggested at $10) and a
fixed $5/month option.

`scripts/audit_support.py` validates localized UTM attribution, both cadences,
and direct Stripe-hosted checkout links. Production rejects test links. For a
deliberate test-mode preview only:

```bash
SUPPORT_ALLOW_TEST_LINKS=1 python3 scripts/audit_support.py
```

When checkout resources change, create and verify replacement Products, Prices,
and localized Payment Links, then update the data in a coordinated release. Do
not archive a recurring Price or Product while subscriptions still depend on it.

The homepage download action uses `_includes/download-latest-button.html`.
It derives macOS DMG, Windows installer, and Linux AppImage URLs from
`_data/product.yml`; `assets/js/site.js` selects the visitor's desktop platform.
Mobile and unknown platforms use GitHub's latest-release page. The performance
audit checks both homepages and the generated artifact URLs.
