
# slidev-builder

Takes `curriculum.slides` + `quiz.questions` and writes a self-contained Slidev presentation to `./slidev/`. Static layout files are copied from maintained skill assets; only `slides.md` is generated for the session.

## Install the reusable template

Run `scripts/install_slidev_template.py` from the directory containing the skill's `SKILL.md`, passing the session's `./slidev` directory:

```sh
python scripts/install_slidev_template.py ./slidev
```

If the current working directory is elsewhere, invoke the script by its full path. Do not read, synthesize, or rewrite the template files during generation. To change the layout for all future sessions, edit `assets/slidev-template/`. Rerun the installer to synchronize an existing session. The installer never touches `slides.md` or `package-lock.json`.

## Output directory structure

```
onboarding/slidev/
  slides.md          <- the complete presentation (curriculum + quiz slides)
  package.json       <- minimal Slidev dependency
  components/
    QuizQuestion.vue <- copied from the skill template
    QuizResult.vue   <- copied from the skill template
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

Then one `---`-delimited section per slide, setting `layout:` from `curriculum.slides[i].layout` and writing the slide's `content` as Markdown below it. Speaker notes go in `<!-- ... -->` directly after the content. If a slide has a `notes` field (written by the teaching-synthesis phase), put it in the `<!-- ... -->` block. If a slide also has a `teaching_notes` field (written by the iterate-on-failure phase), append it to the same block prefixed with `> Teaching note:`.

After all curriculum slides, append the check-your-understanding quiz section:

1. A `layout: section` slide titled `# Check Your Understanding`.
2. One slide per question that renders a `<QuizQuestion>` component (one question per slide prevents content overflow).
3. A final `<QuizResult>` slide that shows the score once all questions have been answered.

## Slide rendering rules

- One `---` separator between each slide. No blank lines between the separator and `layout:`.
- `two-cols` layout uses the Slidev `::right::` separator to split left and right columns.
- Code blocks use fenced triple-backtick with a language identifier (`ts`, `tsx`, `sh`, `json`, `yaml`).
- Mermaid diagrams use fenced triple-backtick with `mermaid`.
- Slidev uses a fixed 16:9 canvas and scales it to the viewport. Keep each slide focused on one main idea; split dense material across slides rather than depending on scrolling for normal reading.
- The shared theme provides vertical overflow scrolling as a safety net on every layout and horizontal scrolling for wide tables, code, and Mermaid diagrams. Do not override those overflow rules in generated slides.

## Static template files

`QuizQuestion.vue`, `QuizResult.vue`, `style.css`, and `package.json` are maintained under `assets/slidev-template/`. The installer copies them byte-for-byte. Bob must not recreate their implementation from prose.

On the generated quiz slide, include each question's `slide_ref` in the stored result passed to `QuizResult`, along with `id` and `correct`.
## QuizQuestion.vue

Write once to `./onboarding/slidev/components/QuizQuestion.vue`. It must:
- Display `prompt` as a heading
- Render each option as a `<button>`
- On click: disable all buttons; highlight correct answer green, chosen-wrong answer red
- Show `rationale` text after an answer is chosen
- Emit `answered` event with `{ id, correct: boolean }`

## QuizResult.vue

Write once to `./onboarding/slidev/components/QuizResult.vue`. It:
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

## public/theme.css

Write once to `./onboarding/slidev/public/theme.css`. Do not overwrite on regeneration if the file already exists.

```css
/* Custom theme overrides — edit freely */
```

## Post-generation instruction

After writing all files, print:
```
Slidev deck written to ./onboarding/slidev/
Run: cd onboarding/slidev && npm install && npm run dev
```
