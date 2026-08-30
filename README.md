# check-your-understanding

An IBM Bob skill that onboards a developer onto any codebase in a single session, no manual walkthroughs, no stale wikis.

---

## What this skill does

A developer opens a new repo and types *"onboard me"*. Bob runs a 6-phase pipeline:

1. **Analyses the repo** — reads structure, entry points, conventions, and captures evidence-backed facts
2. **Interviews the developer** — 3-layer questionnaire: identity, tech familiarity, and their specific task
3. **Synthesises a curriculum** — personalised slide plan based on role, knowledge gaps, and goal
4. **Generates a quiz** — 5–12 questions that test navigation ability, not memorisation
5. **Builds an offline learning module** — opens as a single `index.html`, no npm or server needed
6. **Iterates on failure** — adds targeted teaching notes to any slide the developer answered wrong; repeats up to 3 times

All output is written to `onboarding/` in the target repo.

---

## Skill installation

Add this to your project's `skills-lock.json`:

```json
"check-your-understanding": {
  "source": "SyonR/check-your-understanding",
  "sourceType": "github",
  "skillPath": "check-your-understanding/SKILL.md",
  "computedHash": ""
}
```

Then trigger it in Bob:

```
onboard me
```

or

```
check my understanding of this repo
```

---

## Repository structure

```
check-your-understanding/
  SKILL.md                        ← pipeline orchestrator (6 phases)
  references/
    understand-repo.md            ← Phase 1: repo analysis + guide_facts capture
    user-questionnaire.md         ← Phase 2: adaptive 3-layer interview
    teaching-synthesis.md         ← Phase 3: orchestrates what-to-teach + how-to-format
    what-to-teach.md              ← which slides, in what order
    how-to-format.md              ← depth by role, style, analogies, Key Concepts tab
    generate-quiz.md              ← Phase 4: quiz generation rules
    html-builder.md               ← Phase 5: deterministic offline HTML builder
    iterate-on-failure.md         ← Phase 6: teaching notes + module rebuild
  schema/
    onboarding.schema.json        ← shared data contract for all phases
  scripts/
    build_static_module.py        ← validates session data and builds index.html
```



