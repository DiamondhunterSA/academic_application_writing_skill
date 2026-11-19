#!/usr/bin/env python3
"""Update README.md with a table of skills from the skills directory."""

import argparse
import os
import re
import subprocess
from pathlib import Path

import yaml


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)) or {}
    return {}


def get_skills(skills_dir: Path) -> list[dict]:
    """Get all skills from the skills directory."""
    skills = []

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir() or skill_path.name.startswith("."):
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        if "description" in frontmatter:
            name = frontmatter.get("name", skill_path.name).strip().replace(" ", "-").lower()
            skills.append({
                "name": name,
                "dir_name": skill_path.name,
                "description": frontmatter["description"],
            })

    return sorted(skills, key=lambda s: s["name"].lower())


def get_repo_info() -> dict:
    """Get repository info from environment or git remote."""
    github_repository = os.environ.get("GITHUB_REPOSITORY")
    if github_repository:
        owner, repo = github_repository.split("/", 1)
        return {"owner": owner, "repo": repo, "url": f"https://github.com/{github_repository}"}

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=Path(__file__).resolve().parents[2],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
        parts = url.rstrip("/").split("/")
        return {"owner": parts[-2], "repo": parts[-1], "url": url}
    except Exception:
        return {"owner": "DiamondhunterSA", "repo": "academic_application_writing_skill", "url": "https://github.com/DiamondhunterSA/academic_application_writing_skill"}


def generate_table(skills: list[dict], repo_info: dict) -> str:
    """Generate a markdown table of skills."""
    owner_repo = f"{repo_info['owner']}/{repo_info['repo']}"

    lines = [
        "| Skill | Description |",
        "|-------|-------------|",
    ]

    for skill in skills:
        skill_link = f"[{skill['name']}](skills/{skill['dir_name']})"
        description = skill["description"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {skill_link} | {description} |")
        npx_cmd = f'`npx --yes skills add {owner_repo} --skill {skill["name"]} --agent claude-code --yes`'
        lines.append(f"| | {npx_cmd} |")
        plugin_cmd = f'`claude plugin install {skill["name"]} --marketplace {owner_repo} --scope project`'
        lines.append(f"| | {plugin_cmd} |")

    return "\n".join(lines)


def render_readme(content: str, table: str) -> str:
    """Render the index without writing, so validation uses the same formatting."""
    start_marker = "<!-- SKILLS_TABLE_START -->"
    end_marker = "<!-- SKILLS_TABLE_END -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if content.count(start_marker) != 1 or content.count(end_marker) != 1 or end_idx <= start_idx:
        raise ValueError("README.md must contain <!-- SKILLS_TABLE_START --> and <!-- SKILLS_TABLE_END --> markers")

    return (
        content[:start_idx + len(start_marker)]
        + "\n\n"
        + table
        + "\n\n"
        + content[end_idx:]
    )

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check the README index without writing")
    args = parser.parse_args()
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "skills"
    readme_path = repo_root / "README.md"

    repo_info = get_repo_info()
    skills = get_skills(skills_dir)
    table = generate_table(skills, repo_info)
    content = readme_path.read_text(encoding="utf-8")
    rendered = render_readme(content, table)
    if args.check:
        if content != rendered:
            parser.exit(1, "README skill index is stale. Run .github/scripts/update-readme.py.\n")
        print("README skill index is up to date (read-only check).")
    else:
        if content != rendered:
            readme_path.write_bytes(rendered.encode("utf-8"))
        print(f"Updated README.md with {len(skills)} skills")


if __name__ == "__main__":
    main()
