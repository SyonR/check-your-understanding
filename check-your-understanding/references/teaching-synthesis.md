# teaching-synthesis

Takes `repo_context` + `user_data` and produces `curriculum.slides`. This phase is split into two steps; read both reference files and apply them in order:

1. **[`what-to-teach.md`](what-to-teach.md)** — Decides _which_ slides to include and in what order, based on the goal and the developer's knowledge gaps.
2. **[`how-to-format.md`](how-to-format.md)** — Decides _how_ to write each slide: depth per role, preferred learning style, analogies, and slide count limits.

## Inputs

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
    ]
  }
}
```

Each slide's `content` is valid Slidev Markdown (GitHub-flavoured + Mermaid). The `layout` field must be one of: `cover`, `default`, `center`, `two-cols`, `section`, `image-right`, `iframe-right`. The `notes` field holds speaker notes and analogies; it is never shown on the slide. `teaching_notes` is written later by the iterate-on-failure phase only.