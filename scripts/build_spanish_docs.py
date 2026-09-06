#!/usr/bin/env python3

from __future__ import annotations

import os
import re
import sys
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from json import dumps, loads
from pathlib import Path
from threading import Lock, get_ident
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen
from docs_common import public_docs

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
    "### Added": "### Añadido",
    "### Changed": "### Cambiado",
    "### Fixed": "### Corregido",
    "### Performance": "### Rendimiento",
    "### Security": "### Seguridad",
    "### Validation": "### Validación",
    "### Preserved": "### Conservado",
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

CACHE_DIR = ROOT / ".translation-cache"
CACHE_PATH = CACHE_DIR / "spanish-docs.json"
REVIEWED_TRANSLATIONS_PATH = ROOT / "scripts" / "spanish-docs-overrides.json"
REVIEWED_TRANSLATIONS = loads(REVIEWED_TRANSLATIONS_PATH.read_text())
TRANSLATE_SEPARATOR = "\nZXQZXQASCII_VJBREAKZXQZXQ\n"
TRANSLATE_PRIMARY_ENDPOINT = "https://translate.googleapis.com/translate_a/single"
TRANSLATE_FALLBACK_ENDPOINT = "https://clients5.google.com/translate_a/t"
TRANSLATE_MAX_CHARS = int(os.environ.get("ASCII_VJ_TRANSLATE_MAX_CHARS", "1200"))
TRANSLATE_TIMEOUT_SECONDS = float(os.environ.get("ASCII_VJ_TRANSLATE_TIMEOUT_SECONDS", "15"))
TRANSLATE_RETRIES = int(os.environ.get("ASCII_VJ_TRANSLATE_RETRIES", "8"))
TRANSLATE_REQUEST_DELAY_SECONDS = float(
    os.environ.get("ASCII_VJ_TRANSLATE_REQUEST_DELAY_SECONDS", "1")
)
TRANSLATE_RETRY_MAX_DELAY_SECONDS = float(
    os.environ.get("ASCII_VJ_TRANSLATE_RETRY_MAX_DELAY_SECONDS", "60")
)
cache_lock = Lock()


def load_translation_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        value = loads(CACHE_PATH.read_text())
    except (OSError, ValueError):
        return {}
    if not isinstance(value, dict):
        return {}
    return {str(key): str(item) for key, item in value.items()}


def save_translation_cache_unlocked() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    temporary = CACHE_PATH.with_name(
        f"{CACHE_PATH.stem}.{os.getpid()}.{get_ident()}.tmp"
    )
    temporary.write_text(dumps(cache, ensure_ascii=False, sort_keys=True))
    temporary.replace(CACHE_PATH)


cache: dict[str, str] = load_translation_cache()


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
        "Apple WebKit",
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
        "Unicode",
        "Bayer",
        "Braille",
        "CJK",
        "Hiragana",
        "Katakana",
        "Hangul",
        "Advanced Density",
        "Demo Image",
        "Demo Video",
        "Reports",
        "Update",
        "Stats Overlay",
        "MIDI Learn",
        "SysEx",
        "Ensure Profile on Connection",
        "soft takeover",
        "Classic Camera ASCII",
        "Point & Click Default",
        "Dense Color ASCII",
        "Built-in",
        "My Presets",
        "Atlas Style",
        "Auto",
        "ANSI Newsprint",
        "Terminal Mono",
        "Dense Typewriter",
        "Neon Sledgehammer",
        "Gamma Sinkhole",
        "Chrome Wound",
        "Candy Fragmenter",
        "Paper Shredder",
        "Cyberdelic Riot",
        "Acid Snowstorm",
        "Terminal Collapse",
        "Neon Razorstorm",
        "ASCII World Mint",
        "ASCII City Nightshift",
        "City Nightshift",
        "Media Foundation",
        "DirectShow",
        "V4L2",
    ]
    for term in protected_terms:
        working = protect(rf"\b{re.escape(term)}\b", working)
    # Keep source filenames and repository-relative paths verbatim in labels as
    # well as URLs. Translating these labels makes otherwise valid references
    # look like different files.
    working = protect(
        r"(?<![\w/])(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.(?:css|html|js|json|lock|md|mjs|py|rb|rs|scss|sh|toml|ts|tsx|yaml|yml)(?![\w/])",
        working,
    )
    working = protect(r"\]\((?:https?://|/|mailto:|#)[^)]+\)", working)
    working = protect(r"https?://\S+", working)
    working = protect(r"mailto:\S+", working)
    return working, placeholders


def restore_text(text: str, placeholders: list[str]) -> str:
    restored = text
    # Link placeholders can contain earlier protected terms. Restore the outer
    # placeholders first so nested tokens are present when their turn arrives.
    for index in range(len(placeholders) - 1, -1, -1):
        original = placeholders[index]
        restored = restored.replace(f"ZZTOKEN{index}ZZ", original)
    restored = restored.replace("Mezcla ASCII VJ", "ASCII VJ Remix")
    restored = restored.replace("Remix ASCII VJ", "ASCII VJ Remix")
    restored = restored.replace("ASCII VJ Remezcla", "ASCII VJ Remix")
    return polish_translation(restored)


def polish_translation(text: str) -> str:
    """Normalize recurring technical phrases, including values loaded from cache."""
    replacements = {
        "GitHub publica metadatos": "metadatos de GitHub Releases",
        "GitHub Publica metadatos": "metadatos de GitHub Releases",
        "MIDI Aprenda": "MIDI Learn",
        "MIDI Learn anulaciones": "Anulaciones de MIDI Learn",
        "abrazaderas seguras": "límites de seguridad",
        "Las límites de seguridad": "Los límites de seguridad",
        "barandillas de densidad": "límites de densidad",
        "barreras de densidad": "límites de densidad",
        "una matriz de humo": "una matriz de pruebas de humo",
        "el humo de rendimiento": "la prueba de humo de rendimiento",
        "El humo de rendimiento": "La prueba de humo de rendimiento",
        "un humo de regresión": "una prueba de humo de regresión",
        "UI empaquetado": "UI empaquetada",
        "extiende el humo de la interfaz de usuario empaquetado": "amplía la prueba de humo de la interfaz empaquetada",
        "rampas con tipos personalizados de hasta 96 compatibles. Escalares Unicode": "rampas personalizadas de hasta 96 escalares Unicode compatibles",
        "adquisición suave": "soft takeover",
        "toma de control, selección numérica": "soft takeover, selección numérica",
        "un ícono de aplicación canónica": "un icono canónico de la aplicación",
        "lleva la corrección de aceptación posterior a 0.9.9 Reports": "incorpora la corrección de aceptación de Reports posterior a 0.9.9",
        "antes de enviar una bifurcación].": "antes de publicar una bifurcación.",
        "[Operations]": "[Operaciones]",
        "[La referencia]": "[Referencia]",
        "docs/ACCESIBILIDAD.md": "docs/ACCESSIBILITY.md",
        "paquete.json": "package.json",
        "secciones integradas y Mis preajustes separadas": "secciones Built-in y My Presets separadas",
        "Integrado y Mis ajustes preestablecidos se muestran como secciones": "Built-in y My Presets se muestran como secciones",
        "El nombre para mostrar predeterminado anterior de apuntar y hacer clic ahora es el color ASCII denso, más descriptivo": "El nombre anterior Point & Click Default ahora se muestra como Dense Color ASCII",
        "y se cambió el nombre de la etiqueta de visualización predeterminada de apuntar y hacer clic a Color denso ASCII sin cambiar su identificación preestablecida estable.": "y Point & Click Default ahora se muestra como Dense Color ASCII sin cambiar su identificador estable de preset.",
        "La barra lateral estandarizada selecciona anchos, alturas, columnas de etiquetas, espacio entre filas y presentación de valores; Se eliminó": "Se estandarizaron los anchos y alturas de los selectores, las columnas de las etiquetas, el espaciado entre filas y la presentación de valores; se eliminó",
        "Etiquetado Advanced Density con su `Up to 900 columns` y sin restricción de garantía 30-FPS directamente en la fila de control.": "Se etiquetó Advanced Density con su límite de `Up to 900 columns` y la advertencia de que no garantiza 30 FPS directamente en la fila de control.",
        "una rampa escalar máxima activa": "una rampa activa de hasta 96 escalares",
        "la rampa escalar máxima activa": "la rampa activa de hasta 96 escalares",
        "formato de superficie no normal no sRGB": "formato de superficie unorm no sRGB",
        "un contrato Canvas centralizado de 69 en total / 41 acelerado / 28 explícito": "un contrato centralizado de 69 presets en total / 41 acelerados / 28 explícitos de Canvas2D",
        "Un contrato Canvas centralizado de 69 en total / 41 acelerado / 28 explícito": "Un contrato centralizado de 69 presets en total / 41 acelerados / 28 explícitos de Canvas2D",
        "Las funciones integradas que no solicitan": "Los presets integrados que no solicitan",
        "41 elementos integrados en WebGPU": "41 presets integrados en WebGPU",
        "a través del paquete FFmpeg": "a través de FFmpeg incluido",
    }
    polished = text
    for source, replacement in replacements.items():
        polished = polished.replace(source, replacement)
    return polished

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

        if stripped in REVIEWED_TRANSLATIONS:
            translated[index] = REVIEWED_TRANSLATIONS[stripped]
            continue

        with cache_lock:
            cached = cache.get(stripped)
        if cached is not None:
            translated[index] = polish_translation(cached)
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
            primary_params = urlencode(
                [
                    ("client", "gtx"),
                    ("sl", "en"),
                    ("tl", "es"),
                    ("dt", "t"),
                    ("q", joined),
                ]
            )
            fallback_params = urlencode(
                [
                    ("client", "dict-chrome-ex"),
                    ("sl", "en"),
                    ("tl", "es"),
                    ("q", joined),
                ]
            )
            primary_url = f"{TRANSLATE_PRIMARY_ENDPOINT}?{primary_params}"
            fallback_url = f"{TRANSLATE_FALLBACK_ENDPOINT}?{fallback_params}"
            url = primary_url

            last_error = None
            payload = None
            for attempt in range(TRANSLATE_RETRIES):
                try:
                    with urlopen(url, timeout=TRANSLATE_TIMEOUT_SECONDS) as response:
                        payload = loads(response.read().decode("utf-8"))
                    if TRANSLATE_REQUEST_DELAY_SECONDS > 0:
                        time.sleep(TRANSLATE_REQUEST_DELAY_SECONDS)
                    break
                except Exception as error:  # noqa: BLE001
                    last_error = error
                    if isinstance(error, HTTPError) and error.code == 429 and url == primary_url:
                        url = fallback_url
                        continue
                    if attempt == TRANSLATE_RETRIES - 1:
                        raise
                    delay = min(2**attempt, TRANSLATE_RETRY_MAX_DELAY_SECONDS)
                    if isinstance(error, HTTPError) and error.code == 429:
                        retry_after = error.headers.get("Retry-After")
                        if retry_after:
                            try:
                                delay = max(delay, float(retry_after))
                            except ValueError:
                                pass
                    time.sleep(delay)

            if payload is None and last_error is not None:
                raise last_error

            if url == fallback_url:
                if not isinstance(payload, list) or not payload or not isinstance(payload[0], str):
                    raise RuntimeError("Spanish docs fallback translation returned an unexpected payload")
                translated_joined = payload[0]
            else:
                translated_joined = "".join(part[0] for part in payload[0])
            batch = translated_joined.split(TRANSLATE_SEPARATOR)

            if len(batch) != len(chunk_values):
                raise RuntimeError("Spanish docs translation batch returned an unexpected segment count")

            cache_updates: dict[str, str] = {}
            for (index, stripped, placeholders), value in zip(chunk_meta, batch):
                restored = restore_text(value, placeholders)
                translated[index] = restored
                cache_updates[stripped] = restored

            with cache_lock:
                cache.update(cache_updates)
                save_translation_cache_unlocked()

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


def coalesce_markdown_lines(body: str) -> str:
    """Join hard-wrapped prose before translation while preserving Markdown blocks."""
    lines = body.splitlines()
    output: list[str] = []
    index = 0
    in_fence = False
    fence_marker = ""
    prefixed_block = re.compile(r"^(\s*(?:[-*+]\s+|\d+\.\s+|>\s+))(.+)$")

    def is_structural(line: str) -> bool:
        stripped = line.lstrip()
        return (
            not stripped
            or stripped.startswith(("```", "~~~"))
            or line.startswith("|")
            or re.match(r"^#{1,6}\s+", line) is not None
            or prefixed_block.match(line) is not None
        )

    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip()

        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            output.append(line)
            index += 1
            continue

        if in_fence or not stripped or line.startswith("|") or re.match(r"^#{1,6}\s+", line):
            output.append(line)
            index += 1
            continue

        match = prefixed_block.match(line)
        prefix = match.group(1) if match else ""
        parts = [match.group(2).strip() if match else stripped]
        cursor = index + 1
        while cursor < len(lines) and not is_structural(lines[cursor]):
            parts.append(lines[cursor].strip())
            cursor += 1

        output.append(prefix + " ".join(parts))
        index = cursor

    return "\n".join(output) + "\n"


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

    for line in coalesce_markdown_lines(body).splitlines():
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


def preserve_heading_links(english: str, spanish: str) -> str:
    """Keep English fragment links valid alongside native Spanish heading IDs."""
    result = subprocess.run(
        ["bundle", "exec", "ruby", str(ROOT / "scripts" / "docs_heading_ids.rb")],
        input=dumps([english, spanish]), text=True, capture_output=True,
        check=True, cwd=ROOT,
    )
    english_ids, spanish_ids = loads(result.stdout)
    if len(english_ids) != len(spanish_ids):
        raise ValueError("Translation changed the Markdown heading structure")

    output = []
    heading_index = 0
    fence = ""
    for line in spanish.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = "" if fence == marker else (fence or marker)
        elif not fence and re.match(r"^#{1,6}\s+", line):
            source_id = english_ids[heading_index]
            if source_id not in spanish_ids:
                output.extend([f'<a id="{source_id}"></a>', ""])
            heading_index += 1
        output.append(line)
    if heading_index != len(english_ids):
        raise ValueError("Unsupported Markdown heading layout for translated aliases")
    return "\n".join(output) + "\n"


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

    translated_body = preserve_heading_links(body, translate_body(body))
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

    paths = public_docs(SOURCE_DIR)
    if requested_files:
        paths = [
            path
            for path in paths
            if str(path.relative_to(ROOT)) in requested_files
            or str(path.relative_to(SOURCE_DIR)) in requested_files
        ]

    paths.sort(key=lambda path: (path.stat().st_size, str(path)))

    max_workers = max(1, int(os.environ.get("ASCII_VJ_TRANSLATION_WORKERS", "1")))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(translate_page, path): path for path in paths}
        for future in as_completed(futures):
            future.result()

    print(f"Built Spanish docs in {TARGET_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
