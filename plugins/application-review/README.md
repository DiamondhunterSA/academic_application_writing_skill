# application-review

Review an academic application package or a supplied subset of its materials against program requirements and across documents. Use for final submission checks, cross-document fact checks, prompt coverage, and consistency or complementarity reviews of CVs, statements, research proposals, supplementary essays, and related application materials. Return prioritized findings with evidence and concrete fixes; standalone drafting or sentence-level polishing belongs to the relevant writing skill.

## Installation

Run from the project where you want to use this skill.

### Claude Code

Install this skill with one command:

```bash
claude plugin install application-review --marketplace DiamondhunterSA/academic_application_writing_skill --scope project
```

Alternatively, add the marketplace and install the skill in two steps:

```bash
claude plugin marketplace add DiamondhunterSA/academic_application_writing_skill
claude plugin install application-review@DiamondhunterSA-academic-application-writing --scope project
```

### npx skills

```bash
npx --yes skills add DiamondhunterSA/academic_application_writing_skill --skill application-review --agent claude-code --yes
```

## Usage and collection

Invoke this skill with `/application-review:application-review`.
The `academic-application-writing` collection includes this skill and the other skills in the repository.
Choose the collection or individual plugins for a project to avoid duplicate skill entries.

---

Generated from [skills/application-review](../../skills/application-review); edit the source skill there.
