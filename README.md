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
python3 scripts/audit_docs_current_state.py
python3 scripts/audit_links.py
python3 scripts/audit_seo.py
python3 scripts/audit_support.py
python3 scripts/audit_performance.py
```

The performance audit protects the homepage's inline critical CSS, route-scoped
animation, content-addressed assets, responsive video metadata, and optimized
font/video size budgets.

## Dust Wave Support contract

`_data/support.yml` is the single source for the support brand and checkout options. The English and Spanish support pages render that data with `_includes/support-options.html`, so provider configuration stays shared while ASCII VJ Remix keeps its own visual language. The contract intentionally supports one customer-chosen one-time amount (suggested at $10) and one fixed $5/month option.

`scripts/audit_support.py` validates both built support pages, localized UTM attribution, the two required cadences, and direct Stripe-hosted checkout links. Production validation rejects Stripe test links. During a deliberate test-mode preview, use:

```bash
SUPPORT_ALLOW_TEST_LINKS=1 python3 scripts/audit_support.py
```

The homepage's single latest-download action is rendered by `_includes/download-latest-button.html`. It derives the macOS DMG, Windows installer, and Linux AppImage URLs from `_data/product.yml`, then `assets/js/site.js` chooses the visitor's desktop platform. Mobile and unknown platforms keep the GitHub latest-release page as a safe fallback. The committed performance audit checks both localized pages and every generated artifact URL.

When checkout resources change, create and verify the replacement Product, Prices, and localized Payment Links first; then update `_data/support.yml` in a coordinated release. Do not archive an old recurring Price or Product while existing subscriptions still depend on it.

## Refresh from the source project

The product documentation and release label are generated from the local ASCII
VJ Remix checkout:

```bash
ruby scripts/sync_ascii_docs.rb
python3 scripts/build_spanish_docs.py
bundle exec jekyll build --trace
python3 scripts/audit_docs_current_state.py
python3 scripts/audit_links.py
python3 scripts/audit_seo.py
python3 scripts/audit_support.py
python3 scripts/audit_performance.py
```

Review generated changes before publishing. The source changelog may include an
unreleased section; the marketing site's release badge intentionally selects the
newest dated release instead.

## Source repo

- `/Users/aindaco1/Library/Mobile Documents/com~apple~CloudDocs/ascii-vj-remix`
