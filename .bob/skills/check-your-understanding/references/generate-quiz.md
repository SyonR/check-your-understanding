# generate-quiz

Takes `repo_context` + `curriculum.slides` and produces the single `quiz` block. There is exactly one quiz per session; it lives at the end of the interactive learning module.

## Core test principle

**Test whether the developer can navigate and change the system — not whether they memorised names.**

A passing developer should be able to answer: "Where would I add X?", "What happens when Y?", "Which file controls Z?". A failing developer knows facts but cannot act on them.

## Question types

| Type | When to use |
|---|---|
| `multiple-choice` | Baseline comprehension; always include at least two |
| `scenario` | "You need to add a feature that does X. Where do you start?" |
| `where-would-you-change` | "If the rate limit needs to change, which file do you edit?" |
| `ordering` | "Put these events in the order they happen during a request" |
| `flow-completion` | "Fill in the missing step: Request → Auth → __ → Response" |
| `dependency-reasoning` | "If you change module A, what else might break and why?" |

## Generation rules

1. **One question per slide** that has a concrete, testable claim. Skip the `cover` and `quiz-intro` slides.
2. **Minimum 5 questions, maximum 12.** If slides produce more, keep the questions tied to the developer's `task_context.goal` and cut the rest.
3. **Each question must have a `slide_ref`** pointing to the slide whose content it tests. This is used by the iterate-on-failure phase.
4. **Options must be equal length.** For `multiple-choice`, all four options should be approximately the same word count (±3 words). Never give the answer away through formatting.
5. **Rationale is required.** Every question needs a `rationale` explaining the correct answer. This is shown after the quiz, not during.
6. **No trivia.** Do not ask what a function is named, what a class is called, or what a file path is unless knowing it is directly required to accomplish `task_context.goal`.
7. **No leading questions.** The prompt must not hint at the answer.

## Difficulty calibration

Use `user_data.identity.role` and `tech_familiarity` scores:
- `senior`/`lead` → focus on architecture trade-offs and cross-module dependencies.
- `junior`/`mid` → focus on flow-completion and where-would-you-change types.
- Never ask a question about a technology where `tech_familiarity[tag] == 0` and it was skipped in the curriculum.

## Pass threshold

Default `pass_threshold: 0.8`. Adjust to `0.7` for `junior` role.

## Output

Populate `quiz` in `onboarding-session.json`:

```json
{
  "quiz": {
    "generated_at": "<ISO-8601>",
    "pass_threshold": 0.8,
    "questions": [
      {
        "id": "q1",
        "type": "where-would-you-change",
        "prompt": "The upload rate limit needs to increase from 10 to 50 requests per minute. Which file do you edit?",
        "options": [
          "src/middleware/rateLimit.ts",
          "src/routes/upload.ts",
          "src/config/app.ts",
          "src/services/storage.ts"
        ],
        "answer": "src/middleware/rateLimit.ts",
        "rationale": "Rate limit configuration lives in the middleware layer. The route file calls the middleware but does not define the limit value.",
        "slide_ref": "request-pipeline"
      }
    ]
  }
}
```
