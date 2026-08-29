
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
slidev/
  slides.md          <- the complete presentation (curriculum + quiz slide)
  package.json       <- copied from the skill template
  style.css          <- copied global responsive and overflow styles
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

Then one `---`-delimited section per slide, setting `layout:` from `curriculum.slides[i].layout` and writing the slide's `content` as Markdown below it. Speaker notes go in `<!-- ... -->` directly after the content. If `teaching_notes` is present, append it to the notes block prefixed with `> Teaching note:`.

After all curriculum slides, append the interactive quiz directly. Do not add a separate `# Check Your Understanding` transition slide. Render `<QuizQuestion>` for each question and `<QuizResult>` at the end.

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

## Post-generation instruction

After writing all files, print:
```
Slidev deck written to ./slidev/
Run: cd slidev && npm install && npm run dev
```
