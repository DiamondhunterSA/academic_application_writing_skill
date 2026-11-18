# Academic Application Writing

> A collection of independent skills for application writing and package review.

`academic-application-writing` bundles the repository's skills into one Claude Code plugin. Both Claude Code and `npx skills` use the source files under `skills/`. The GitHub repository is `DiamondhunterSA/personal-statement-skill`, and the marketplace is `DiamondhunterSA-skills`.

## Overview

The collection includes `personal-statement` for application essays, `inquiry-email` for academic and professional inquiries, `recommendation-letter` for academic references from mentors and instructors, and `application-review` for evidence-based checks across an application package. Inquiry emails support both background-and-fit and purpose-first approaches, selected using the user's request and relevant preferences.

The `personal-statement` skill provides a **5-stage writing assistant** across application contexts:

- **5-Stage Workflow** — Gather → Plan → Write → Polish → Iterate
- **10+ Discipline Templates** — Tailored guidance for CS, Engineering, Medicine, Law, Business, Humanities, and more
- **4 Reference Modules** — Frameworks, discipline-specific advice, annotated examples, and format templates
- **Multi-Language Support** — Bilingual parallel text, localized tone adaptation
- **Natural Writing Style** — Vocabulary and sentence-level guidance for clear, specific prose

### Supported Application Types

| Type | Typical Length | Key Focus |
|------|---------------|-----------|
| Graduate / Master's | 500–1000 words | Academic fit, career goals |
| PhD Program | 1000–2000 words | Research interest, advisor fit |
| Scholarship | 500–800 words | Merit, impact, potential |
| Job Application | 300–500 words | Skills, experience, role fit |
| Fellowship | 800–1500 words | Leadership, community impact |
| Motivation Letter (European) | 1–2 pages | Formal letter format |

### How It Works

The skill follows a structured **progressive disclosure** approach:

```
Stage 1: Gather    →  Collect context, CV, program requirements
Stage 2: Plan      →  Build content pillars, discipline-aligned outline
Stage 3: Write     →  Draft with "show don't tell", anti-AI tone
Stage 4: Polish    →  Grammar, flow, specificity, word count
Stage 5: Iterate   →  Targeted revision based on feedback
```

**Key Features:**
- **Context persistence** — Saves applicant info to `.claude/personal-statement-context.md` for reuse across multiple applications
- **Discipline alignment** — Automatically adapts guidance based on target field (CS emphasizes projects, Medicine emphasizes empathy + rigor, etc.)
- **Multi-application support** — Reuses confirmed applicant facts and adapts structure and content to each target's prompt and limits

## Quick Start

### Option 1: npx skills (CLI)

Run from the project where you want to use the skills. Install every skill into Claude Code without interactive selection:

```bash
npx skills add DiamondhunterSA/personal-statement-skill -s '*' -a claude-code -y
```

Use `--skill personal-statement`, `--skill inquiry-email`, `--skill recommendation-letter`, or `--skill application-review` to select one skill. Add `-g` for a user-wide npx installation, or `--copy` to copy files instead of using links. `--all` selects all agents as well as all skills; the command above targets Claude Code only.

### Option 2: Claude Code Plugin Marketplace

Install the entire collection with one command:

```bash
claude plugin install academic-application-writing --marketplace DiamondhunterSA/personal-statement-skill --scope project
```

Alternatively, add the marketplace and install the collection in two steps:

```bash
# Step 1: Add the marketplace
claude plugin marketplace add DiamondhunterSA/personal-statement-skill

# Step 2: Install the collection
claude plugin install academic-application-writing@DiamondhunterSA-skills --scope project
```

Start a new Claude session, or run `/reload-plugins`, then invoke a skill:

```text
/academic-application-writing:personal-statement
/academic-application-writing:inquiry-email
/academic-application-writing:recommendation-letter
/academic-application-writing:application-review
```

Choose one installation channel for a project. The npx installation exposes `/personal-statement`, `/inquiry-email`, `/recommendation-letter`, and `/application-review`. The collection plugin uses the namespaced commands above.

### Individual skill plugins

The marketplace also offers each skill as an independent, searchable plugin. Use the installation commands in the table below to select one skill. Their commands are `/personal-statement:personal-statement`, `/inquiry-email:inquiry-email`, `/recommendation-letter:recommendation-letter`, and `/application-review:application-review`.

Choose the collection or individual plugins for a project to avoid duplicate skill entries.

## Skills

<!-- SKILLS_TABLE_START -->

| Skill | Description |
|-------|-------------|
| [application-review](skills/application-review) | Review an academic application package or a supplied subset of its materials against program requirements and across documents. Use for final submission checks, cross-document fact checks, prompt coverage, and consistency or complementarity reviews of CVs, statements, research proposals, supplementary essays, and related application materials. Return prioritized findings with evidence and concrete fixes; standalone drafting or sentence-level polishing belongs to the relevant writing skill. |
| | `npx skills add DiamondhunterSA/personal-statement-skill --skill application-review -a claude-code -y` |
| | `claude plugin install application-review --marketplace DiamondhunterSA/personal-statement-skill --scope project` |
| [inquiry-email](skills/inquiry-email) | Draft, revise, and personalize inquiry emails (including enquiry emails and academic outreach) to prospective supervisors, research groups, admissions or funding offices, and contacts for research or professional opportunities. Use for initial inquiries, follow-ups, or replies in an inquiry thread; full application essays, cover letters, and unrelated marketing or customer-support email are outside this skill's focus. |
| | `npx skills add DiamondhunterSA/personal-statement-skill --skill inquiry-email -a claude-code -y` |
| | `claude plugin install inquiry-email --marketplace DiamondhunterSA/personal-statement-skill --scope project` |
| [personal-statement](skills/personal-statement) | Assist in writing, structuring, and polishing personal statements and self-introductions. Use for drafting or revising a PS, personal statement, self-introduction, application essay, motivation letter, statement of purpose, cover letter, or personal bio for study abroad, graduate/PhD admissions, scholarships, jobs, or similar applications. Package-wide requirements and cross-document consistency reviews are outside this skill's focus. |
| | `npx skills add DiamondhunterSA/personal-statement-skill --skill personal-statement -a claude-code -y` |
| | `claude plugin install personal-statement --marketplace DiamondhunterSA/personal-statement-skill --scope project` |
| [recommendation-letter](skills/recommendation-letter) | Draft, revise, and personalize academic recommendation letters, letters of reference, and LoRs in the first-person voice of a project supervisor, research supervisor, course instructor, or another academic mentor. Use for full letters, recommender questionnaire responses, translations, and distinct letters from several recommenders supporting graduate, PhD, scholarship, fellowship, or research applications. Ground each draft in the recommender's relationship, observations, and supplied evidence. |
| | `npx skills add DiamondhunterSA/personal-statement-skill --skill recommendation-letter -a claude-code -y` |
| | `claude plugin install recommendation-letter --marketplace DiamondhunterSA/personal-statement-skill --scope project` |

<!-- SKILLS_TABLE_END -->

## Skill Architecture

### Reference Modules

The `personal-statement` skill includes 4 reference modules loaded on demand for token efficiency. The `inquiry-email` skill has its own frameworks, formats and examples under `skills/inquiry-email/references/`. The `recommendation-letter` skill loads recommender roles and letter or questionnaire formats from `skills/recommendation-letter/references/`. The `application-review` skill loads review criteria and reporting guidance from `skills/application-review/references/` as needed.

| Module | File | Content |
|--------|------|---------|
| **Frameworks** | `references/frameworks.md` | Content Pillars framework, format templates by scenario |
| **Discipline** | `references/discipline.md` | 10+ fields with specific guidance, key questions, and pitfalls |
| **Examples** | `references/examples.md` | Annotated paragraphs, before/after comparisons, opening/closing techniques |
| **Templates** | `references/post-templates.md` | Structural skeletons for essay, formal letter, SoP, and Q&A formats |

### Progressive Disclosure

```
Always loaded:    Skill metadata (name, description, activation criteria)
On activation:    Core 5-stage workflow instructions
On demand:        Reference modules (frameworks, discipline, examples, templates)
```

This keeps token usage minimal — reference materials are only loaded when the relevant stage needs them.

## Usage Examples

### Start from Scratch

```
"Help me write a personal statement for a CS Master's at CMU"
```

The skill starts from the available context and gathers the information needed for the requested draft.

### Polish an Existing Draft

```
"Here's my personal statement draft, please help me polish it: [paste draft]"
```

Jumps directly to Stage 4 (Polish) with grammar, flow, and specificity checks.

### Multiple Applications

```
"I need to adapt my PS for both MIT and Stanford"
```

Reuses confirmed facts and adapts the structure, examples, program fit, and future plans to each prompt.

### Draft Academic Recommendations

```
"Write an English PhD recommendation letter from my research supervisor's perspective.
Use these shared research experiences, their feedback, and my CV.
Also prepare a separate letter from my course instructor using the coursework evidence."
```

`recommendation-letter` follows Gather → Plan → Write → Polish → Iterate. It drafts complete first-person letters and referee questionnaire responses using each recommender's relationship, observations, and supplied evaluation. Project supervisors, research supervisors, course instructors, and mentors with combined roles have role-specific guidance. Applicant-prepared drafts include a short review note outside the letter for the recommender.

### Review an Application Package

```
"Review my CV, SOP, and research proposal against these program requirements.
Prioritize factual inconsistencies, unanswered prompts, and submission limits.
Give me evidence and a concrete fix for each issue; do not rewrite the documents."
```

`application-review` follows Gather → Map → Review → Report → Recheck. It distinguishes confirmed problems, checks that need verification, and optional improvements. It can review a supplied subset without treating unseen materials as missing from the application; substantial drafting stays with the writing skills.

## Project Structure

```
.
├── .claude-plugin/
│   ├── plugin.json              # academic-application-writing collection
│   └── marketplace.json         # Root collection + standalone plugin entries
├── .github/
│   ├── scripts/                 # CI/CD automation scripts
│   │   ├── generate-plugins.py   # Collection metadata + standalone distributions
│   │   ├── update-readme.py      # Generate the skill index
│   │   └── validate-repository.py # Read-only release checks
│   ├── tests/                   # Packaging and validation regression tests
│   └── workflows/               # GitHub Actions workflows
│       └── generate-plugins.yml # Generate plugins and README together
├── skills/                      # Skill source files (edit here)
│   ├── application-review/       # SKILL.md + references/
│   ├── personal-statement/       # SKILL.md + references/
│   ├── recommendation-letter/    # SKILL.md + references/
│   └── inquiry-email/            # SKILL.md + references/
├── plugins/                     # Generated individual plugin packages
│   ├── application-review/
│   ├── personal-statement/
│   ├── recommendation-letter/
│   └── inquiry-email/
└── README.md
```

### Two Distribution Channels

| Channel | How It Works | Install Command |
|---------|-------------|-----------------|
| **npx skills** | Install all or selected source skills | `npx skills add DiamondhunterSA/personal-statement-skill -s '*' -a claude-code -y` |
| **Claude collection** | Marketplace source `./` loads the root `skills/` directly | `claude plugin install academic-application-writing --marketplace DiamondhunterSA/personal-statement-skill --scope project` |
| **Claude standalone** | Generated `plugins/<name>/` keeps the original individual entry | `claude plugin install personal-statement --marketplace DiamondhunterSA/personal-statement-skill --scope project` |

### CI/CD Automation

The single `generate-plugins.yml` workflow watches pushes and pull requests. Feature branches and pull requests run the packaging tests and read-only repository validation. The generation job runs only on the repository's actual default branch; it can also be dispatched manually on that branch.

The job generates collection metadata and standalone plugins, updates the README index, and validates the result. It commits `plugins/`, both root `.claude-plugin/` manifests, and `README.md` together in one write-back, using write permission only for that default-branch job. Runs for the same workflow and branch are serialized without cancelling an active run.

Before committing, the job compares the remote branch head with the checked-out commit. If the branch has advanced, it logs a notice and skips the write-back. A later race fails through a normal push; the job does not rebase or force older generated files over newer source changes.

Generated homepage links follow the repository's default branch.

## Contributing

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/my-new-skill/`)
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and skill instructions
3. Optionally add a `references/` directory for supporting materials
4. Keep the generated manifests, individual plugin packages and README skill index consistent with the source.
5. Submit a pull request. CI checks the skills and generated files; the default-branch workflow maintains the derived artifacts.

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

## License

MIT
