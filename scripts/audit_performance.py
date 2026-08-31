#!/usr/bin/env python3
"""Guard the generated site's deliberate performance optimizations."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PRODUCT = ROOT / "_data" / "product.yml"

HOME_PAGES = ["index.html", "es/index.html"]
DOC_PAGES = ["docs/index.html", "es/docs/index.html"]
THEME_PAGES = [*DOC_PAGES, "support/index.html", "es/support/index.html"]
HERO_WEBM = ROOT / "assets" / "videos" / "ascii-hero.webm"
HERO_MP4 = ROOT / "assets" / "videos" / "ascii-hero.mp4"
DISPLAY_FONT = ROOT / "assets" / "fonts" / "VCR_OSD_MONO_1.001.woff2"
APP_ICON = ROOT / "assets" / "images" / "ascii-vj-remix-app-icon.png"
SITE_SCRIPT = ROOT / "assets" / "js" / "site.js"

WEBM_BUDGET = 4_000_000
MP4_BUDGET = 4_000_000
FONT_BUDGET = 20_000
APP_ICON_BUDGET = 250_000
HASHED_SITE_JS = re.compile(r"/assets/js/site\.js\?v=[0-9a-f]{12}")
HASHED_THEME_CSS = re.compile(r"/assets/css/just-the-docs-default\.css\?v=[0-9a-f]{12}")
HASHED_HOME_JS = re.compile(r"/assets/js/home-animation\.js\?v=[0-9a-f]{12}")
HASHED_WEBM = re.compile(r"/assets/videos/ascii-hero\.webm\?v=[0-9a-f]{12}")
HASHED_MP4 = re.compile(r"/assets/videos/ascii-hero\.mp4\?v=[0-9a-f]{12}")
HASHED_APP_ICON = re.compile(r"/assets/images/ascii-vj-remix-app-icon\.png\?v=[0-9a-f]{12}")
PLACEHOLDER_LEAK = re.compile(r"(?:ZZTOKEN|ZXQZXQ|ZXC[A-Z0-9]+ZX)")


class DownloadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.downloads: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "a" and "data-download-latest" in data:
            self.downloads.append(data)


def read(rel: str, errors: list[str]) -> str:
    path = SITE / rel
    if not path.exists():
        errors.append(f"missing generated page: {rel}")
        return ""
    return path.read_text(errors="replace")


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def latest_release() -> str:
    match = re.search(r'^\s*version:\s*["\']?([^"\'\s]+)', PRODUCT.read_text(), re.MULTILINE)
    if not match:
        raise ValueError("could not parse latest release version")
    return match.group(1)


def check_asset(path: Path, budget: int, errors: list[str]) -> int:
    if not path.exists():
        errors.append(f"missing optimized asset: {path.relative_to(ROOT)}")
        return 0
    size = path.stat().st_size
    require(
        size <= budget,
        errors,
        f"{path.relative_to(ROOT)} is {size:,} bytes; budget is {budget:,}",
    )
    return size


def main() -> int:
    errors: list[str] = []
    if not SITE.exists():
        errors.append("_site does not exist; run a Jekyll build first")
    try:
        release = latest_release()
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        release = ""

    site_script = SITE_SCRIPT.read_text(errors="replace") if SITE_SCRIPT.exists() else ""
    require(bool(site_script), errors, "assets/js/site.js is missing")
    require(
        "const activeLang = queryLang || pageLang || 'en';" in site_script,
        errors,
        "site language is not owned by the current localized route",
    )
    require(
        "ascii-vj-lang" not in site_script,
        errors,
        "stored language state can override the current localized route",
    )

    for rel in HOME_PAGES:
        html = read(rel, errors)
        if not html:
            continue
        require('<style data-home-critical>' in html, errors, f"{rel}: critical CSS is not inline")
        require('.skip-link{position:absolute' in html, errors, f"{rel}: skip-link hiding styles are missing")
        require("/assets/css/home.css" not in html, errors, f"{rel}: external homepage CSS returned")
        require('<canvas class="ascii-art-background"' in html, errors, f"{rel}: initial canvas is missing")
        require('<pre class="ascii-art-background"' not in html, errors, f"{rel}: late-inserted ASCII pre returned")
        require(HASHED_SITE_JS.search(html) is not None, errors, f"{rel}: site.js is not content-addressed")
        require(HASHED_HOME_JS.search(html) is not None, errors, f"{rel}: homepage animation is not content-addressed")
        require(HASHED_WEBM.search(html) is not None, errors, f"{rel}: WebM source is not content-addressed")
        require(HASHED_MP4.search(html) is not None, errors, f"{rel}: MP4 fallback is not content-addressed")
        require(HASHED_APP_ICON.search(html) is not None, errors, f"{rel}: app icon is not content-addressed")
        require('as="image" type="image/svg+xml" fetchpriority="high"' in html, errors, f"{rel}: hero poster preload is missing")
        require('type="font/woff2"' in html and 'rel="preload"' in html, errors, f"{rel}: WOFF2 preload is missing")
        require('width="1200" height="766"' in html, errors, f"{rel}: hero video dimensions are missing")
        require('fetchpriority="high"' in html, errors, f"{rel}: hero video priority hint is missing")
        require(release and f"v{release}" in html, errors, f"{rel}: latest release v{release} is missing")
        if rel == "index.html":
            require("All 69 built-in presets must remain visible" in html, errors, f"{rel}: renderer contract is missing")
            require("search presets by name" in html, errors, f"{rel}: preset search story is missing")
            require("retry through the included FFmpeg path" in html, errors, f"{rel}: bundled video fallback story is missing")
            require("share transition timing" in html, errors, f"{rel}: synchronized Pop Out story is missing")
        else:
            require("Los 69 presets integrados deben seguir visibles" in html, errors, f"{rel}: falta el contrato de renderizado")
            require("busca presets por nombre" in html, errors, f"{rel}: falta la historia de búsqueda de presets")
            require("reintentarse con FFmpeg" in html, errors, f"{rel}: falta la historia del fallback de video")
            require("comparten el tiempo de las transiciones" in html, errors, f"{rel}: falta la historia de Pop Out sincronizado")

        parser = DownloadParser()
        parser.feed(html)
        require(len(parser.downloads) == 1, errors, f"{rel}: expected exactly one latest-download action")
        if len(parser.downloads) == 1:
            download = parser.downloads[0]
            release_base = f"https://github.com/aindaco1/ascii-vj-remix/releases/download/v{release}/"
            expected = {
                "href": "https://github.com/aindaco1/ascii-vj-remix/releases/latest",
                "data-download-macos": f"{release_base}ASCII.VJ.Remix_{release}_aarch64.dmg",
                "data-download-windows": f"{release_base}ASCII.VJ.Remix_{release}_x64-setup.exe",
                "data-download-linux": f"{release_base}ASCII.VJ.Remix_{release}_amd64.AppImage",
            }
            for attribute, value in expected.items():
                require(download.get(attribute) == value, errors, f"{rel}: invalid {attribute} download target")

    for rel in DOC_PAGES:
        html = read(rel, errors)
        if not html:
            continue
        require(HASHED_SITE_JS.search(html) is not None, errors, f"{rel}: site.js is not content-addressed")
        require("home-animation.js" not in html, errors, f"{rel}: homepage animation leaked into docs")
        require("/assets/js/vendor/lunr.min.js" in html, errors, f"{rel}: docs search index is missing")
        require("/assets/js/just-the-docs.js" in html, errors, f"{rel}: docs theme behavior is missing")

    for rel in THEME_PAGES:
        html = read(rel, errors)
        if not html:
            continue
        require(HASHED_THEME_CSS.search(html) is not None, errors, f"{rel}: theme CSS is not content-addressed")

    if SITE.exists():
        for path in SITE.rglob("*.html"):
            html = path.read_text(errors="replace")
            label = path.relative_to(SITE)
            require("VCR_OSD_MONO_1.001.ttf" not in html, errors, f"{label}: legacy TTF is requested")
            require(PLACEHOLDER_LEAK.search(html) is None, errors, f"{label}: translation placeholder leaked")

    webm_size = check_asset(HERO_WEBM, WEBM_BUDGET, errors)
    mp4_size = check_asset(HERO_MP4, MP4_BUDGET, errors)
    font_size = check_asset(DISPLAY_FONT, FONT_BUDGET, errors)
    icon_size = check_asset(APP_ICON, APP_ICON_BUDGET, errors)

    if errors:
        print("Performance audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Performance audit passed "
        f"(WebM {webm_size:,} B, MP4 {mp4_size:,} B, WOFF2 {font_size:,} B, icon {icon_size:,} B)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
