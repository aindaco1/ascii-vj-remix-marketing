"""Shared scope for generated, public documentation (both locales)."""

from pathlib import Path


def public_docs(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*.md")
        if path.relative_to(root).parts[0] != "maintenance"
        and path.read_text().startswith("---\n")
    )
