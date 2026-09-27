"""Offline regressions for source reorganization and localized cross-references."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from build_spanish_docs import preserve_heading_links, protect_text, restore_text, rewrite_docs_links
from docs_common import public_docs

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "sync_ascii_docs.rb"


def ruby(expression, value):
    result = subprocess.run(
        ["ruby", "-r", str(SYNC), "-e",
         f"input = JSON.parse($stdin.read); puts JSON.generate({expression})"],
        input=json.dumps(value), text=True, capture_output=True, check=True,
    )
    return json.loads(result.stdout)


class SourceSyncTests(unittest.TestCase):
    def test_commands_parse_only_scripts_and_keep_escaped_values(self):
        package = {"devDependency": "not a command", "scripts": {
            "bundle:test": 'node build.mjs --name "Dev"',
            "midi:probe": "node probe.mjs | cat",
            "media:preview": "node preview.mjs media/point-click-test-30s.mp4",
        }}
        rows = ruby("SyncAsciiDocs.command_rows(input)", json.dumps(package))
        self.assertEqual(len(rows), 3)
        self.assertIn('node build.mjs --name "Dev"', rows[0])
        self.assertIn(r"probe.mjs \| cat", rows[1])
        self.assertIn("media/<bundled-test-fixture>.mp4", rows[2])

    def test_release_badge_requires_a_dated_entry(self):
        changelog = "## [Unreleased]\n\n## [2.0.0] - Unreleased\n\n## [1.0.3] - 2026-09-02\n"
        self.assertEqual(ruby("SyncAsciiDocs.released_version(input)", changelog), "1.0.3")
        with self.assertRaises(subprocess.CalledProcessError):
            ruby("SyncAsciiDocs.released_version(input)", "## [Unreleased]\n")

    def test_reorganized_and_excerpted_links(self):
        source = "[Release](RELEASING.md#build-and-package) [Requirements](USER_GUIDE.md#system-requirements) [Shared](SHARED_DESKTOP_MIGRATION.md#shared-service-maintenance)"
        result = ruby('SyncAsciiDocs.rewrite_links(input, "docs/AGENTS.md")', source)
        self.assertIn("/docs/operations/release/#build-and-package", result)
        self.assertIn("/docs/overview/ascii-vj-remix/#system-requirements", result)
        self.assertIn("/docs/development/shared-desktop-services/#shared-service-maintenance", result)
        result = ruby('SyncAsciiDocs.rewrite_links(input, "docs/USER_GUIDE.md", excerpt: true)',
                      "[Recovery](#upgrading-from-096-or-097)")
        self.assertIn("/blob/main/docs/USER_GUIDE.md#upgrading-from-096-or-097", result)

    def test_missing_section_does_not_partially_write_output(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "site"
            source = Path(temp) / "source"
            (project / "scripts").mkdir(parents=True)
            shutil.copyfile(SYNC, project / "scripts" / SYNC.name)
            files = ruby("SOURCE_FILES.values", None)
            for filename in files:
                target = source / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# Fixture\n")
            (source / "README.md").write_text("# Product\n\n## What This Project Is\n\nIdentity.\n")
            (source / "CHANGELOG.md").write_text("## [1.0.3] - 2026-09-02\n\nReleased.\n")
            (source / "package.json").write_text('{"scripts":{"dev":"vite"}}')
            icon = source / "src-tauri/icons/icon.png"
            icon.parent.mkdir(parents=True)
            icon.write_bytes(b"new icon")
            sentinels = ["docs/index.md", "_data/product.yml", "assets/images/ascii-vj-remix-app-icon.png"]
            for filename in sentinels:
                target = project / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("original")
            result = subprocess.run(
                ["ruby", str(project / "scripts" / SYNC.name)],
                env={**os.environ, "ASCII_VJ_SOURCE": str(source)},
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Missing section "System Requirements" in docs/USER_GUIDE.md', result.stderr)
            for filename in sentinels:
                self.assertEqual((project / filename).read_text(), "original")


class TranslationTests(unittest.TestCase):
    def test_cycling_preset_names_and_shared_packages_are_protected(self):
        source = "Tidal Glass, Ember Grotto, Fern After Rain, Violet Dusk, Jev, Dust Wave Platform, Test Core, Desktop Core, Release Core"
        protected, tokens = protect_text(source)
        self.assertNotIn("Tidal Glass", protected)
        self.assertNotIn("Desktop Core", protected)
        self.assertEqual(restore_text(protected, tokens), source)

    def test_maintenance_never_enters_public_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ["index.md", "development/index.md", "maintenance/README.md"]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('---\ntitle: "Guide"\n---\n# Guide\n')
            self.assertEqual([str(path.relative_to(root)) for path in public_docs(root)],
                             ["development/index.md", "index.md"])

    def test_translation_preserves_internal_and_external_fragments(self):
        source = "[Checks](/docs/operations/testing/#recommended-check-sets) [Source](https://github.com/example/docs#release-and-updater-work) [Local](#quick-reference)"
        protected, tokens = protect_text(source)
        self.assertEqual(restore_text(protected, tokens), source)
        result = rewrite_docs_links(source)
        self.assertIn("/es/docs/operations/testing/#recommended-check-sets", result)
        self.assertIn("https://github.com/example/docs#release-and-updater-work", result)

    def test_heading_aliases_use_actual_markdown_ids_and_skip_code(self):
        english = "# Guide\n\n## MIDI, UC-33e, or SysEx Changes\n\n```text\n# Example\n```\n\n## Guide\n"
        spanish = "# Guía\n\n## Cambios MIDI, UC-33e o SysEx\n\n```text\n# Example\n```\n\n## Guía\n"
        result = preserve_heading_links(english, spanish)
        self.assertIn('<a id="midi-uc-33e-or-sysex-changes"></a>', result)
        self.assertIn('<a id="guide-1"></a>', result)
        self.assertNotIn('id="example"', result)
        self.assertIn("## Guía", result)  # Preserve native translated heading IDs too.

    def test_same_heading_id_is_not_duplicated(self):
        result = preserve_heading_links("# MIDI\n", "# MIDI\n")
        self.assertNotIn("<a ", result)

    def test_missing_translated_heading_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "heading structure"):
            preserve_heading_links("# Guide\n\n## Setup\n", "# Guía\n")


if __name__ == "__main__":
    unittest.main()
