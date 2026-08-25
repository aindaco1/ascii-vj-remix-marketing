#!/usr/bin/env python3
"""Guard the generated site's deliberate performance optimizations."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PRODUCT = ROOT / "_data" / "product.yml"

HOME_PAGES = ["index.html", "es/index.html"]
DOC_PAGES = ["docs/index.html", "es/docs/index.html"]
HERO_WEBM = ROOT / "assets" / "videos" / "ascii-hero.webm"
HERO_MP4 = ROOT / "assets" / "videos" / "ascii-hero.mp4"
DISPLAY_FONT = ROOT / "assets" / "fonts" / "VCR_OSD_MONO_1.001.woff2"

WEBM_BUDGET = 4_000_000
MP4_BUDGET = 4_000_000
FONT_BUDGET = 20_000
HASHED_SITE_JS = re.compile(r"/assets/js/site\.js\?v=[0-9a-f]{12}")
HASHED_HOME_JS = re.compile(r"/assets/js/home-animation\.js\?v=[0-9a-f]{12}")
HASHED_WEBM = re.compile(r"/assets/videos/ascii-hero\.webm\?v=[0-9a-f]{12}")
HASHED_MP4 = re.compile(r"/assets/videos/ascii-hero\.mp4\?v=[0-9a-f]{12}")
PLACEHOLDER_LEAK = re.compile(r"(?:ZZTOKEN|ZXQZXQ|ZXC[A-Z0-9]+ZX)")


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
        require('as="image" type="image/svg+xml" fetchpriority="high"' in html, errors, f"{rel}: hero poster preload is missing")
        require('type="font/woff2"' in html and 'rel="preload"' in html, errors, f"{rel}: WOFF2 preload is missing")
        require('width="1200" height="766"' in html, errors, f"{rel}: hero video dimensions are missing")
        require('fetchpriority="high"' in html, errors, f"{rel}: hero video priority hint is missing")
        require(release and f"v{release}" in html, errors, f"{rel}: latest release v{release} is missing")

    for rel in DOC_PAGES:
        html = read(rel, errors)
        if not html:
            continue
        require(HASHED_SITE_JS.search(html) is not None, errors, f"{rel}: site.js is not content-addressed")
        require("home-animation.js" not in html, errors, f"{rel}: homepage animation leaked into docs")

    if SITE.exists():
        for path in SITE.rglob("*.html"):
            html = path.read_text(errors="replace")
            label = path.relative_to(SITE)
            require("VCR_OSD_MONO_1.001.ttf" not in html, errors, f"{label}: legacy TTF is requested")
            require(PLACEHOLDER_LEAK.search(html) is None, errors, f"{label}: translation placeholder leaked")

    webm_size = check_asset(HERO_WEBM, WEBM_BUDGET, errors)
    mp4_size = check_asset(HERO_MP4, MP4_BUDGET, errors)
    font_size = check_asset(DISPLAY_FONT, FONT_BUDGET, errors)

    if errors:
        print("Performance audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Performance audit passed "
        f"(WebM {webm_size:,} B, MP4 {mp4_size:,} B, WOFF2 {font_size:,} B)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
