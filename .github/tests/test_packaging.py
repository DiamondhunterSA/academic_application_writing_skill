"""Regression checks for collection installs, compatibility and read-only failures."""

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath, PureWindowsPath
from unittest.mock import patch


SKILL_NAMES = (
    "personal-statement",
    "inquiry-email",
    "application-review",
    "recommendation-letter",
)
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("repository_validator", SCRIPTS / "validate-repository.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
generator = validator.generator
readme = validator.readme
INFO = {"owner": "DiamondhunterSA", "repo": "academic_application_writing_skill",
        "url": "https://github.com/DiamondhunterSA/academic_application_writing_skill", "default_branch": "main"}


def snapshot(root):
    return {p.relative_to(root).as_posix(): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob("*") if p.is_file()}


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="academic-writing-test-")
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        for name in SKILL_NAMES:
            folder = self.root / "skills" / name
            (folder / "references").mkdir(parents=True)
            (folder / "assets").mkdir()
            (folder / "scripts").mkdir()
            (folder / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Help with {name}.\n---\n"
                "Read [guidance](references/guide.md). Use [helper](scripts/helper.py).\n",
                encoding="utf-8",
            )
            (folder / "references/guide.md").write_text("# Guidance\n", encoding="utf-8")
            (folder / "assets/example.bin").write_bytes(b"\x89\xff\0\r\n")
            (folder / "scripts/helper.py").write_text("print('helper')\n", encoding="utf-8")
        (self.root / "README.md").write_text(
            "# Collection\n\n<!-- SKILLS_TABLE_START -->\n<!-- SKILLS_TABLE_END -->\n", encoding="utf-8"
        )
        target = self.root / ".github/scripts"
        target.mkdir(parents=True)
        for script in SCRIPTS.glob("*.py"):
            shutil.copyfile(script, target / script.name)
        self.generate()

    def generate(self):
        artifacts = generator.build_artifacts(self.root, INFO)
        generator.write_artifacts(self.root, artifacts)
        path = self.root / "README.md"
        table = readme.generate_table(readme.get_skills(self.root / "skills"), INFO)
        path.write_bytes(readme.render_readme(path.read_text(encoding="utf-8"), table).encode("utf-8"))

    def run_script(self, script, *args):
        env = dict(os.environ, GITHUB_REPOSITORY="DiamondhunterSA/academic_application_writing_skill",
                   SKILLS_DEFAULT_BRANCH="main", PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run([sys.executable, "-B", str(self.root / ".github/scripts" / script), *args],
                              cwd=self.root.parent, env=env, capture_output=True, text=True)

    def test_collection_and_individual_install_ids_discover_the_expected_skills(self):
        source = snapshot(self.root / "skills")
        self.assertEqual(validator.validate_repository(self.root, INFO), [])
        marketplace = json.loads((self.root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "DiamondhunterSA-academic-application-writing")
        entries = {entry["name"]: entry for entry in marketplace["plugins"]}
        self.assertEqual(entries["academic-application-writing"]["source"], "./")
        for name in SKILL_NAMES:
            self.assertEqual(entries[name]["source"], f"./plugins/{name}")
            plugin = self.root / "plugins" / name
            self.assertEqual(validator.discover_skill_names(plugin), {name})
            instructions = (plugin / "README.md").read_text(encoding="utf-8")
            self.assertIn(f"{name}@{marketplace['name']}", instructions)
            self.assertEqual((plugin / "skills/assets/example.bin").read_bytes(), b"\x89\xff\0\r\n")
        self.assertEqual(validator.discover_skill_names(self.root), set(SKILL_NAMES))
        self.generate()
        self.assertEqual(source, snapshot(self.root / "skills"))

    def test_read_only_commands_leave_contents_and_timestamps_unchanged(self):
        before = snapshot(self.root)
        for script, args in (("generate-plugins.py", ("--check",)),
                             ("update-readme.py", ("--check",)),
                             ("validate-repository.py", ())):
            result = self.run_script(script, *args)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(before, snapshot(self.root))

    def test_invalid_distribution_fails_without_repairing_or_writing(self):
        copied = self.root / "plugins/inquiry-email/skills/references/guide.md"
        copied.write_text("stale\n", encoding="utf-8")
        before = snapshot(self.root)
        result = self.run_script("validate-repository.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("differs from source", result.stderr)
        self.assertEqual(before, snapshot(self.root))

    def test_broken_reference_missing_discovery_and_stale_index_are_reported(self):
        entry = self.root / "skills/inquiry-email/SKILL.md"
        entry.write_text(entry.read_text(encoding="utf-8") + "[Missing](references/missing.md)\n", encoding="utf-8")
        self.generate()
        manifest = self.root / "plugins/inquiry-email/.claude-plugin/plugin.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        del data["skills"]
        manifest.write_text(json.dumps(data), encoding="utf-8")
        index = self.root / "README.md"
        index.write_text(index.read_text(encoding="utf-8").replace("| Skill |", "| Outdated |"), encoding="utf-8")
        errors = validator.validate_repository(self.root, INFO)
        self.assertTrue(any("Broken local reference" in error for error in errors))
        self.assertTrue(any("Skill discovery mismatch" in error for error in errors))
        self.assertTrue(any("README skill index is stale" in error for error in errors))

    def test_versions_change_only_for_affected_skill_content_and_ignore_checkout_newlines(self):
        def versions():
            return {path.as_posix(): json.loads(data)["version"]
                    for path, data in generator.build_artifacts(self.root, INFO).items()
                    if path.name == "plugin.json"}
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                entry = self.root / "skills" / name / "SKILL.md"
                original = entry.read_bytes()
                initial = versions()
                try:
                    entry.write_bytes(original.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
                    self.assertEqual(initial, versions())
                    entry.write_bytes(entry.read_bytes() + b"New instructions.\r\n")
                    updated = versions()
                    changed = {path for path in initial if initial[path] != updated[path]}
                    self.assertEqual(changed, {
                        ".claude-plugin/plugin.json",
                        f"plugins/{name}/.claude-plugin/plugin.json",
                    })
                finally:
                    entry.write_bytes(original)

    def test_invalid_source_does_not_remove_existing_distributions(self):
        entry = self.root / "skills/inquiry-email/SKILL.md"
        entry.write_text("---\nname: wrong-name\ndescription: Test\n---\n", encoding="utf-8")
        before = snapshot(self.root)
        result = self.run_script("generate-plugins.py")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(before, snapshot(self.root))

    def test_versions_are_identical_for_windows_and_posix_path_ordering(self):
        windows = {PureWindowsPath("SKILL.md"): b"entry", PureWindowsPath("references/a.md"): b"reference"}
        posix = {PurePosixPath("SKILL.md"): b"entry", PurePosixPath("references/a.md"): b"reference"}
        self.assertEqual(generator.content_version({}, windows), generator.content_version({}, posix))

    def test_generation_cleans_stale_files_without_recreating_the_plugin_root(self):
        plugin_root = self.root / "plugins"
        identity = plugin_root.stat().st_ino
        stale = plugin_root / "inquiry-email/skills/references/old.md"
        stale.write_text("old", encoding="utf-8")
        self.assertTrue(any("Stale generated file" in error for error in validator.validate_repository(self.root, INFO)))
        self.generate()
        self.assertFalse(stale.exists())
        self.assertEqual(identity, plugin_root.stat().st_ino)
        self.assertEqual(validator.validate_repository(self.root, INFO), [])

    def test_repository_identity_defaults_and_overrides(self):
        expected_default = {key: INFO[key] for key in ("owner", "repo", "url")}
        expected_fork = {"owner": "example", "repo": "fork", "url": "https://github.com/example/fork"}
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(generator.subprocess, "run", side_effect=OSError("Git unavailable")):
                self.assertEqual(generator.get_repo_info(self.root), expected_default)
                self.assertEqual(readme.get_repo_info(), expected_default)
            remote = subprocess.CompletedProcess([], 0, stdout="git@github.com:example/fork.git\n")
            with patch.object(generator.subprocess, "run", return_value=remote):
                self.assertEqual(generator.get_repo_info(self.root), expected_fork)
                self.assertEqual(readme.get_repo_info(), expected_fork)
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "example/fork"}, clear=True):
            self.assertEqual(generator.get_repo_info(self.root), expected_fork)
            self.assertEqual(readme.get_repo_info(), expected_fork)

    def test_branch_override_and_encoded_homepage_preserve_release_configuration(self):
        with patch.dict(os.environ, {"SKILLS_DEFAULT_BRANCH": "main"}):
            self.assertEqual(generator.get_default_branch("master", self.root), "master")
            self.assertEqual(generator.get_default_branch(repo_root=self.root), "main")
        info = dict(INFO, default_branch="release/stable")
        manifest = generator.build_artifacts(self.root, info)[Path("plugins/inquiry-email/.claude-plugin/plugin.json")]
        self.assertIn("/tree/release%2Fstable/", json.loads(manifest)["homepage"])


if __name__ == "__main__":
    unittest.main()
