#!/usr/bin/env python3
"""Reject stale or aspirational claims in generated current-state documentation."""
from __future__ import annotations

import hashlib
import re
import sys
from collections import Counter
from pathlib import Path
from docs_common import public_docs

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SPANISH_DOCS = ROOT / "es" / "docs"
PRODUCT = ROOT / "_data" / "product.yml"
CURRENT_STATE_EXCLUSIONS = {
    DOCS / "reference" / "changelog.md",
    DOCS / "reference" / "roadmap.md",
}
SPANISH_CURRENT_STATE_EXCLUSIONS = {
    SPANISH_DOCS / "reference" / "changelog.md",
    SPANISH_DOCS / "reference" / "roadmap.md",
}

FORBIDDEN_CURRENT_STATE = {
    "stale release-candidate baseline": re.compile(r"The current source/package release candidate is", re.I),
    "legacy point-and-click reference": re.compile(r"ascii[- ]point[- ]and[- ]click|point[- ](?:and[- ])?click", re.I),
    "stale 0.9.3 release posture": re.compile(r"public 0\.9\.3 release CI|Windows 0\.9\.3 artifacts", re.I),
    "stale 0.9.5 current posture": re.compile(r"Windows 0\.9\.5 artifacts|current development docs describe 0\.9\.6 on top of the released 0\.9\.5", re.I),
    "stale 0.9.6 current posture": re.compile(r"Public 0\.9\.6 (?:macOS|Windows) artifacts|Current source docs describe the \*\*0\.9\.6\*\* feature set", re.I),
    "aspirational macOS release claim": re.compile(r"public macOS release builds should be Developer ID signed", re.I),
    "unfinished-signing placeholder": re.compile(r"until (?:a|the) signing backend is (?:proven|ready)", re.I),
    "unfinished-stream placeholder": re.compile(r"hides stream mode until .*ready", re.I),
    "unfinished-MIDI placeholder": re.compile(r"physical commissioning remains incomplete|physical commissioning and broader platform validation remain follow-on work", re.I),
    "future catalog in current-state docs": re.compile(r"future bundled (?:translation )?catalog", re.I),
    "future-work section in current-state docs": re.compile(r"^##\s+(?:Future\b|Open Engineering Work\b|Known Future Work\b)", re.I | re.M),
    "future capture requirement": re.compile(r"PipeWire for future capture work", re.I),
    "future implementation presented as architecture": re.compile(r"the long-term answer for packaged stream-style", re.I),
    "translation placeholder leak": re.compile(r"ZZTOKEN|ZXQZXQ|ZXC[A-Z0-9]+ZX|BEGIN SOURCE|END SOURCE", re.I),
}

FORBIDDEN_SPANISH_CURRENT_STATE = {
    "legacy point-and-click reference": re.compile(r"ascii[- ]point[- ]and[- ]click|point[- ](?:and[- ])?click|juego.*point", re.I),
    "stale 0.9.3 release posture": re.compile(r"versión pública 0\.9\.3 CI|artefactos.*Windows 0\.9\.3", re.I),
    "stale 0.9.5 current posture": re.compile(r"artefactos.*Windows 0\.9\.5|documentos de desarrollo actuales.*0\.9\.5", re.I),
    "stale 0.9.6 current posture": re.compile(r"artefactos públicos 0\.9\.6 (?:macOS|Windows)|documentos fuente actuales.*\*\*0\.9\.6\*\*", re.I),
    "unfinished-signing placeholder": re.compile(r"hasta que se (?:pruebe|demuestre).*firma", re.I),
    "unfinished-MIDI placeholder": re.compile(r"puesta en servicio.*incompleta", re.I),
    "future-work section in current-state docs": re.compile(r"^##\s+(?:Funciones futuras|Trabajo futuro conocido|Trabajo de ingeniería abierto|Futuro)\b", re.I | re.M),
    "translation placeholder leak": re.compile(r"ZZTOKEN|ZXQZXQ|ZXC[A-Z0-9]+ZX|BEGIN SOURCE|END SOURCE|FIN DOCUMENTOS", re.I),
}

ENGLISH_RELEASE_CLAIMS = {
    "current docs feature set": re.compile(
        r"Current (?:source )?docs describe the \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*"
    ),
    "overview feature baseline": re.compile(
        r"current ([0-9]+\.[0-9]+\.[0-9]+) feature baseline", re.I
    ),
    "latest verified public release": re.compile(
        r"latest verified public release are\s+([0-9]+\.[0-9]+\.[0-9]+)", re.I
    ),
    "public macOS artifacts": re.compile(
        r"Public ([0-9]+\.[0-9]+\.[0-9]+) macOS artifacts", re.I
    ),
}

SPANISH_RELEASE_CLAIMS = {
    "current docs feature set": re.compile(
        r"documentos(?: fuente)? actuales describen.*?\*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*",
        re.I,
    ),
    "public macOS artifacts": re.compile(
        r"artefactos públicos ([0-9]+\.[0-9]+\.[0-9]+) macOS", re.I
    ),
}

REQUIRED_FEATURE_MARKERS = [
    "Seventeen project-native palettes",
    "Bayer 2x2/4x4/8x8 dithering",
    "custom typed ramps of up to 96 supported Unicode scalars",
    "Advanced Density preference exposes up to 900 columns",
    "ASCII World Mint",
    "ASCII City Nightshift",
    "Multiple named preset playlists",
    "Media Foundation on Windows",
    "V4L2 through the bundled local FFmpeg",
    "PNG directly to Desktop",
    "manual current-state diagnostic",
]

HOMEPAGE_MARKERS = {
    "index.md": [
        "71 built-in presets, 17 palettes",
        "Preset playlists",
        "Save a frame",
        "ASCII World Mint",
        "ASCII City Nightshift",
    ],
    "es/index.md": [
        "71 presets integrados, 17 paletas",
        "Listas de presets",
        "Guarda un fotograma",
        "ASCII World Mint",
        "ASCII City Nightshift",
    ],
}


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def product_value(key: str) -> str:
    body = PRODUCT.read_text(errors="replace")
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\s]+)", body, re.MULTILINE)
    if not match:
        raise ValueError(f"could not parse {key} from {relative(PRODUCT)}")
    return match.group(1)


def audit_release_claims(
    docs_root: Path,
    exclusions: set[Path],
    patterns: dict[str, re.Pattern[str]],
    expected: str,
    errors: list[str],
) -> None:
    for path in public_docs(docs_root):
        if path in exclusions:
            continue
        body = path.read_text(errors="replace")
        for label, pattern in patterns.items():
            for match in pattern.finditer(body):
                actual = match.group(1)
                if actual != expected:
                    line = body.count("\n", 0, match.start()) + 1
                    errors.append(
                        f"{relative(path)}:{line}: {label} says {actual}; expected {expected}"
                    )


def audit_icon(expected_sha256: str, errors: list[str]) -> None:
    icon = ROOT / "assets" / "images" / "ascii-vj-remix-app-icon.png"
    if not icon.exists():
        errors.append(f"{relative(icon)} is missing")
        return

    data = icon.read_bytes()
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != expected_sha256:
        errors.append(
            f"{relative(icon)} hash {actual_sha256} does not match product data {expected_sha256}"
        )
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append(f"{relative(icon)} is not a valid PNG")
        return
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (512, 512):
        errors.append(f"{relative(icon)} is {width}x{height}; expected 512x512")


def audit_tree(
    docs_root: Path,
    exclusions: set[Path],
    patterns: dict[str, re.Pattern[str]],
    errors: list[str],
) -> None:
    if not docs_root.exists():
        errors.append(f"{relative(docs_root)} directory is missing")
        return
    for path in public_docs(docs_root):
        if path in exclusions:
            continue
        body = path.read_text(errors="replace")
        for label, pattern in patterns.items():
            match = pattern.search(body)
            if match:
                line = body.count("\n", 0, match.start()) + 1
                errors.append(f"{relative(path)}:{line}: {label}")


def audit_translated_source_links(errors: list[str]) -> None:
    """Translation must retain source, attribution, and internal fragment links."""
    link = re.compile(r"\[[^\[\]\n]+\]\(([^)]+)\)")
    for english in public_docs(DOCS):
        spanish = SPANISH_DOCS / english.relative_to(DOCS)
        if not spanish.exists():
            errors.append(f"{relative(spanish)} is missing")
            continue
        expected = Counter(link.findall(english.read_text()))
        actual = Counter(
            target.removeprefix("/es") if target.startswith("/es/docs/") else target
            for target in link.findall(spanish.read_text())
        )
        if expected != actual:
            errors.append(f"{relative(spanish)}: source or internal links differ from English")


def main() -> int:
    errors: list[str] = []
    for name, markers in HOMEPAGE_MARKERS.items():
        homepage = ROOT / name
        body = homepage.read_text(errors="replace")
        for marker in markers:
            if marker not in body:
                errors.append(f"{name}: missing current homepage marker: {marker}")
        if re.search(r"first stable desktop release|primera versión estable de escritorio|\b69\b|\b16 (?:built-in palettes|paletas integradas)\b", body):
            errors.append(f"{name}: stale 1.0.0 homepage copy")
    try:
        release = product_value("version")
        icon_sha256 = product_value("sha256")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        release = ""
        icon_sha256 = ""

    audit_tree(DOCS, CURRENT_STATE_EXCLUSIONS, FORBIDDEN_CURRENT_STATE, errors)
    audit_tree(
        SPANISH_DOCS,
        SPANISH_CURRENT_STATE_EXCLUSIONS,
        FORBIDDEN_SPANISH_CURRENT_STATE,
        errors,
    )
    audit_translated_source_links(errors)

    if release:
        audit_release_claims(
            DOCS,
            CURRENT_STATE_EXCLUSIONS,
            ENGLISH_RELEASE_CLAIMS,
            release,
            errors,
        )
        audit_release_claims(
            SPANISH_DOCS,
            SPANISH_CURRENT_STATE_EXCLUSIONS,
            SPANISH_RELEASE_CLAIMS,
            release,
            errors,
        )

        release_baseline = DOCS / "overview" / "changelog-baseline.md"
        baseline_body = release_baseline.read_text(errors="replace") if release_baseline.exists() else ""
        if f"## {release} Release Notes" not in baseline_body:
            errors.append(
                f"{relative(release_baseline)}: missing generated {release} release-notes heading"
            )

        features = DOCS / "overview" / "features.md"
        feature_body = features.read_text(errors="replace") if features.exists() else ""
        normalized_feature_body = re.sub(r"\s+", " ", feature_body)
        for marker in REQUIRED_FEATURE_MARKERS:
            if marker not in normalized_feature_body:
                errors.append(f"{relative(features)}: missing current feature marker: {marker}")

        spanish_features = SPANISH_DOCS / "overview" / "features.md"
        spanish_feature_body = spanish_features.read_text(errors="replace")
        for marker in ["ASCII World Mint", "ASCII City Nightshift", "Media Foundation", "V4L2"]:
            if marker not in spanish_feature_body:
                errors.append(f"{relative(spanish_features)}: missing current feature marker: {marker}")

    if icon_sha256:
        audit_icon(icon_sha256, errors)

    if DOCS.exists():
        release_guide = DOCS / "operations" / "release.md"
        release_body = release_guide.read_text() if release_guide.exists() else ""
        for marker in ["docs/RELEASING.md", "## Evidence and Release Records", "## Published-Artifact Acceptance"]:
            if marker not in release_body:
                errors.append(f"{relative(release_guide)}: missing canonical release guide marker: {marker}")
        quickstart = DOCS / "development" / "quickstart.md"
        quickstart_body = quickstart.read_text() if quickstart.exists() else ""
        if "npm ci" not in quickstart_body or "## First-Time Setup" not in quickstart_body:
            errors.append(f"{relative(quickstart)}: missing canonical contributor setup")
        features = DOCS / "overview" / "features.md"
        if "docs/USER_GUIDE.md" not in features.read_text():
            errors.append(f"{relative(features)}: missing canonical user guide attribution")
        roadmap = DOCS / "reference" / "roadmap.md"
        if not roadmap.exists():
            errors.append("docs/reference/roadmap.md is missing")
        else:
            body = roadmap.read_text(errors="replace")
            if "This document contains prospective work only." not in body:
                errors.append("docs/reference/roadmap.md: missing prospective-work contract")
            if re.search(r"^#{1,6}\s+.*\b0\.9\.[0-9]+\b", body, re.MULTILINE):
                errors.append("docs/reference/roadmap.md: contains a version-specific milestone heading")

    if SPANISH_DOCS.exists():
        roadmap = SPANISH_DOCS / "reference" / "roadmap.md"
        if not roadmap.exists():
            errors.append("es/docs/reference/roadmap.md is missing")
        else:
            body = roadmap.read_text(errors="replace")
            if "Este documento contiene únicamente trabajos prospectivos." not in body:
                errors.append("es/docs/reference/roadmap.md: missing prospective-work contract")
            if re.search(r"^#{1,6}\s+.*\b0\.9\.[0-9]+\b", body, re.MULTILINE):
                errors.append("es/docs/reference/roadmap.md: contains a version-specific milestone heading")

    if errors:
        print("Current-state documentation audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Current-state documentation audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
