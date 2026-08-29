---
name: check-your-understanding
description: >
  Onboard a developer onto a codebase: analyse the repo, interview the developer,
  synthesise a personalised curriculum, generate an offline interactive HTML
  learning module with a quiz, and iterate the module on failure.
  Triggers on: "onboard me", "check my understanding", "walk me through this repo",
  "generate onboarding slides".
argument-hint: "Path to the repo to onboard onto (defaults to current directory)"
---

Onboard one developer onto one codebase in a single session. State is stored in `onboarding/onboarding-session.json`; every phase reads from and writes to that file so the pipeline is resumable.

## Phase 0 — Locate or create the session file

Create the `onboarding/` directory if it does not exist. Look for `onboarding/onboarding-session.json`.

- If absent: create it as `{}` and run all phases from Phase 1.
- If present: read it and check which phases have already produced output (non-null fields). Skip completed phases; resume from the first incomplete one.

## Phase 1 — Understand the repo

**Run in background** (this phase can be started immediately and run concurrently with Phase 2 if `repo_context` is absent).

Read [`references/understand-repo.md`](references/understand-repo.md) and follow it to produce `repo_context`. Done when all 13 coverage flags are `true` and every required `repo_context.guide_facts` category contains source-backed facts.

If `repo_context` already exists, check the coverage flags and `guide_facts`. Re-run only the investigation needed for false flags or missing guide categories; do not repeat the complete repository analysis.

## Phase 2 — Questionnaire

**Requires:** `repo_context.tech_tags` (wait for Phase 1 to produce them before starting Layer 2).

Read [`references/user-questionnaire.md`](references/user-questionnaire.md) and conduct the three-layer questionnaire interactively. Write answers to `onboarding/user_data.json` and into `onboarding/onboarding-session.json`.

Done when `user_data` is present and `task_context.goal` is non-empty.

## Phase 3 — Teaching synthesis

**Requires:** `repo_context` (all coverage flags `true`) + `user_data`.

Read [`references/teaching-synthesis.md`](references/teaching-synthesis.md) and produce `curriculum.slides`. Write into `onboarding/onboarding-session.json`.

Done when `curriculum.slides` contains between 5 and 20 teaching slides with no quiz-introduction slide, and `curriculum.guide.tabs` contains the compact project-guide tabs. If slides already exist but the guide is missing, generate only `curriculum.guide`; preserve the existing slides.

## Phase 4 — Generate quiz

**Requires:** `curriculum.slides`.

Read [`references/generate-quiz.md`](references/generate-quiz.md) and produce `quiz`. Write into `onboarding/onboarding-session.json`.

Done when `quiz.questions` has between 5 and 12 items, every question has a `slide_ref`, and `pass_threshold` is set.

> Phases 3 and 4 may run in parallel once Phase 2 is complete.

## Phase 5 — Build offline learning module

**Requires:** `repo_context.guide_facts` + `curriculum.slides` + `curriculum.guide` + `quiz.questions`.

Read [`references/html-builder.md`](references/html-builder.md) and run the deterministic builder. Never synthesize the HTML, CSS, JavaScript, quiz UI, or Mermaid runtime.

Done when `./learning-module/index.html`, `./learning-module/assets/mermaid.min.js`, and `./learning-module/assets/MERMAID-LICENSE.txt` all exist.

## Phase 6 — Quiz and iterate

After the developer has viewed the deck and completed the quiz, read their answers and write `quiz_result` into `onboarding/onboarding-session.json`.

If `quiz_result.passed == true`: print a congratulations message and stop.

If `quiz_result.passed == false`: read [`references/iterate-on-failure.md`](references/iterate-on-failure.md) and update the failing slides with `teaching_notes` only (do not rewrite `slide.content`). If a failed slide previously had no diagram and a diagram would clarify the concept, you may add a Mermaid diagram to `slide.content` — that is the one exception. Then regenerate the deck. Repeat up to 3 times.

## Output summary

| File | Written by |
|---|---|
| `onboarding/onboarding-session.json` | All phases (progressive) |
| `onboarding/user_data.json` | Phase 2 |
| `onboarding/index.html` | Deterministically built from session data in Phase 5; rebuilt by Phase 6 |
| `onboarding/assets/mermaid.min.js` | Copied from the pinned offline template by Phase 5 |
| `onboarding/assets/MERMAID-LICENSE.txt` | Mermaid license copied by Phase 5 |
| `onboarding/onboarding-session.json` | All phases (progressive) |
| `onboarding/user_data.json` | Phase 2 |
| `onboarding/slidev/slides.md` | Phase 5, updated by Phase 6 |
| `onboarding/slidev/package.json` | Phase 5 (once) |
| `onboarding/slidev/components/QuizQuestion.vue` | Phase 5 (once) |
| `onboarding/slidev/components/QuizResult.vue` | Phase 5 (once) |
| `onboarding/slidev/public/theme.css` | Phase 5 (once, never overwritten) |
