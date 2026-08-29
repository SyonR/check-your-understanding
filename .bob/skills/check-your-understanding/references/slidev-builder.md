
# slidev-builder

Takes `curriculum.slides` + `quiz.questions` and writes a self-contained Slidev presentation to `./slidev/`. The directory is the deliverable; the developer opens it with `npx slidev`.

## Output directory structure

```
slidev/
  slides.md          <- the complete presentation (curriculum + quiz slide)
  package.json       <- minimal Slidev dependency
  components/
    QuizQuestion.vue <- reusable multiple-choice quiz component
    QuizResult.vue   <- pass/fail result display
  public/
    theme.css        <- custom CSS overrides (generated once, not overwritten on regeneration)
```

## slides.md format

Slidev uses YAML frontmatter at the top of `slides.md`, then `---` to separate slides.

The top-level frontmatter block:
```yaml
---
theme: default
title: "{repo name} — Developer Onboarding"
highlighter: shiki
---
```

Then one `---`-delimited section per slide, setting `layout:` from `curriculum.slides[i].layout` and writing the slide's `content` as Markdown below it. Speaker notes go in `<!-- ... -->` directly after the content. If `teaching_notes` is present, append it to the notes block prefixed with `> Teaching note:`.

After all curriculum slides, append two more sections:

1. A `layout: section` slide titled `# Check Your Understanding`.
2. A single slide that renders `<QuizQuestion>` for each question and `<QuizResult>` at the end.

## Slide rendering rules

- One `---` separator between each slide. No blank lines between the separator and `layout:`.
- `two-cols` layout uses the Slidev `::right::` separator to split left and right columns.
- Code blocks use fenced triple-backtick with a language identifier (`ts`, `tsx`, `sh`, `json`, `yaml`).
- Mermaid diagrams use fenced triple-backtick with `mermaid`.

## QuizQuestion.vue

Write once to `./slidev/components/QuizQuestion.vue`. It must:
- Display `prompt` as a heading
- Render each option as a `<button>`
- On click: disable all buttons; highlight correct answer green, chosen-wrong answer red
- Show `rationale` text after an answer is chosen
- Emit `answered` event with `{ id, correct: boolean }`
- Include global CSS that makes any slide containing a quiz question vertically scrollable:

  ```vue
  <style scoped>
  .quiz-btn:disabled {
    pointer-events: none;
  }

  :global(.slidev-layout:has(.quiz-question)) {
    overflow-y: auto;
  }
  </style>

## QuizResult.vue

Write once to `./slidev/components/QuizResult.vue`. It:
- Receives an array of `{ id, correct }` results
- When `results.length == questions.length`: displays score and pass/fail state
- On fail: lists the `slide_ref` for each failed question as "Review: {slide title}"

## package.json

```json
{
  "name": "onboarding-slides",
  "private": true,
  "scripts": {
    "dev": "slidev slides.md --open",
    "build": "slidev build slides.md"
  },
  "dependencies": {
    "@slidev/cli": "^0.49.0",
    "@slidev/theme-default": "latest"
  }
}
```

## Post-generation instruction

After writing all files, print:
```
Slidev deck written to ./slidev/
Run: cd slidev && npm install && npm run dev
```
