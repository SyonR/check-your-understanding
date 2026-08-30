# what-to-teach

Decides **which slides to include and in what order**. Run this before `how-to-format.md`.

## Step 1 — Anchor to the goal

Read `task_context.goal`. Every slide must be traceable to this goal. A slide that does not help the developer accomplish their goal is cut.

## Step 2 — Gap analysis

For each `tech_tag` in `repo_context.tech_tags`:

| Familiarity score | Action |
|---|---|
| `0` | **Teach from scratch** — include a foundational slide |
| `1` | **Orient** — one slide placing it in context of _this_ repo |
| `2` | **Connect** — one slide showing _how this repo uses it_ specifically |
| `3` | **Skip** foundational content; reference only where the repo diverges from convention |

## Step 3 — Sequence

Build the slide list in this order:

1. **Welcome** (`layout: cover`) — repo name, their goal, session overview
2. **Big picture** (`layout: section`) — architecture diagram or structure overview; always comes second
3. **Tech orientation slides** — ordered: unknown tags before known tags; fundamentals before specifics
4. **Repo-specific flows** — the runtime flows from `repo_context` most relevant to `task_context.goal`
5. **Where you'll be working** (`layout: two-cols`) — files and directories side-by-side with descriptions
6. **Key conventions** — only conventions that affect their work area

Do not generate a quiz-introduction slide. The Project Guide is the final non-quiz page and leads directly to the first question.

## Output of this step

An ordered list of slide stubs: `id`, `title`, `layout`, and a rough `content` outline. Pass this list to `how-to-format.md` to apply depth and style.
