#!/usr/bin/env python3
"""Read-only checks for plugin discovery, references, generated files and the README index."""

import sys

sys.dont_write_bytecode = True

import argparse
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_script(filename: str):
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_"), Path(__file__).parent / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generator = load_script("generate-plugins.py")
readme = load_script("update-readme.py")


def discover_skill_names(plugin_root: Path) -> set[str]:
    """Check the documented default layout and explicitly declared skill directories."""
    manifest = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    directories = [(plugin_root / "skills", False)]
    declared = manifest.get("skills", [])
    if isinstance(declared, str):
        declared = [declared]
    for relative in declared:
        directory = (plugin_root / relative).resolve()
        if not directory.is_relative_to(plugin_root.resolve()):
            raise ValueError(f"Skill directory escapes plugin: {relative}")
        if not directory.is_dir():
            raise ValueError(f"Declared skill directory is missing: {relative}")
        directories.append((directory, True))
    entries = set()
    for directory, explicit in directories:
        if not directory.is_dir():
            continue
        if explicit and (directory / "SKILL.md").is_file():
            entries.add(directory / "SKILL.md")
        else:
            entries.update(child / "SKILL.md" for child in directory.iterdir()
                           if child.is_dir() and (child / "SKILL.md").is_file())
    names = set()
    for entry in entries:
        metadata = readme.parse_frontmatter(entry.read_text(encoding="utf-8"))
        name = metadata.get("name")
        if not isinstance(name, str) or not name:
            raise ValueError(f"Missing skill name: {entry}")
        if name in names:
            raise ValueError(f"Duplicate discovered skill: {name}")
        names.add(name)
    return names


def reference_errors(repo_root: Path, files: list[Path]) -> list[str]:
    errors = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", text)
        for raw in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", text):
            match = re.match(r'\s*(?:<([^>]+)>|([^\s]+))', raw)
            if not match:
                continue
            target = match.group(1) or match.group(2)
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            local = unquote(url.path)
            destination = (repo_root / local.lstrip("/") if local.startswith("/") else path.parent / local).resolve()
            if not destination.is_relative_to(repo_root.resolve()) or not destination.exists():
                errors.append(f"Broken local reference in {path.relative_to(repo_root).as_posix()}: {target}")
    return errors


def validate_repository(repo_root: Path, repo_info: dict) -> list[str]:
    errors = []
    skills = generator.get_skills(repo_root)
    artifacts = generator.build_artifacts(repo_root, repo_info)
    errors.extend(generator.artifact_errors(repo_root, artifacts))
    if (repo_root / "SKILL.md").exists():
        errors.append("Root SKILL.md duplicates the source skill discovery; keep entrypoints under skills/<name>/.")
    locations = [(repo_root, {skill["name"] for skill in skills})]
    locations.extend((repo_root / "plugins" / skill["name"], {skill["name"]}) for skill in skills)
    for plugin_root, expected_names in locations:
        try:
            found = discover_skill_names(plugin_root)
            if found != expected_names:
                errors.append(f"Skill discovery mismatch at {plugin_root.relative_to(repo_root)}: expected {sorted(expected_names)}, found {sorted(found)}")
        except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
            errors.append(f"Cannot discover skills at {plugin_root.relative_to(repo_root)}: {error}")
    markdown = list((repo_root / "skills").rglob("*.md")) + list((repo_root / "plugins").rglob("*.md"))
    root_readme = repo_root / "README.md"
    if root_readme.is_file():
        markdown.append(root_readme)
        table = readme.generate_table(readme.get_skills(repo_root / "skills"), repo_info)
        content = root_readme.read_text(encoding="utf-8")
        if readme.render_readme(content, table) != content:
            errors.append("README skill index is stale; run .github/scripts/update-readme.py.")
    else:
        errors.append("Missing README.md")
    errors.extend(reference_errors(repo_root, markdown))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--default-branch", help="CLI override for the published branch")
    args = parser.parse_args()
    try:
        repo_info = generator.get_repo_info()
        repo_info["default_branch"] = generator.get_default_branch(args.default_branch)
        errors = validate_repository(ROOT, repo_info)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as error:
        errors = [str(error)]
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    count = len(generator.get_skills(ROOT))
    print(f"Validation passed: {count} source skills, root collection, {count} standalone plugins, local references and README index. No files written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
