
# iterate-on-failure

Runs only when `quiz_result.passed == false`. Takes the set of failed questions, updates `curriculum.slides` with targeted `teaching_notes`, and rebuilds the offline learning module.

## Inputs

- `quiz_result.failed_question_ids` — the questions the developer got wrong
- `quiz.questions` — the full question set (to find `slide_ref` for each failed question)
- `curriculum.slides` — the existing slide set
- `repo_context` — the source of truth for corrections

## Algorithm

### Step 1 — Map failures to slides

For each `id` in `failed_question_ids`:
1. Find the question in `quiz.questions`.
2. Get its `slide_ref`.
3. Find the slide in `curriculum.slides` where `slide.id == slide_ref`.

### Step 2 — Write teaching notes

For each failed slide, write a `teaching_notes` string into `curriculum.slides[i].teaching_notes`:

- State what the correct answer is and why, in plain language.
- Reference the exact file or line in the repo that is the source of truth.
- **Do not rewrite `slide.content`.** The one exception: if the slide has no diagram and adding a Mermaid diagram would directly clarify the failed concept, you may add it to `slide.content`.
- Preserve all other slides unchanged.
- If multiple failed questions map to the same slide, consolidate into one `teaching_notes` string.

### Step 3 — Rebuild module

After updating `curriculum.slides`, re-run the HTML builder phase to regenerate `./onboarding/learning-module/index.html`.

Do not regenerate the quiz. The quiz stays unchanged so the developer retakes the same questions.

## Output

Updated `onboarding/onboarding-session.json` with `teaching_notes` populated on affected slides. Updated `./onboarding/learning-module/index.html`.

Print:
```
{n} lesson(s) updated with teaching notes.
Learning module rebuilt. Open: onboarding/learning-module/index.html
```

## Iteration limit

Do not iterate more than 3 times on the same session. After 3 failures, append a final `layout: section` lesson:

```
# Recommended next step

These concepts may need hands-on practice:
{list of slide titles for all failed slide_refs across all iterations}

Consider pairing with a team member or reviewing the linked source files directly.
```
