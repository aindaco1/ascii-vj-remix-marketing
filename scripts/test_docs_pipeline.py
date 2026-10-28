"""Offline regressions for source reorganization and localized cross-references."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from build_spanish_docs import known_translation, preserve_heading_links, protect_text, restore_text, rewrite_docs_links
from docs_common import public_docs

ROOT = Path(__file__).resolve().parents[1]
SYNC = ROOT / "scripts" / "sync_ascii_docs.rb"


def ruby(expression, value, source_ref="main"):
    result = subprocess.run(
        ["ruby", "-r", str(SYNC), "-e",
         f"input = JSON.parse($stdin.read); puts JSON.generate({expression})"],
        input=json.dumps(value), text=True, capture_output=True, check=True,
        env={**os.environ, "ASCII_VJ_SOURCE_REF": source_ref},
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
        source = "[Release](RELEASING.md#build-and-package) [Requirements](USER_GUIDE.md#system-requirements) [Shared](SHARED_DESKTOP_MIGRATION.md#shared-service-maintenance) [Spatial](USER_GUIDE.md#spatial-visuals-and-trails-110) [Accents](USER_GUIDE.md#fractal-accents)"
        result = ruby('SyncAsciiDocs.rewrite_links(input, "docs/AGENTS.md")', source)
        self.assertIn("/docs/operations/release/#build-and-package", result)
        self.assertIn("/docs/overview/ascii-vj-remix/#system-requirements", result)
        self.assertIn("/docs/development/shared-desktop-services/#shared-service-maintenance", result)
        self.assertIn("/docs/overview/features/#spatial-visuals-and-trails-110", result)
        self.assertIn("/docs/overview/features/#fractal-accents", result)
        result = ruby('SyncAsciiDocs.rewrite_links(input, "docs/USER_GUIDE.md", excerpt: true)',
                      "[Recovery](#upgrading-from-096-or-097)")
        self.assertIn("/blob/main/docs/USER_GUIDE.md#upgrading-from-096-or-097", result)

    def test_candidate_notes_do_not_replace_dated_release(self):
        changelog = "## [1.3.0] - Unreleased\n\nCandidate changes.\n\n## [1.2.0] - 2026-10-04\n\nPublished changes.\n"
        self.assertEqual(ruby("SyncAsciiDocs.upcoming_version(input)", changelog), "1.3.0")
        self.assertEqual(ruby("SyncAsciiDocs.released_version(input)", changelog), "1.2.0")
        self.assertEqual(ruby('SyncAsciiDocs.released_body(input, "1.2.0")', changelog), "Published changes.")
        self.assertEqual(ruby("SyncAsciiDocs.upcoming_notes(input)", changelog),
                         "## Upcoming 1.3.0 Release Notes\n\nCandidate changes.")
        published = changelog.replace("Unreleased", "2026-10-14")
        self.assertIsNone(ruby("SyncAsciiDocs.upcoming_version(input)", published))
        self.assertEqual(ruby("SyncAsciiDocs.upcoming_notes(input)", published), "")

    def test_source_links_use_imported_revision_and_local_sharing_anchor(self):
        revision = "a" * 40
        result = ruby('SyncAsciiDocs.rewrite_links(input, "docs/USER_GUIDE.md", excerpt: true)',
                      "[Sharing](#native-video-sharing) [Linux](#linux-ndi-sources-do-not-appear)",
                      source_ref=revision)
        self.assertIn("/docs/overview/features/#native-video-sharing", result)
        self.assertIn(f"/blob/{revision}/docs/USER_GUIDE.md#linux-ndi-sources-do-not-appear", result)
        self.assertNotIn("/blob/main/", result)

    def test_launch_target_selects_notes_without_inventing_publication_date(self):
        changelog = "## [1.3.0] - Unreleased\n\nNative video sharing.\n\n## [1.2.0] - 2026-10-04\n\nOlder notes.\n"
        self.assertEqual(ruby('SyncAsciiDocs.site_release_version(input, target: "1.3.0")', changelog), "1.3.0")
        self.assertEqual(ruby('SyncAsciiDocs.site_release_version(input, target: nil)', changelog), "1.2.0")
        self.assertEqual(ruby('SyncAsciiDocs.released_body(input, "1.3.0")', changelog), "Native video sharing.")
        self.assertEqual(ruby('SyncAsciiDocs.released_date(input, "1.3.0")', changelog), "")
        self.assertEqual(ruby('SyncAsciiDocs.release_copy(input, target: "1.3.0")',
                              "## [1.3.0] - Unreleased\n\nAvailable in the 1.3.0 candidate; see [release status](record)."),
                         "## [1.3.0]\n\nAdded in 1.3.0; see [release record](record).")

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

    def test_dated_release_normalizes_old_candidate_copy_only(self):
        value = {
            "changelog": "## [1.4.0] - Unreleased\n\n## [1.3.1] - 2026-10-21\n\n## [1.3.0] - 2026-10-13\n",
            "copy": "Available in the 1.3.0 candidate; see [release status](old).\nAvailable in the 1.4.0 candidate; see [release status](next).",
        }
        self.assertEqual(ruby('SyncAsciiDocs.site_release_version(input["changelog"], target: nil)', value), "1.3.1")
        self.assertEqual(ruby('SyncAsciiDocs.release_copy(input["copy"], target: nil, changelog: input["changelog"])', value),
                         "Added in 1.3.0; see [release record](old).\nAvailable in the 1.4.0 candidate; see [release status](next).")


class TranslationTests(unittest.TestCase):
    def test_pinned_links_reuse_reviewed_prose_before_cached_translation(self):
        base = "https://github.com/aindaco1/ascii-vj-remix/blob/"
        source = f"See [guide]({base}main/docs/USER_GUIDE.md#native-video-sharing)."
        translated = f"Consulta la [guía]({base}main/docs/USER_GUIDE.md#native-video-sharing)."
        pinned = source.replace("/main/", "/" + "a" * 40 + "/")
        with patch.dict("build_spanish_docs.REVIEWED_TRANSLATIONS", {source: translated}, clear=True), \
             patch.dict("build_spanish_docs.cache", {pinned: "Stale service wording"}, clear=True):
            self.assertEqual(known_translation(pinned), translated.replace("/main/", "/" + "a" * 40 + "/"))

    def test_video_transport_names_are_preserved(self):
        source = "NDI® Input, Syphon Input, Video I/O, NDI High Bandwidth"
        protected, tokens = protect_text(source)
        for term in ["NDI", "Syphon", "Video I/O"]:
            self.assertNotIn(term, protected)
        self.assertEqual(restore_text(protected, tokens), source)

    def test_cycling_preset_names_and_shared_packages_are_protected(self):
        source = "Tidal Glass, Ember Grotto, Fern After Rain, Violet Dusk, Jev, Dust Wave Platform, Test Core, Desktop Core, Release Core, Spatial ASCII, Flat Media, Bright output, Bright Output, Space / Motion, Neon Night Drive, Media Corridor, Wet Coast, Neon Cathedral, Orbital Chamber, Ashen Ruins, Fractal Dive, Mandelbulb Bloom, Mandelbox Passage, Edge Etching, Phosphor Echo, Brightness Relief, Fractal Accents, Subtle Limit, Threadlight, Silver Etching, Contour Silk, Julia Glass, Chromatic Undertow, Phosphor Lace, Another variation"
        protected, tokens = protect_text(source)
        self.assertNotIn("Tidal Glass", protected)
        self.assertNotIn("Desktop Core", protected)
        for term in source.split(", "):
            self.assertNotIn(term, protected)
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
