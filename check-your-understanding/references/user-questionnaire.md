
# user-questionnaire

Conduct an adaptive terminal questionnaire and write the result to `user_data.json`. The questionnaire has three layers: **experience and learning support**, **tech familiarity** (derived from `tech_tags`), and **task context**. Ask all questions interactively, one group at a time.

## Prerequisite

`repo_context.tech_tags` must be populated before running this phase. Use it to generate the tech-familiarity questions.

## Experience and learning support — Layer 1 (always ask)

Present as numbered multiple-choice or short-answer prompts. Use `ask_followup_question` for each.

| Question | Type | Stores in |
|---|---|---|
| How many years of software experience do you have? | single choice: 0–1 / 1–3 / 3–7 / 7+ | `identity.years_experience` (midpoint) |
| What is your current role? | single choice: junior / mid / senior / lead / other | `identity.role` |
| How do you prefer to learn? | single choice: top-down (big picture first) / bottom-up (details first) / example-first / concept-first | `preferred_style` |
| How much prerequisite support would help? | single choice: standard / foundations (recommended for students, interns, and career switchers) | `learning_mode` |
| How interactive should the lesson be? | single choice: light (2–3 activities) / guided (4–6 activities) | `interaction_level` |

Explain that **Foundations mode** defines prerequisite CS concepts on first use and does not assume framework, command-line, HTTP, database, or asynchronous-programming knowledge unless their familiarity answers show otherwise. Do not infer the choice solely from job title; always let the learner choose.

## Tech familiarity — Layer 2 (adaptive: one question per tech_tag)

For each tag in `repo_context.tech_tags`, ask a familiarity question. Skip tags where the answer is obvious from the prior-experience answers (e.g. a senior developer with 7+ years asked about `javascript`).

Template:
> How familiar are you with **{tag}**?
> A) Never used it (0)  B) I've seen it but not built with it (1)  C) I've used it on a project (2)  D) I'm comfortable teaching it (3)

Store result as `user_data.tech_familiarity[tag] = 0|1|2|3`.

**Batching rule:** Group related tags into one question when they are tightly coupled (e.g. `react` + `typescript`, `postgres` + `prisma`). Ask no more than 6 familiarity questions total; prioritise tags that appear in the hotspots region of `repo_context.summary`.

## Task context — Layer 3 (always ask)

| Question | Type | Stores in |
|---|---|---|
| Do you have a specific ticket or task you are working on? | yes/no | `task_context.has_ticket` |
| If yes: what is the ticket reference? (Jira, Linear, GitHub issue, Slack link) | short text | `task_context.ticket_ref` |
| If yes: paste a one-sentence summary of what the ticket asks you to do. | short text | `task_context.ticket_summary` |
| In one sentence: what do you need to be able to do after this session? | short text | `task_context.goal` |

If `has_ticket` is false, skip `ticket_ref` and `ticket_summary` but always collect `goal`.

## Output

Write `onboarding/user_data.json`. Also write the `user_data` block into `onboarding/onboarding-session.json`:

```json
{
  "user_data": {
    "collected_at": "<ISO-8601>",
    "identity": { "years_experience": 3, "role": "mid" },
    "tech_familiarity": { "react": 2, "postgres": 1, "docker": 0 },
    "task_context": {
      "has_ticket": true,
      "ticket_ref": "PROJ-123",
      "ticket_summary": "Add rate limiting to the /api/upload endpoint.",
      "goal": "Understand where the request pipeline lives so I can add middleware."
    },
    "preferred_style": "top-down",
    "learning_mode": "foundations",
    "interaction_level": "guided"
  }
}
```

## Tone rules

- Use plain English. No jargon in the questions themselves.
- Keep the session under 3 minutes. If a question can be answered by a prior answer, skip it.
- Never ask a question whose answer won't change the curriculum or quiz.
