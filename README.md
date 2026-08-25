# ascii-vj-remix-marketing

Marketing site and developer documentation for ASCII VJ Remix.

Canonical site: `https://asciivj.com`

Built with Jekyll and `just-the-docs`, following the architecture of `pool-marketing-docs`.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

## Production build

```bash
bundle exec jekyll build --trace
python3 scripts/audit_seo.py
python3 scripts/audit_performance.py
```

The performance audit protects the homepage's inline critical CSS, route-scoped
animation, content-addressed assets, responsive video metadata, and optimized
font/video size budgets.

## Refresh from the source project

The product documentation and release label are generated from the local ASCII
VJ Remix checkout:

```bash
ruby scripts/sync_ascii_docs.rb
python3 scripts/build_spanish_docs.py
bundle exec jekyll build --trace
python3 scripts/audit_seo.py
python3 scripts/audit_performance.py
```

Review generated changes before publishing. The source changelog may include an
unreleased section; the marketing site's release badge intentionally selects the
newest dated release instead.

## Source repo

- `/Users/aindaco1/Library/Mobile Documents/com~apple~CloudDocs/ascii-vj-remix`
