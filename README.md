# ascii-vj-remix-marketing

Marketing site and developer documentation for [ASCII VJ Remix](https://asciivj.com),
built with Jekyll and `just-the-docs`.

## Local Preview

```bash
bundle install
bundle exec jekyll serve
```

## Documentation Map

- [`docs/index.md`](docs/index.md): public developer documentation. English pages
  are generated from the [mother repository](https://github.com/aindaco1/ascii-vj-remix).
- [`es/docs/index.md`](es/docs/index.md): generated Spanish developer documentation.
- [`docs/maintenance/README.md`](docs/maintenance/README.md): site maintenance,
  source refresh, localization, validation, and shared support/download contracts.
- [`docs/maintenance/source-notes.md`](docs/maintenance/source-notes.md): dated
  source-ingestion evidence and claims policy.
- [`docs/maintenance/support-design-qa.md`](docs/maintenance/support-design-qa.md):
  historical support-page design review.

Keep the root README as the repository entry point and any license file at the
root. `index.md` and `support.md` are website routes and stay in place. Internal
guides belong in `docs/maintenance/`, which is excluded from the public build,
search, sitemap, translation, and current-product claims audits. Component
documentation and required third-party notices stay beside their components.

## Refresh and Validate

The mother repository owns technical behavior. This repository owns public
marketing copy, documentation presentation, localization, and deployment.
Edit upstream guides or the import templates, then regenerate; do not hand-edit
generated English or Spanish pages.

The default source is the sibling `../ascii-vj-remix` checkout. Override it with
`ASCII_VJ_SOURCE=/absolute/path/to/ascii-vj-remix` when needed.

```bash
ruby scripts/sync_ascii_docs.rb
python3 scripts/build_spanish_docs.py
bundle exec jekyll build --trace
python3 scripts/audit_docs_current_state.py
python3 scripts/audit_links.py
python3 scripts/audit_seo.py
python3 scripts/audit_support.py
python3 scripts/audit_performance.py
git diff --check
```

See the [maintenance guide](docs/maintenance/README.md) for source ownership,
translation overrides, pipeline tests, release verification, and publishing.
