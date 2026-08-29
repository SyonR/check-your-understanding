# teaching-synthesis

Takes `repo_context` + `user_data` and produces `curriculum.slides`. This phase is split into two steps; read both reference files and apply them in order:

1. **[`what-to-teach.md`](what-to-teach.md)** — Decides _which_ slides to include and in what order, based on the goal and the developer's knowledge gaps.
2. **[`how-to-format.md`](how-to-format.md)** — Decides _how_ to write each slide: depth per role, preferred learning style, analogies, and slide count limits.

## Inputs

- `repo_context.guide_facts` — source-backed commands, paths, patterns, and warnings for the compact project guide
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

Do not generate a quiz-introduction or "Check Your Understanding" transition slide. The compact Project Guide is the final non-quiz page and leads directly to the first question.

### Step 3a — Compact project guide

Also produce `curriculum.guide`, a quick-reference subpage shown after the teaching slides and immediately before the first quiz question. Use exactly these short tabs: `Setup`, `First Tasks`, `Architecture`, `Patterns`, `Test & Debug`, and `Reference`.

- Populate each tab only from its matching `repo_context.guide_facts` category: `setup`, `first_tasks`, `architecture`, `patterns`, `test_debug`, or `reference`.
- Preserve commands, URLs, environment-variable names, and file paths exactly as recorded. When facts conflict, use the fact backed by executable code or configuration rather than prose documentation.
- Every visible statement must be traceable to at least one fact's `evidence`. Evidence paths do not need to be displayed unless they are useful reference links.
- If a required category is absent or empty, return to Phase 1 and collect only that category. Do not infer missing repository facts from general framework knowledge.
- Keep each tab at 80 words or fewer and no more than four bullets.
- Prefer commands, file paths, expected results, and project-specific warnings over general explanations.
- Summarise existing research; do not add another teaching sequence or duplicate full slides.
- Use lowercase kebab-case tab IDs.
- If slides already exist and only the guide is missing, create the guide without rewriting the slides.

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

- Minimum 5 teaching slides, including the cover.
- Maximum 20 slides. If the gap analysis produces more, merge related tech slides and cut any slide not directly on the path to `task_context.goal`.

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
        {
          "id": "setup",
          "label": "Setup",
          "content": "**Start:** `{repo command}`\n\n- **Verify:** {expected result}\n- **Tests:** `{test command}`"
        },
        {
          "id": "first-tasks",
          "label": "First Tasks",
          "content": "- {small task and first file}\n- {next task and verification}"
        },
        {
          "id": "architecture",
          "label": "Architecture",
          "content": "- {component flow}\n- {data or service boundary}"
        },
        {
          "id": "patterns",
          "label": "Patterns",
          "content": "- {convention and canonical file}\n- {important anti-pattern}"
        },
        {
          "id": "test-debug",
          "label": "Test & Debug",
          "content": "- **Test:** `{command}`\n- **First debug stop:** {log or tool}"
        },
        {
          "id": "reference",
          "label": "Reference",
          "content": "- `{path}` — {purpose}\n- {project-specific warning or help location}"
        }
      ]
    }
  }
}
```

Each lesson's `content` uses the Markdown subset documented in [`html-builder.md`](html-builder.md), including Mermaid fenced blocks. The `layout` field must be one of: `cover`, `default`, `center`, `two-cols`, `section`.
