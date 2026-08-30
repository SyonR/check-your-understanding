# how-to-format

Takes the ordered slide stubs from `what-to-teach.md` and applies **depth calibration, preferred style, analogies, and slide count limits**. Run this after `what-to-teach.md`.

## Step 4 — Depth calibration

Apply to every slide based on `user_data.identity.role`:

| Role | Depth |
|---|---|
| `junior` | Define every term. Use analogies. One concept per slide. |
| `mid` | Skip definitions for `tech_familiarity >= 2`. Show examples. |
| `senior` / `lead` | Skip all foundational slides. Go straight to repo-specifics and architecture decisions. |

Then apply `user_data.preferred_style`:

| Style | Rule |
|---|---|
| `top-down` | Put big-picture slides first, details last |
| `bottom-up` | Start with a concrete file, build up to architecture |
| `example-first` | Lead each slide with a code snippet, then explain |
| `concept-first` | Lead each slide with the concept definition, then the example |

### Foundations mode

When `user_data.learning_mode == 'foundations'`, override role-based assumptions where necessary:

- Assume no prior knowledge of the command line, HTTP, APIs, databases, asynchronous execution, dependency injection, ORMs, or the project's frameworks unless the learner rated the relevant technology `2` or `3`.
- Introduce each prerequisite only when it becomes necessary: **plain meaning → concrete repository example → why it matters for the learner's goal**.
- Use one main idea per page, short sentences, and a small worked example. Define symbols and abbreviations on first use.
- State the input, output, and responsibility when describing a function, layer, request, or data flow.
- Call out one likely misconception when it could cause a real implementation mistake.
- Do not turn the curriculum into a generic CS survey; omit fundamentals that are not needed for the learner's goal.

## Step 5 — Simplification and analogy

For any concept where `tech_familiarity[tag] <= 1`, add one analogy line to the slide's `notes` field. The `notes` field is never shown on the slide itself — it goes into Slidev speaker notes. The analogy should be something a non-programmer would recognise.

Do not put analogies or speaker content into `content`. Do not write `teaching_notes` here — that field is reserved for the iterate-on-failure phase.

## Step 6 — Slide count guard

- Minimum 5 teaching slides, including the cover.
- Maximum 20 slides. If the gap analysis produced more stubs, merge related tech slides and cut any slide not directly on the path to `task_context.goal`.

## Step 7 — Key Concepts tab (conditional)

After the 6 guide tabs are generated, check both conditions:

- `user_data.learning_mode == 'foundations'`, **or**
- `user_data.identity.role == 'junior'`, **or**
- any `tech_familiarity` score for a tag used in the Architecture or Patterns tab content is `0`

If either condition is true, generate a 7th tab:

```json
{
  "id": "key-concepts",
  "label": "Key Concepts",
  "content": "..."
}
```

**Rules for this tab:**

- Identify every technical term in the Architecture and Patterns tabs that corresponds to a `tech_familiarity == 0` tag (e.g. MCP, GraphQL, gRPC, event loop). Also include terms used in those tabs that have no direct `tech_tag` but are jargon a non-developer would not know (e.g. "middleware", "service layer", "ORM").
- Write one plain-language definition per term, 1–2 sentences. Lead with an analogy when the concept is abstract.
- Maximum 5 terms. If more qualify, prioritise the ones most relevant to `task_context.goal`.
- Do not duplicate anything already explained in the curriculum slides.
- If neither condition is true, do not generate this tab. The guide stays at 6 tabs.

## Step 8 — Embedded learning interactions

Add an optional `interaction` to selected teaching slides. Never add one to the cover, Project Guide, or final quiz. Keep the activity directly tied to that page's single learning objective.

| `interaction_level` | Required activities |
|---|---|
| `light` | 2–3 interactions across the module |
| `guided` | 4–6 interactions across the module |

Use both interaction types at least once:

```json
{
  "type": "reveal",
  "prompt": "Pause and predict what happens next.",
  "answer": "A short explanation revealed on demand."
}
```

```json
{
  "type": "checkpoint",
  "prompt": "Which file should own this change?",
  "options": ["Option A", "Option B", "Option C"],
  "answer": "Option B",
  "rationale": "A short explanation connected to the repository."
}
```

- `reveal` is for prediction, tracing, terminology, or explaining why a step occurs.
- `checkpoint` is an ungraded practice question with 2–4 plausible options and immediate feedback.
- Do not copy final-quiz questions. Embedded checkpoints prepare the learner; the final quiz measures independent recall.
- Keep prompts under 30 words and answers or rationales under 60 words.
- In Foundations mode, prefer interactions that expose misconceptions or ask the learner to trace one concrete input through the repository.
