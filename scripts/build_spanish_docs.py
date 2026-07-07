#!/usr/bin/env python3

from __future__ import annotations

import re
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import loads
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen



ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "docs"
TARGET_DIR = ROOT / "es" / "docs"

SECTION_TITLES = {
    "Overview": "Resumen",
    "Development": "Desarrollo",
    "Operations": "Operaciones",
    "Reference": "Referencia",
}

TITLE_OVERRIDES = {
    "ASCII VJ Remix": "ASCII VJ Remix",
    "Feature Set": "Conjunto de funciones",
    "Release Baseline": "Base de la versión",
    "Quickstart": "Inicio rápido",
    "Architecture": "Arquitectura",
    "Rendering Engine": "Motor de renderizado",
    "Contributing": "Cómo contribuir",
    "Agent Guide": "Guía para agentes",
    "Security": "Seguridad",
    "Performance": "Rendimiento",
    "Testing": "Pruebas",
    "Accessibility": "Accesibilidad",
    "Internationalization": "Internacionalización",
    "Release and Updates": "Lanzamiento y actualizaciones",
    "Commands": "Comandos",
    "Roadmap": "Hoja de ruta",
    "Changelog": "Registro de cambios",
    "Source Map": "Mapa de fuentes",
}

BODY_OVERRIDES = {
    "# Overview": "# Resumen",
    "# Development": "# Desarrollo",
    "# Operations": "# Operaciones",
    "# Reference": "# Referencia",
    "## Source Material": "## Material de origen",
}

MONTH_OVERRIDES = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "July": "julio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre",
}

cache: dict[str, str] = {}
TRANSLATE_SEPARATOR = "\nZXQZXQASCII_VJBREAKZXQZXQ\n"
TRANSLATE_MAX_CHARS = int(os.environ.get("ASCII_VJ_TRANSLATE_MAX_CHARS", "1200"))
TRANSLATE_TIMEOUT_SECONDS = float(os.environ.get("ASCII_VJ_TRANSLATE_TIMEOUT_SECONDS", "15"))
TRANSLATE_RETRIES = int(os.environ.get("ASCII_VJ_TRANSLATE_RETRIES", "3"))


def protect_text(text: str) -> tuple[str, list[str]]:
    working = text
    placeholders: list[str] = []

    def protect(pattern: str, value: str) -> str:
        def replacer(match: re.Match[str]) -> str:
            token = f"ZZTOKEN{len(placeholders)}ZZ"
            placeholders.append(match.group(0))
            return token

        return re.sub(pattern, replacer, value)

    working = protect(r"`[^`]+`", working)
    working = protect(r"\{\{.*?\}\}", working)
    working = protect(r"\{%.*?%\}", working)
    protected_terms = [
        "ASCII VJ Remix",
        "ASCILINE",
        "Tauri",
        "Vite",
        "Rust",
        "JavaScript",
        "TypeScript",
        "WebGPU",
        "WebGL2",
        "Canvas2D",
        "Pixel Canvas",
        "Pop Out",
        "WTF mode",
        "MIDI",
        "FFmpeg",
        "AVFoundation",
        "Metal",
        "D3D12",
        "Vulkan",
        "GLES",
        "WebView2",
        "WebKitGTK",
        "Cloudflare Worker",
        "GitHub",
        "GitHub Releases",
        "Jekyll",
        "macOS",
        "Windows",
        "Linux",
        "RMS",
        "IPC",
        "GPU",
        "CPU",
        "FPS",
        "MKV",
    ]
    for term in protected_terms:
        working = protect(rf"\b{re.escape(term)}\b", working)
    working = protect(r"\]\((?:https?://|/|mailto:)[^)]+\)", working)
    working = protect(r"https?://\S+", working)
    working = protect(r"mailto:\S+", working)
    return working, placeholders


def restore_text(text: str, placeholders: list[str]) -> str:
    restored = text
    for index, original in enumerate(placeholders):
        restored = restored.replace(f"ZZTOKEN{index}ZZ", original)
    restored = restored.replace("Mezcla ASCII VJ", "ASCII VJ Remix")
    restored = restored.replace("Remix ASCII VJ", "ASCII VJ Remix")
    restored = restored.replace("ASCII VJ Remezcla", "ASCII VJ Remix")
    return restored



def translate_date_line(text: str) -> str | None:
    match = re.fullmatch(r"([A-Za-z]+) ([0-9]{1,2}), ([0-9]{4})", text.strip())
    if not match:
        return None

    month, day, year = match.groups()
    translated_month = MONTH_OVERRIDES.get(month)
    if translated_month is None:
        return None

    return f"{int(day)} de {translated_month} de {year}"


def translate_texts(texts: list[str]) -> list[str]:
    translated = ["" for _ in texts]
    pending_values = []
    pending_meta = []

    for index, text in enumerate(texts):
        stripped = text.strip()
        if not stripped:
            translated[index] = text
            continue

        translated_date = translate_date_line(stripped)
        if translated_date is not None:
            translated[index] = translated_date
            continue

        if stripped in TITLE_OVERRIDES:
            translated[index] = TITLE_OVERRIDES[stripped]
            continue

        if stripped in SECTION_TITLES:
            translated[index] = SECTION_TITLES[stripped]
            continue

        if stripped in cache:
            translated[index] = cache[stripped]
            continue

        protected, placeholders = protect_text(stripped)
        pending_values.append(protected)
        pending_meta.append((index, stripped, placeholders))

    if pending_values:
        start = 0
        while start < len(pending_values):
            end = start
            chunk_length = 0

            while end < len(pending_values):
                value = pending_values[end]
                separator_length = len(TRANSLATE_SEPARATOR) if end > start else 0
                if end > start and chunk_length + separator_length + len(value) > TRANSLATE_MAX_CHARS:
                    break
                chunk_length += separator_length + len(value)
                end += 1

            chunk_values = pending_values[start:end]
            chunk_meta = pending_meta[start:end]
            joined = TRANSLATE_SEPARATOR.join(chunk_values)
            params = urlencode(
                [
                    ("client", "gtx"),
                    ("sl", "en"),
                    ("tl", "es"),
                    ("dt", "t"),
                    ("q", joined),
                ]
            )
            url = f"https://translate.googleapis.com/translate_a/single?{params}"

            last_error = None
            payload = None
            for attempt in range(TRANSLATE_RETRIES):
                try:
                    with urlopen(url, timeout=TRANSLATE_TIMEOUT_SECONDS) as response:
                        payload = loads(response.read().decode("utf-8"))
                    break
                except Exception as error:  # noqa: BLE001
                    last_error = error
                    if attempt == TRANSLATE_RETRIES - 1:
                        raise
                    time.sleep(min(2**attempt, 5))

            if payload is None and last_error is not None:
                raise last_error

            translated_joined = "".join(part[0] for part in payload[0])
            batch = translated_joined.split(TRANSLATE_SEPARATOR)

            if len(batch) != len(chunk_values):
                raise RuntimeError("Spanish docs translation batch returned an unexpected segment count")

            for (index, stripped, placeholders), value in zip(chunk_meta, batch):
                restored = restore_text(value, placeholders)
                translated[index] = restored
                cache[stripped] = restored

            start = end

    return translated


def translate_text(text: str) -> str:
    return translate_texts([text])[0]


def translate_table_row(line: str) -> str:
    parts = line.split("|")
    cells = []
    translatable_indexes = []

    for index, part in enumerate(parts):
        cells.append(part)
        if part and not re.fullmatch(r"\s*:?-{2,}:?\s*", part):
            translatable_indexes.append(index)

    translated_cells = translate_texts([parts[index] for index in translatable_indexes])
    for index, value in zip(translatable_indexes, translated_cells):
        cells[index] = value
    return "|".join(cells)


def rewrite_docs_links(text: str) -> str:
    text = text.replace("](/docs/", "](/es/docs/")
    text = text.replace("(/docs/", "(/es/docs/")
    text = text.replace('href="/docs/', 'href="/es/docs/')
    text = text.replace('"/docs/', '"/es/docs/')
    text = text.replace(" /docs/", " /es/docs/")
    return text


def translate_line(line: str) -> str:
    if re.match(r"^#{1,6}\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/\S+", line):
        return line

    if line in BODY_OVERRIDES:
        return BODY_OVERRIDES[line]

    if re.fullmatch(r"\s*", line):
        return line

    if line.startswith("|"):
        return rewrite_docs_links(translate_table_row(line))

    patterns = [
        r"^(#{1,6}\s+)(.+)$",
        r"^(\s*[-*+]\s+)(.+)$",
        r"^(\s*\d+\.\s+)(.+)$",
        r"^(>\s+)(.+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            return rewrite_docs_links(match.group(1) + translate_text(match.group(2)))

    return rewrite_docs_links(translate_text(line))


def translate_body(body: str) -> str:
    translated_lines = []
    in_fence = False
    fence_marker = ""
    pending_texts: list[str] = []
    pending_prefixes: list[str] = []

    def flush_pending() -> None:
        if not pending_texts:
            return

        for prefix, value in zip(pending_prefixes, translate_texts(pending_texts)):
            translated_lines.append(rewrite_docs_links(prefix + value))

        pending_texts.clear()
        pending_prefixes.clear()

    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            flush_pending()
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            translated_lines.append(line)
            continue

        if in_fence:
            translated_lines.append(line)
            continue

        if re.match(r"^#{1,6}\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/\S+", line):
            flush_pending()
            translated_lines.append(line)
            continue

        if line in BODY_OVERRIDES:
            flush_pending()
            translated_lines.append(BODY_OVERRIDES[line])
            continue

        if re.fullmatch(r"\s*", line):
            flush_pending()
            translated_lines.append(line)
            continue

        if line.startswith("|"):
            flush_pending()
            translated_lines.append(rewrite_docs_links(translate_table_row(line)))
            continue

        patterns = [
            r"^(#{1,6}\s+)(.+)$",
            r"^(\s*[-*+]\s+)(.+)$",
            r"^(\s*\d+\.\s+)(.+)$",
            r"^(>\s+)(.+)$",
        ]

        matched = False
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                pending_prefixes.append(match.group(1))
                pending_texts.append(match.group(2))
                matched = True
                break

        if matched:
            continue

        pending_prefixes.append("")
        pending_texts.append(line)

    flush_pending()
    return "\n".join(translated_lines) + "\n"


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def dump_scalar(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if re.search(r"[:#\[\]{}&*!|>'\"%@`]", text):
        return '"' + text.replace('"', '\\"') + '"'
    return text


def load_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    _, front_matter, body = text.split("---\n", 2)
    data = {}
    for line in front_matter.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data, body


def dump_page(data: dict, body: str) -> str:
    front_matter = "\n".join(f"{key}: {dump_scalar(value)}" for key, value in data.items())
    return f"---\n{front_matter}\n---\n{body}"


def translate_page(path: Path) -> None:
    relative_path = path.relative_to(SOURCE_DIR)
    target_path = TARGET_DIR / relative_path
    target_path.parent.mkdir(parents=True, exist_ok=True)

    data, body = load_front_matter(path.read_text())

    if "title" in data:
        data["title"] = translate_text(str(data["title"])).strip()

    if "description" in data:
        data["description"] = translate_text(str(data["description"])).strip()

    if "parent" in data:
        parent = str(data["parent"])
        data["parent"] = SECTION_TITLES.get(parent, translate_text(parent).strip())

    data["lang"] = "es"

    translated_body = translate_body(body)
    target_path.write_text(dump_page(data, translated_body))


def main() -> int:
    if not SOURCE_DIR.exists():
        print("docs/ directory not found", file=sys.stderr)
        return 1

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    requested_files = {
        value.strip()
        for value in os.environ.get("ASCII_VJ_TRANSLATION_FILES", "").split(",")
        if value.strip()
    }

    paths = sorted(SOURCE_DIR.rglob("*.md"))
    if requested_files:
        paths = [
            path
            for path in paths
            if str(path.relative_to(ROOT)) in requested_files
            or str(path.relative_to(SOURCE_DIR)) in requested_files
        ]

    max_workers = max(1, int(os.environ.get("ASCII_VJ_TRANSLATION_WORKERS", "1")))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(translate_page, path): path for path in paths}
        for future in as_completed(futures):
            future.result()

    print(f"Built Spanish docs in {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
