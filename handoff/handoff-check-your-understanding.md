# Handoff — check-your-understanding skill

**Date:** 2025-07-15  
**Workspace:** `c:\Users\syonr\Documents\check-your-understanding`  
**Branch:** `main`

---

## What was built

A complete agentic pipeline skill called `check-your-understanding` that onboards a developer onto a codebase by:

1. Analysing the repo in the background
2. Running an adaptive questionnaire to profile the developer
3. Synthesising a personalised curriculum
4. Generating a Slidev presentation (interactive slides)
5. Appending a single check-your-understanding quiz at the end
6. Iterating on failed quiz questions by updating the affected slides with teaching notes and regenerating the deck (max 3 iterations)

---

## Skill entry point

`check-your-understanding/SKILL.md` — model-invokable skill with frontmatter. Triggers on: "onboard me", "check my understanding", "walk me through this repo", "generate onboarding slides".

The skill is a **6-phase pipeline**. All state is stored in `onboarding-session.json` in the session output directory, making it resumable mid-run.

---

## Pipeline phases

| Phase | Reference doc | Input | Output |
|---|---|---|---|
| 0 | (inline) | — | `onboarding-session.json` created or resumed |
| 1 — Understand repo (background) | `references/understand-repo.md` | Repo files | `repo_context` + `tech_tags` in session JSON |
| 2 — Questionnaire | `references/user-questionnaire.md` | `tech_tags` | `user_data.json` + `user_data` in session JSON |
| 3 — Teaching synthesis | `references/teaching-synthesis.md` | `repo_context` + `user_data` | `curriculum.slides` in session JSON |
| 4 — Generate quiz (parallel w/ 3) | `references/generate-quiz.md` | `curriculum.slides` | `quiz.questions` in session JSON |
| 5 — Build Slidev deck | `references/slidev-builder.md` | `curriculum.slides` + `quiz.questions` | `./slidev/` directory |
| 6 — Quiz + iterate | `references/iterate-on-failure.md` | `quiz_result` | Updated `teaching_notes` + regenerated `slidev/slides.md` |

Phases 1 and 2 overlap (Phase 1 runs in background; Phase 2 Layer 1 starts immediately; Layer 2 waits for `tech_tags`). Phases 3 and 4 are parallel.

---

## File inventory

All under `check-your-understanding/` in the workspace:

```
SKILL.md                          ← main pipeline skill (model-invokable)
schema/
  onboarding.schema.json          ← JSON Schema for onboarding-session.json
references/
  understand-repo.md              ← repo analysis methodology + coverage checklist
  user-questionnaire.md           ← 3-layer adaptive questionnaire spec
  teaching-synthesis.md           ← curriculum synthesis algorithm
  generate-quiz.md                ← quiz generation rules
  slidev-builder.md               ← Slidev output spec + Vue component specs
  iterate-on-failure.md           ← failure loop: teaching notes + deck regen
slidev/                           ← empty; created at runtime by Phase 5
```

A second copy of `onboarding.schema.json` was also written to `schema/onboarding.schema.json` at the workspace root.

---

## Key design decisions (do not reverse without reason)

- **One quiz per session.** The deck ends with exactly one quiz section. On failure, slides are updated but the quiz questions are never regenerated — the developer retakes the same questions against improved slides.
- **`tech_tags` drives everything.** The questionnaire Layer 2, curriculum depth, and quiz difficulty all pivot on the normalised `tech_tags` list from `repo_context`. Adding a new tag to the normalised list in `understand-repo.md` automatically propagates to all downstream phases.
- **`tech_familiarity` scale is 0–3.** 0 = never used, 3 = can teach. A tag at 3 is skipped in the curriculum and never tested in the quiz.
- **`onboarding-session.json` is the resumability contract.** Every phase checks its expected output field before running. Do not rename schema fields without updating the skill phases.
- **Iteration limit is 3.** After 3 quiz failures the pipeline appends a "recommended next step" slide and stops iterating.
- **Phase 1 runs in background.** The skill explicitly marks Phase 1 as background-runnable so agents that support concurrency can start repo analysis while identity questions are being asked.

---

## What is NOT yet built (next-session work)

1. **No real pipeline run yet.** The schema and reference docs exist but the full pipeline has not been executed against a real repo. First run will likely surface minor tweaks to reference docs.
2. **Slidev Vue components are spec'd but not pre-seeded.** `QuizQuestion.vue` and `QuizResult.vue` are defined in `slidev-builder.md` but not pre-generated. A starter implementation could be pre-seeded in `check-your-understanding/slidev/components/` to speed up Phase 5.
3. **No `AGENTS.md` pointer.** No Bob `AGENTS.md` entry exists to make this skill discoverable by directory-scoped agents.
4. **No example session fixture.** An example `onboarding-session.json` with fixture data would let slidev-builder and iterate-on-failure be tested in isolation without running the full pipeline.
5. **Background parallelism is aspirational.** In a single-threaded agent the "run in background" instruction in Phase 1 becomes sequential. The pipeline still works; only the concurrency benefit is lost.

---

## Suggested skills for next session

- `writing-for-agents` — if editing any reference doc or SKILL.md
- `prototype` — to build a fixture `onboarding-session.json` and test the slidev-builder phase in isolation
- `tdd` — to write integration tests around the pipeline phases
- `domain-modeling` — if the schema needs to grow (e.g. multi-session state, learning records)
- `implement` — to pre-seed the Vue components in `check-your-understanding/slidev/components/`
