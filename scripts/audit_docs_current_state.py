#!/usr/bin/env python3
"""Reject stale or aspirational claims in generated current-state documentation."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SPANISH_DOCS = ROOT / "es" / "docs"
CURRENT_STATE_EXCLUSIONS = {
    DOCS / "reference" / "changelog.md",
    DOCS / "reference" / "roadmap.md",
}
SPANISH_CURRENT_STATE_EXCLUSIONS = {
    SPANISH_DOCS / "reference" / "changelog.md",
    SPANISH_DOCS / "reference" / "roadmap.md",
}

FORBIDDEN_CURRENT_STATE = {
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


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def audit_tree(
    docs_root: Path,
    exclusions: set[Path],
    patterns: dict[str, re.Pattern[str]],
    errors: list[str],
) -> None:
    if not docs_root.exists():
        errors.append(f"{relative(docs_root)} directory is missing")
        return
    for path in sorted(docs_root.rglob("*.md")):
        if path in exclusions:
            continue
        body = path.read_text(errors="replace")
        for label, pattern in patterns.items():
            match = pattern.search(body)
            if match:
                line = body.count("\n", 0, match.start()) + 1
                errors.append(f"{relative(path)}:{line}: {label}")


def main() -> int:
    errors: list[str] = []
    audit_tree(DOCS, CURRENT_STATE_EXCLUSIONS, FORBIDDEN_CURRENT_STATE, errors)
    audit_tree(
        SPANISH_DOCS,
        SPANISH_CURRENT_STATE_EXCLUSIONS,
        FORBIDDEN_SPANISH_CURRENT_STATE,
        errors,
    )

    if DOCS.exists():
        roadmap = DOCS / "reference" / "roadmap.md"
        if not roadmap.exists():
            errors.append("docs/reference/roadmap.md is missing")
        else:
            body = roadmap.read_text(errors="replace")
            if "This document contains prospective work only." not in body:
                errors.append("docs/reference/roadmap.md: missing prospective-work contract")
            if re.search(r"\b0\.9\.[0-9]+\b", body):
                errors.append("docs/reference/roadmap.md: contains a stale version-specific milestone")

    if SPANISH_DOCS.exists():
        roadmap = SPANISH_DOCS / "reference" / "roadmap.md"
        if not roadmap.exists():
            errors.append("es/docs/reference/roadmap.md is missing")
        else:
            body = roadmap.read_text(errors="replace")
            if "Este documento contiene únicamente trabajos prospectivos." not in body:
                errors.append("es/docs/reference/roadmap.md: missing prospective-work contract")
            if re.search(r"\b0\.9\.[0-9]+\b", body):
                errors.append("es/docs/reference/roadmap.md: contains a stale version-specific milestone")

    if errors:
        print("Current-state documentation audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Current-state documentation audit passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
