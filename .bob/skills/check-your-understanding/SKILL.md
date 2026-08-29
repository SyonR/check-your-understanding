---
name: check-your-understanding
description: >
  Onboard a developer onto a codebase: analyse the repo, interview the developer,
  synthesise a personalised curriculum, generate a Slidev deck with a single
  check-your-understanding quiz at the end, and iterate the deck on failure.
  Triggers on: "onboard me", "check my understanding", "walk me through this repo",
  "generate onboarding slides".
argument-hint: "Path to the repo to onboard onto (defaults to current directory)"
---

Onboard one developer onto one codebase in a single session. State is stored in `onboarding-session.json` in the session output directory; every phase reads from and writes to that file so the pipeline is resumable.

## Phase 0 — Locate or create the session file

Look for `onboarding-session.json` in the current directory.

- If absent: create it as `{}` and run all phases from Phase 1.
- If present: read it and check which phases have already produced output (non-null fields). Skip completed phases; resume from the first incomplete one.

## Phase 1 — Understand the repo

**Run in background** (this phase can be started immediately and run concurrently with Phase 2 if `repo_context` is absent).

Read [`references/understand-repo.md`](references/understand-repo.md) and follow it to produce `repo_context`. Done when all 13 coverage flags are `true`.

If `repo_context` already exists, check the coverage flags. If any are `false`, re-run only the investigation steps needed to fill the gaps, then update the existing `repo_context` block.

## Phase 2 — Questionnaire

**Requires:** `repo_context.tech_tags` (wait for Phase 1 to produce them before starting Layer 2).

Read [`references/user-questionnaire.md`](references/user-questionnaire.md) and conduct the three-layer questionnaire interactively. Write answers to `user_data.json` and into `onboarding-session.json`.

Done when `user_data` is present and `task_context.goal` is non-empty.

## Phase 3 — Teaching synthesis

**Requires:** `repo_context` (all coverage flags `true`) + `user_data`.

Read [`references/teaching-synthesis.md`](references/teaching-synthesis.md) and produce `curriculum.slides`. Write into `onboarding-session.json`.

Done when `curriculum.slides` contains between 5 and 20 slides, ending with a `quiz-intro` slide.

## Phase 4 — Generate quiz

**Requires:** `curriculum.slides`.

Read [`references/generate-quiz.md`](references/generate-quiz.md) and produce `quiz`. Write into `onboarding-session.json`.

Done when `quiz.questions` has between 5 and 12 items, every question has a `slide_ref`, and `pass_threshold` is set.

> Phases 3 and 4 may run in parallel once Phase 2 is complete.

## Phase 5 — Build Slidev deck

**Requires:** `curriculum.slides` + `quiz.questions`.

Read [`references/slidev-builder.md`](references/slidev-builder.md) and write the complete Slidev presentation to `./slidev/`.

Done when `./slidev/slides.md`, `./slidev/package.json`, `./slidev/components/QuizQuestion.vue`, and `./slidev/components/QuizResult.vue` all exist.

## Phase 6 — Quiz and iterate

After the developer has viewed the deck and completed the quiz, read their answers and write `quiz_result` into `onboarding-session.json`.

If `quiz_result.passed == true`: print a congratulations message and stop.

If `quiz_result.passed == false`: read [`references/iterate-on-failure.md`](references/iterate-on-failure.md) and update the failing slides with `teaching_notes`, then regenerate the deck. Repeat up to 3 times.

## Output summary

| File | Written by |
|---|---|
| `onboarding-session.json` | All phases (progressive) |
| `user_data.json` | Phase 2 |
| `slidev/slides.md` | Phase 5, updated by Phase 6 |
| `slidev/package.json` | Phase 5 (once) |
| `slidev/components/QuizQuestion.vue` | Phase 5 (once) |
| `slidev/components/QuizResult.vue` | Phase 5 (once) |