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

## Step 5 — Simplification and analogy

For any concept where `tech_familiarity[tag] <= 1`, add one analogy line to the slide's `notes` field. The `notes` field is never shown on the slide itself — it goes into Slidev speaker notes. The analogy should be something a non-programmer would recognise.

Do not put analogies or speaker content into `content`. Do not write `teaching_notes` here — that field is reserved for the iterate-on-failure phase.

## Step 6 — Slide count guard

- Minimum 5 slides (including cover and quiz intro).
- Maximum 20 slides. If the gap analysis produced more stubs, merge related tech slides and cut any slide not directly on the path to `task_context.goal`.

## Step 7 — Key Concepts tab (conditional)

After the 6 guide tabs are generated, check both conditions:

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
