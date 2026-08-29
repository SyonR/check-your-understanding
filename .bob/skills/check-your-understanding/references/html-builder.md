# offline HTML builder

Builds a responsive, interactive learning module from `repo_context.guide_facts`, `curriculum.slides`, `curriculum.guide`, and `quiz.questions`. The learner opens the result directly from their filesystem; npm, Node, a web server, and internet access are not required.

## Build

Run the builder located under the directory containing this skill's `SKILL.md`:

```sh
python scripts/build_static_module.py ./onboarding-session.json ./learning-module
```

When the current working directory is elsewhere, invoke the script by its full path. Do not read or recreate the HTML shell in model output. The script validates the required session data—including all six evidence-backed guide-fact categories and the six compact rendered tabs—injects it into the maintained template, and copies the pinned Mermaid runtime and license.

## Output

```text
learning-module/
  index.html
  assets/
    mermaid.min.js
    MERMAID-LICENSE.txt
```

`index.html` contains all lesson rendering, navigation, responsive styling, quiz behavior, scoring, review links, and the compact project-guide subpage from `curriculum.guide`. Its maintained shell uses the same restrained purple and neutral palette for every session, a full-viewport content area, and a collapsible numbered sidebar. The sidebar has no title/header, its scroll indicator stays hidden, and the lesson area has no top header or progress bar. Mermaid 11.17.2 is loaded from the adjacent local asset and renders `mermaid` fenced blocks offline with `securityLevel: strict`.

The learner opens `learning-module/index.html` in a modern browser. Keep the entire directory together when sharing it.

## Content compatibility

The maintained renderer supports the generated curriculum's headings, paragraphs, emphasis, inline code, fenced code, Mermaid blocks, blockquotes, ordered and unordered lists, tables, and `::left::` / `::right::` columns. Keep generated slide content within that subset. Raw HTML is displayed as text rather than executed.

The module renders one quiz question per view to avoid clipping on small screens. The lesson area is always vertically scrollable, including cover and section layouts. Two-column content collapses to one column on narrow screens. CSS viewport queries plus browser resize and `visualViewport` listeners adapt the shell when screen dimensions or zoom level change.

## Completion

Confirm that all three output files exist, then print:

```text
Offline learning module written to ./learning-module/index.html
Open index.html directly in a modern browser; no package manager or server is required.
```
