#!/usr/bin/env python3
"""Conservative generated-site SEO audit for the ASCII VJ Remix marketing/docs site."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
SITE_ORIGIN = "https://aindaco1.github.io/ascii-vj-remix-marketing"
REQUIRED_PAGES = [
    "index.html",
    "es/index.html",
    "support/index.html",
    "es/support/index.html",
    "docs/index.html",
    "es/docs/index.html",
]
FORBIDDEN_FOOTER_TEXT = ["ASCII repo", "Source map", "Repositorio ASCII", "Mapa de fuentes"]


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""
        self.lang = ""
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k.lower(): v or "" for k, v in attrs}
        if tag == "html":
            self.lang = data.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.meta.append(data)
        elif tag == "link":
            self.links.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def meta_content(parser: HeadParser, *, name: str | None = None, prop: str | None = None) -> str:
    for item in parser.meta:
        if name and item.get("name") == name:
            return item.get("content", "").strip()
        if prop and item.get("property") == prop:
            return item.get("content", "").strip()
    return ""


def link_href(parser: HeadParser, *, rel: str, hreflang: str | None = None) -> str:
    for item in parser.links:
        rels = item.get("rel", "").split()
        if rel in rels and (hreflang is None or item.get("hreflang") == hreflang):
            return item.get("href", "").strip()
    return ""


def is_abs_http(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def audit_page(rel: str, errors: list[str]) -> None:
    path = SITE / rel
    if not path.exists():
        fail(errors, f"missing required page: {rel}")
        return
    html = path.read_text(errors="replace")
    parser = HeadParser()
    parser.feed(html)
    label = f"/{rel}" if rel != "index.html" else "/"

    if not parser.lang:
        fail(errors, f"{label}: missing html lang")
    if not parser.title.strip():
        fail(errors, f"{label}: missing title")
    desc = meta_content(parser, name="description")
    if len(desc) < 50:
        fail(errors, f"{label}: missing or thin meta description")
    canonical = link_href(parser, rel="canonical")
    if not is_abs_http(canonical):
        fail(errors, f"{label}: canonical is not absolute: {canonical!r}")
    og_url = meta_content(parser, prop="og:url")
    if not is_abs_http(og_url):
        fail(errors, f"{label}: og:url is not absolute: {og_url!r}")
    for prop in ["og:title", "og:description", "og:site_name", "og:type", "og:image"]:
        if not meta_content(parser, prop=prop):
            fail(errors, f"{label}: missing {prop}")
    og_image = meta_content(parser, prop="og:image")
    if og_image and not is_abs_http(og_image):
        fail(errors, f"{label}: og:image is not absolute: {og_image!r}")
    for name in ["twitter:card", "twitter:title", "twitter:description", "application-name", "apple-mobile-web-app-title", "language"]:
        if not meta_content(parser, name=name):
            fail(errors, f"{label}: missing {name}")
    for lang in ["en", "es", "x-default"]:
        href = link_href(parser, rel="alternate", hreflang=lang)
        if not is_abs_http(href):
            fail(errors, f"{label}: missing absolute hreflang {lang}")
    footers = re.findall(r"<footer\b[^>]*>.*?</footer>", html, flags=re.IGNORECASE | re.DOTALL)
    footer_html = "\n".join(footers)
    for forbidden in FORBIDDEN_FOOTER_TEXT:
        if forbidden in footer_html:
            fail(errors, f"{label}: forbidden footer text still present: {forbidden}")


def main() -> int:
    errors: list[str] = []
    if not SITE.exists():
        fail(errors, "_site does not exist; run a Jekyll build first")
    else:
        for rel in REQUIRED_PAGES:
            audit_page(rel, errors)
        robots = SITE / "robots.txt"
        sitemap = SITE / "sitemap.xml"
        if not robots.exists():
            fail(errors, "missing robots.txt")
        else:
            body = robots.read_text(errors="replace")
            if "Sitemap:" not in body or SITE_ORIGIN not in body:
                fail(errors, "robots.txt missing absolute sitemap URL")
        if not sitemap.exists():
            fail(errors, "missing sitemap.xml")
        else:
            body = sitemap.read_text(errors="replace")
            if SITE_ORIGIN not in body:
                fail(errors, "sitemap.xml does not contain absolute site origin")
            if "/docs/overview/</loc>" in body or "/es/docs/overview/</loc>" in body:
                fail(errors, "sitemap includes removed duplicate overview index URL")
    if errors:
        print("SEO audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("SEO audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
