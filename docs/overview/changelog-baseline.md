---
title: "Release Baseline"
description: "Source-derived Release Baseline documentation for developers maintaining, extending, packaging, or contributing to ASCII VJ Remix."
nav_order: 3
parent: "Overview"
---

# Release Baseline

The current release is **1.3.1**. The [Changelog](/docs/reference/changelog/) contains the full version history.

[Download v1.3.1](https://github.com/aindaco1/ascii-vj-remix/releases/tag/v1.3.1).

See the [Feature Set](/docs/overview/features/) for current controls and the upstream [release records](https://github.com/aindaco1/ascii-vj-remix/blob/ab93bbd6b4d1634d3ee90e05dea743686b83d366/docs/releases/README.md) for version-specific validation and platform coverage.



## 1.3.1 Release Notes

- Reject compromised eMudhra TLS chains with rustls-webpki 0.103.16 and webpki root bundles 1.0.10.
- Add opt-in live TLS acceptance against all 12 disclosed test chains and a valid HTTPS control (`npm run test:tls`).



## Source Material

This page is generated from ASCII VJ Remix source material. Primary sources:
- [CHANGELOG.md](https://github.com/aindaco1/ascii-vj-remix/blob/ab93bbd6b4d1634d3ee90e05dea743686b83d366/CHANGELOG.md)
