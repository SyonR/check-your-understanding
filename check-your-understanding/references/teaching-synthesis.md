# teaching-synthesis

Takes `repo_context` + `user_data` and produces `curriculum.slides` + `curriculum.guide`. Apply the two sub-files in order:

1. **[`what-to-teach.md`](what-to-teach.md)** — which slides to include and in what order (goal anchoring, gap analysis, sequencing, project guide tabs).
2. **[`how-to-format.md`](how-to-format.md)** — how to write each slide (depth by role, preferred style, analogies, slide count guard, conditional Key Concepts tab).

## Inputs

- `repo_context.guide_facts` — source-backed facts for the compact project guide
- `repo_context.summary` — what the codebase is
- `repo_context.tech_tags` — what technologies are in play
- `user_data.tech_familiarity` — what the developer already knows
- `user_data.task_context.goal` — what they need to accomplish
- `user_data.preferred_style` — how they prefer to be taught
- `user_data.identity.role` — their seniority level

## Output

Populate `curriculum` in `onboarding/onboarding-session.json`:

```json
{
  "curriculum": {
    "generated_at": "<ISO-8601>",
    "slides": [
      {
        "id": "cover",
        "title": "Welcome to {repo name}",
        "layout": "cover",
        "content": "## Your goal\n{task_context.goal}\n\n## Today's session\n{slide count} slides + quiz",
        "notes": ""
      },
      {
        "id": "architecture",
        "title": "How {repo name} is structured",
        "layout": "default",
        "content": "...",
        "notes": "Analogy: ..."
      }
    ],
    "guide": {
      "title": "Project Guide",
      "intro": "A compact reference for working in this repository.",
      "tabs": [
        { "id": "setup",       "label": "Setup",        "content": "..." },
        { "id": "first-tasks", "label": "First Tasks",  "content": "..." },
        { "id": "architecture","label": "Architecture", "content": "..." },
        { "id": "patterns",    "label": "Patterns",     "content": "..." },
        { "id": "test-debug",  "label": "Test & Debug", "content": "..." },
        { "id": "reference",   "label": "Reference",    "content": "..." }
      ]
    }
  }
}
```

A 7th `key-concepts` tab is appended by `how-to-format.md` when `identity.role == 'junior'` or any relevant `tech_familiarity == 0`. See [`how-to-format.md`](how-to-format.md) Step 7 for the rules.

Each slide's `content` uses the Markdown subset documented in [`html-builder.md`](html-builder.md), including Mermaid fenced blocks. The `layout` field must be one of: `cover`, `default`, `center`, `two-cols`, `section`. Do not generate a quiz-introduction slide; the Project Guide leads directly to the first quiz question.
