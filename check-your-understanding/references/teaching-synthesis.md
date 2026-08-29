# teaching-synthesis

Takes `repo_context` + `user_data` and produces `curriculum.slides` — the ordered list of slide specs that form the Slidev deck. This is the only phase that decides _what_ to teach, _in what order_, and _at what depth_.

## Inputs

- `repo_context.summary` — what the codebase is
- `repo_context.tech_tags` — what technologies are in play
- `user_data.tech_familiarity` — what the developer already knows
- `user_data.task_context.goal` — what they need to accomplish
- `user_data.preferred_style` — how they prefer to be taught
- `user_data.identity.role` — their seniority level

## Synthesis algorithm

### Step 1 — Anchor to the goal

Read `task_context.goal`. Every slide must be traceable to this goal. A slide that does not help the developer accomplish their goal is cut.

### Step 2 — Gap analysis

For each `tech_tag` in `repo_context.tech_tags`:
- `tech_familiarity[tag] == 0` → **teach from scratch** (include a foundational slide)
- `tech_familiarity[tag] == 1` → **orient** (one slide that places it in context of _this_ repo)
- `tech_familiarity[tag] == 2` → **connect** (one slide showing _how this repo uses it_ specifically)
- `tech_familiarity[tag] == 3` → **skip** foundational content; reference only where the repo diverges from convention

### Step 3 — Sequence

Build the slide list in this order:

1. **Welcome** (`layout: cover`) — repo name, their goal, session overview
2. **Big picture** (`layout: section`) — architecture diagram or structure overview; always comes second
3. **Tech orientation slides** — ordered: unknown tags before known tags; fundamentals before specifics
4. **Repo-specific flows** — the runtime flows from `repo_context` most relevant to `task_context.goal`
5. **Where you'll be working** (`layout: two-cols`) — files and directories side-by-side with descriptions
6. **Key conventions** — only conventions that affect their work area
7. **Quiz intro** (`layout: section`) — transitions to the check-your-understanding

### Step 4 — Depth calibration

| Role | Depth |
|---|---|
| junior | Define every term. Use analogies. One concept per slide. |
| mid | Skip definitions for `tech_familiarity >= 2`. Show examples. |
| senior / lead | Skip all foundational slides. Go straight to repo-specifics and architecture decisions. |

`preferred_style` further adjusts:
- `top-down` → put the big-picture slides first, details last
- `bottom-up` → start with a concrete file, build up to architecture
- `example-first` → lead each slide with a code snippet, then explain
- `concept-first` → lead each slide with the concept definition, then the example

### Step 5 — Simplification and analogy

For any concept where `tech_familiarity[tag] <= 1`, add one analogy line to the slide's `notes` field (not visible in the slide itself). The analogy should be something a non-programmer would recognise.

### Step 6 — Slide count guard

- Minimum 5 slides (including cover and quiz intro).
- Maximum 20 slides. If the gap analysis produces more, merge related tech slides and cut any slide not directly on the path to `task_context.goal`.

## Output

Populate `curriculum` in `onboarding-session.json`:

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

Each slide's `content` is valid Slidev Markdown (GitHub-flavoured + Mermaid). The `layout` field must be one of: `cover`, `default`, `center`, `two-cols`, `section`, `image-right`, `iframe-right`.