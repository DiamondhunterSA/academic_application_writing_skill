---
name: application-review
description: Review an academic application package or a supplied subset of its materials against program requirements and across documents. Use for final submission checks, cross-document fact checks, prompt coverage, and consistency or complementarity reviews of CVs, statements, research proposals, supplementary essays, and related application materials. Return prioritized findings with evidence and concrete fixes; standalone drafting or sentence-level polishing belongs to the relevant writing skill.
---

## Application Review

Help the applicant identify what needs correcting, confirming, or strengthening across an application package. Work from the supplied materials and applicable requirements. Follow **Gather → Map → Review → Report → Recheck**, compressing stages when the context is already available.

### Scope and Starting Point

- Start reviewing when enough material is available; do not require a separate intake or outline approval. Honor a narrower request such as "facts only," "requirements only," or "check the revised passages."
- Review the available subset even when the full package is unavailable. Separate "not supplied for review" from "required but missing from the application." One document can be checked against its prompt, but cross-document conclusions need the relevant comparison material.
- Review by default. Provide or apply revisions when requested, preserving the applicant's voice and confirmed facts. Resolve factual uncertainty before choosing one version for a rewrite.
- This skill works independently. If available and useful, `personal-statement` can handle substantial essay revisions and `inquiry-email` can handle inquiry drafts; neither is required to perform the review.

### Stage 1: Gather

**Goal:** Establish the target, review scope, and versions being assessed.

1. Reuse the supplied documents, program prompts, portal instructions, and applicant information. Existing `.claude/personal-statement-context.md` or `.claude/inquiry-email-context.md` may help if they exist and concern this applicant; treat them as dated context, not independent proof of a disputed fact.
2. Identify the target institution, program or opportunity, degree, application cycle, and any requested focus. For several applications, keep each target's requirements and document variants separate while reusing common applicant facts.
3. Inventory each supplied item by filename or a stable label, document type, target, and version/date if known. Distinguish current drafts, superseded drafts, translations, instructions, and supporting evidence. Ask which version is current only when it materially affects a finding; do not select by filename or modification time alone.
4. Ask only for information that changes the review, in batches of at most 2–3 questions. Continue checks that do not depend on the answers. Do not require confidential recommendation letters; applicant-provided support materials and known submission status can be reviewed without them.
5. State material access limits. An unreadable file, a text extract, or a missing portal view does not support conclusions about its full contents, rendering, or submission state.

**Exit condition:** The available materials and review target are identified, with any scope gaps recorded.

### Stage 2: Map

**Goal:** Establish what each material must do and which claims can be compared.

1. Build a working requirements map: target, document/prompt, required or optional status, requested content, limits and counting rules, submission constraints, source, and cycle/date where available. Mark unspecified fields unknown rather than filling them with typical admissions advice.
2. Use applicable official instructions and the actual prompt for requirements. Applicant-supplied facts establish background, not institutional rules. If current external facts are needed, verify through available tools and link the specific official source. If verification is unavailable or outside the user's requested scope, identify the unresolved check and proceed with the supplied evidence. Do not silently resolve conflicting instructions; identify their scope and ask for the relevant portal/program clarification when necessary.
3. Build a compact working fact map for repeated claims: identity, dates, affiliations, qualifications, project roles, methods, results, publications, and goals. Record where each claim appears and any dated evidence or applicant confirmation. This is a comparison aid, not a requirement to print a second full applicant profile.
4. Assign document roles using the actual prompts. Do not assume that a document titled "personal statement," "SOP," or "research statement" has a universal purpose or length.

**Exit condition:** Requirements, comparable claims, and unverified information are distinguishable.

### Stage 3: Review

**Goal:** Find material issues without converting assumptions into errors.

Read the relevant sections of [references/checks.md](references/checks.md) for the requested review. Work in this order unless the user specifies another priority:

1. **Requirements and completion:** required materials, every prompt component, target names, explicit limits, placeholders, and supported submission/attachment checks.
2. **Facts and attribution:** compare dates, project scope, personal versus team contributions, outcome metrics, and publication or degree status across the current materials. Check whether differences reflect a dated update, translation, scope, or measurement definition before calling them contradictory.
3. **Package coherence:** assess whether experiences support the stated goals and whether documents contribute useful evidence for their respective prompts. Reusing a project can be appropriate; flag repetition when it displaces required or complementary content.
4. **Program and research fit:** check that claimed connections are accurate and explained, and that research questions, methods, preparation, and proposed work align where relevant. Distinguish a verified program fact from an applicant's proposed plan or interpretation.
5. **Presentation:** check clarity, terminology, length, and visible formatting when accessible. Prioritize consequential problems over subjective wording preferences.

For every material finding, preserve the exact document location and a short excerpt or measured value. A conflict needs both sides; a requirements violation needs the applicable rule and the observed mismatch. An unsupported claim is unverified, not automatically false. Do not invent facts, citations, institutional requirements, or missing text to complete the assessment.

**Exit condition:** Findings are tied to evidence, with their priority and uncertainty identified.

### Stage 4: Report

**Goal:** Give the user an actionable review in their requested language and level of detail.

Use [references/reporting.md](references/reporting.md) for priority definitions, the adaptable report format, and examples of calibrated findings.

- Lead with the most consequential findings and the scope reviewed. Distinguish confirmed problems, unresolved checks, and optional improvements. Include coverage information sufficient to show which requirements were checked and which were not assessable.
- Give each finding a location, evidence, consequence, and concrete correction or verification action. Group repeated instances of the same root problem while naming the affected documents.
- Suggest replacement wording only when the facts are established; otherwise ask a focused factual question or show conditional alternatives. Keep review comments outside application-ready prose.
- Report observable readiness within the reviewed scope, not an admission probability, a universal application score, or a claim that acceptance or submission is guaranteed. A partial review cannot establish that the whole package is ready.

**Exit condition:** The user can see what to fix first, where to fix it, and what still needs checking.

### Stage 5: Recheck

**Goal:** Verify revisions against the original findings without reopening settled work unnecessarily.

1. Track findings as resolved, still open, or not rechecked; retain stable identifiers when a previous report exists. Close an issue only after inspecting the relevant revised passages or evidence.
2. Recheck affected requirements and cross-document dependencies. A corrected CV claim may also require changes to the statement and inquiry email; a new publication status may legitimately replace an earlier one.
3. Recount affected text after edits using the applicable method. Do not claim exact counts, page compliance, or successful upload without observing or measuring them.
4. Summarize remaining issues and review limits. If the user requests a saved report or revised files, use the requested location and preserve originals unless replacement is authorized. Reviewing materials does not authorize submitting applications or contacting recipients.

### Language Handling

Use the user's language for the review unless they request otherwise. Keep quotations and proposed edits in the document's intended language. For bilingual versions, compare meaning, factual scope, contribution, and certainty; different wording or length alone is not a conflict.

### Reference Materials

- Review criteria and document-specific checks: [references/checks.md](references/checks.md).
- Finding priorities, report structure, and worked examples: [references/reporting.md](references/reporting.md).
