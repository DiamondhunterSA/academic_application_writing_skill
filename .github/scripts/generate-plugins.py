#!/usr/bin/env python3
"""Generate the root collection plugin and backwards-compatible single-skill plugins."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import yaml


ROOT = Path(__file__).resolve().parents[2]
COLLECTION_NAME = "academic-application-writing"
COLLECTION_DESCRIPTION = (
    "Academic application writing skills for personal statements, inquiry emails, recommendation letters, and application package reviews. "
    "Install the collection to use every skill, or install individual skills separately."
)


def is_link(path: Path) -> bool:
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def normalized_bytes(data: bytes) -> bytes:
    """Ignore checkout line endings for UTF-8 text, preserving binary resources."""
    try:
        return data.decode("utf-8").replace("\r\n", "\n").encode("utf-8")
    except UnicodeDecodeError:
        return data


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def get_repo_info(repo_root: Path = ROOT) -> dict:
    repository = os.environ.get("GITHUB_REPOSITORY")
    if repository:
        owner, repo = repository.split("/", 1)
        return {"owner": owner, "repo": repo, "url": f"https://github.com/{repository}"}
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"], cwd=repo_root,
            capture_output=True, text=True, check=True,
        )
        url = result.stdout.strip().replace("git@github.com:", "https://github.com/")
        url = url.removesuffix(".git").rstrip("/")
        owner, repo = url.split("/")[-2:]
        return {"owner": owner, "repo": repo, "url": url}
    except (OSError, ValueError, subprocess.CalledProcessError):
        return {
            "owner": "DiamondhunterSA", "repo": "personal-statement-skill",
            "url": "https://github.com/DiamondhunterSA/personal-statement-skill",
        }


def get_default_branch(explicit: str | None = None, repo_root: Path = ROOT) -> str:
    branch = explicit or os.environ.get("SKILLS_DEFAULT_BRANCH")
    if branch and branch.strip():
        return branch.strip()
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"],
            cwd=repo_root, capture_output=True, text=True, encoding="utf-8", check=True,
        )
        branch = result.stdout.strip().removeprefix("origin/")
        if branch:
            return branch
    except (OSError, subprocess.CalledProcessError):
        pass
    raise ValueError("Cannot determine the default branch. Set SKILLS_DEFAULT_BRANCH or pass --default-branch.")


def get_skills(repo_root: Path) -> list[dict]:
    skills_root = repo_root / "skills"
    if is_link(skills_root):
        raise ValueError("skills/ must be a real directory, not a link")
    skills = []
    for folder in sorted(skills_root.iterdir()):
        if folder.name.startswith("."):
            continue
        if is_link(folder):
            raise ValueError(f"Linked skill directory: {folder.name}")
        if not folder.is_dir():
            continue
        entry = folder / "SKILL.md"
        if is_link(entry) or not entry.is_file():
            raise ValueError(f"Missing or linked SKILL.md: skills/{folder.name}")
        content = entry.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---(?:\n|$)", content, re.DOTALL)
        metadata = yaml.safe_load(match.group(1)) if match else None
        if not isinstance(metadata, dict):
            raise ValueError(f"Missing YAML frontmatter: skills/{folder.name}/SKILL.md")
        name, description = metadata.get("name"), metadata.get("description")
        if name != folder.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
            raise ValueError(f"Skill name must match its lowercase directory name: {folder.name}")
        if len(name) > 64 or name == COLLECTION_NAME:
            raise ValueError(f"Invalid or reserved skill name: {name}")
        if not isinstance(description, str) or not description.strip():
            raise ValueError(f"Missing skill description: {name}")
        files = {}
        for path in sorted(folder.rglob("*")):
            if is_link(path):
                raise ValueError(f"Linked skill resource: {path.relative_to(repo_root)}")
            if path.is_file():
                files[path.relative_to(folder)] = path.read_bytes()
        skills.append({"name": name, "description": description.strip(), "files": files})
    if not skills:
        raise ValueError("No skills found under skills/")
    return skills


def content_version(manifest: dict, files: dict[Path, bytes]) -> str:
    """Content-derived versions remain stable without Git history or across LF/CRLF."""
    digest = hashlib.sha256(json_bytes(manifest))
    for relative, data in sorted(files.items(), key=lambda item: item[0].as_posix()):
        digest.update(relative.as_posix().encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(normalized_bytes(data)).digest())
    return "0.2.0+" + digest.hexdigest()[:12]


def generate_readme(name: str, description: str, repo_info: dict) -> str:
    repository = f"{repo_info['owner']}/{repo_info['repo']}"
    marketplace = f"{repo_info['owner']}-skills"
    return f"""# {name}

{description}

## Installation

Run from the project where you want to use this skill.

### Claude Code

Install this skill with one command:

```bash
claude plugin install {name} --marketplace {repository} --scope project
```

Alternatively, add the marketplace and install the skill in two steps:

```bash
claude plugin marketplace add {repository}
claude plugin install {name}@{marketplace} --scope project
```

### npx skills

```bash
npx skills add {repository} --skill {name} -a claude-code -y
```

## Usage and collection

Invoke this skill with `/{name}:{name}`.
The `{COLLECTION_NAME}` collection includes this skill and the other skills in the repository.
Choose the collection or individual plugins for a project to avoid duplicate skill entries.

---

Generated from [skills/{name}](../../skills/{name}); edit the source skill there.
"""


def build_artifacts(repo_root: Path, repo_info: dict) -> dict[Path, bytes]:
    """Describe every generated file without touching the filesystem."""
    skills = get_skills(repo_root)
    common = {
        "author": {"name": repo_info["owner"], "url": repo_info["url"]},
        "repository": repo_info["url"], "license": "MIT",
    }
    collection = {
        "name": COLLECTION_NAME, "displayName": "Academic Application Writing",
        "description": COLLECTION_DESCRIPTION, **common,
        "homepage": repo_info["url"],
        "keywords": ["academic-writing", "applications"] + [skill["name"] for skill in skills],
    }
    collection_files = {
        Path("skills") / skill["name"] / relative: data
        for skill in skills for relative, data in skill["files"].items()
    }
    collection["version"] = content_version(collection, collection_files)
    artifacts = {Path(".claude-plugin/plugin.json"): json_bytes(collection)}
    entries = [{
        "name": COLLECTION_NAME, "source": "./", "description": COLLECTION_DESCRIPTION,
        "version": collection["version"], "category": "productivity",
    }]
    for skill in skills:
        name = skill["name"]
        plugin_root = Path("plugins") / name
        manifest = {
            "name": name, "description": skill["description"], **common,
            "homepage": f"{repo_info['url']}/tree/{quote(repo_info['default_branch'], safe='')}/plugins/{name}",
            "skills": ["./skills"],
        }
        manifest["version"] = content_version(manifest, skill["files"])
        artifacts[plugin_root / ".claude-plugin/plugin.json"] = json_bytes(manifest)
        artifacts[plugin_root / "README.md"] = generate_readme(name, skill["description"], repo_info).encode("utf-8")
        for relative, data in skill["files"].items():
            artifacts[plugin_root / "skills" / relative] = data
        entries.append({
            "name": name, "source": f"./plugins/{name}", "description": skill["description"],
            "version": manifest["version"], "category": "productivity",
        })
    marketplace = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": f"{repo_info['owner']}-skills",
        "description": "Academic application writing collection and individual skill plugins.",
        "owner": {"name": repo_info["owner"], "url": f"https://github.com/{repo_info['owner']}"},
        "plugins": entries,
    }
    artifacts[Path(".claude-plugin/marketplace.json")] = json_bytes(marketplace)
    return artifacts


def check_output_paths(repo_root: Path) -> None:
    for folder in (repo_root / "plugins", repo_root / ".claude-plugin"):
        if is_link(folder):
            raise ValueError(f"Generated directory must not be linked: {folder.name}")
        if folder.exists():
            for path in folder.rglob("*"):
                if is_link(path):
                    raise ValueError(f"Linked generated path: {path.relative_to(repo_root)}")


def artifact_errors(repo_root: Path, artifacts: dict[Path, bytes]) -> list[str]:
    check_output_paths(repo_root)
    errors = []
    for relative, expected in artifacts.items():
        path = repo_root / relative
        if not path.is_file():
            errors.append(f"Missing generated file: {relative.as_posix()}")
        elif normalized_bytes(path.read_bytes()) != normalized_bytes(expected):
            errors.append(f"Generated file differs from source/configuration: {relative.as_posix()}")
    plugins_root = repo_root / "plugins"
    if plugins_root.exists():
        for path in plugins_root.rglob("*"):
            if path.is_file() and path.relative_to(repo_root) not in artifacts:
                errors.append(f"Stale generated file: {path.relative_to(repo_root).as_posix()}")
    return errors


def write_artifacts(repo_root: Path, artifacts: dict[Path, bytes]) -> None:
    check_output_paths(repo_root)
    # Keep existing directories and their inherited Windows ACLs. Remove only stale files.
    plugins_root = repo_root / "plugins"
    if plugins_root.exists():
        if not plugins_root.resolve().is_relative_to(repo_root.resolve()) or plugins_root.resolve() == repo_root.resolve():
            raise ValueError("Generated plugin path escapes the repository")
        for path in plugins_root.rglob("*"):
            if path.is_file() and path.relative_to(repo_root) not in artifacts:
                path.unlink()
        for path in sorted(plugins_root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
    for relative, data in artifacts.items():
        target = repo_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file() or normalized_bytes(target.read_bytes()) != normalized_bytes(data):
            target.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--default-branch", help="CLI override; otherwise SKILLS_DEFAULT_BRANCH, then origin/HEAD")
    parser.add_argument("--check", action="store_true", help="Report stale generated files without writing")
    args = parser.parse_args()
    try:
        repo_info = get_repo_info()
        repo_info["default_branch"] = get_default_branch(args.default_branch)
        artifacts = build_artifacts(ROOT, repo_info)
        if args.check:
            errors = artifact_errors(ROOT, artifacts)
            for error in errors:
                print(error, file=sys.stderr)
            if errors:
                return 1
            print("Plugin artifacts are up to date (read-only check).")
        else:
            write_artifacts(ROOT, artifacts)
            print(f"Generated {COLLECTION_NAME} and {len(get_skills(ROOT))} standalone plugins.")
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
