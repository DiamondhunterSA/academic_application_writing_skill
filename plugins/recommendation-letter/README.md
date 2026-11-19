# recommendation-letter

Draft, revise, and personalize academic recommendation letters, letters of reference, and LoRs in the first-person voice of a project supervisor, research supervisor, course instructor, or another academic mentor. Use for full letters, recommender questionnaire responses, translations, and distinct letters from several recommenders supporting graduate, PhD, scholarship, fellowship, or research applications. Ground each draft in the recommender's relationship, observations, and supplied evidence.

## Installation

Run from the project where you want to use this skill.

### Claude Code

Install this skill with one command:

```bash
claude plugin install recommendation-letter --marketplace DiamondhunterSA/academic_application_writing_skill --scope project
```

Alternatively, add the marketplace and install the skill in two steps:

```bash
claude plugin marketplace add DiamondhunterSA/academic_application_writing_skill
claude plugin install recommendation-letter@DiamondhunterSA-academic-application-writing --scope project
```

### npx skills

```bash
npx --yes skills add DiamondhunterSA/academic_application_writing_skill --skill recommendation-letter --agent claude-code --yes
```

## Usage and collection

Invoke this skill with `/recommendation-letter:recommendation-letter`.
The `academic-application-writing` collection includes this skill and the other skills in the repository.
Choose the collection or individual plugins for a project to avoid duplicate skill entries.

---

Generated from [skills/recommendation-letter](../../skills/recommendation-letter); edit the source skill there.
