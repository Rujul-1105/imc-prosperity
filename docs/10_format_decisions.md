# Format Decisions

Why HTML for `resources/`, why .md for `docs/`, and the trade-offs we accepted.

## The choice

| Folder | Format | Why |
|---|---|---|
| `resources/` | `.html` | Browser-renderable, MathJax + Prism, lighter than PDF. |
| `docs/` | `.md` | Machine-grep-friendly, lighter than HTML, easier to edit in text editors. |

## Why HTML for `resources/`

Considered:

- **Markdown** — cleanest to write, but no MathJax without a converter, no syntax highlighting without one, and the conversion tooling adds friction.
- **PDF** — looks nice, but editing is painful (no copy-paste of code, no live links, no MathJax).
- **HTML** — slightly more verbose to write, but:
  - MathJax renders equations live.
  - Prism.js renders code with syntax highlighting.
  - Copy-paste works in the browser.
  - Easy to edit (plain text).
  - Browser-rendered = portable.
- **Jupyter notebook** — interactive, but the team doesn't want a notebook-driven curriculum. Too easy to get lost in execution.

HTML won on portability + editability + live rendering.

## Why Markdown for `docs/`

Considered:

- **HTML** — consistent with `resources/`, but docs/ is for AI agents + future-self, not browser reading.
- **Markdown** — easier to grep, easier to diff in git, easier to embed in prompts.
- **Plain text** — too unstructured for a "regeneration context" folder.

Markdown won on machine-readability.

## CDN dependencies

We chose MathJax and Prism from jsdelivr. They are the de-facto standards. We accept:

- An internet connection to view `resources/` (the team has internet).
- A 5-10ms load on first open. Negligible.

Alternatives considered:

- Self-hosted libraries: rejected. Bloats file size, requires bundling.
- No libraries (write everything from scratch): rejected. MathJax is non-trivial to replace.

## File size

- Each module HTML: ~30-100 KB. Negligible.
- Total `resources/` size: ~2 MB for all 20 modules. Tiny.
- Total `docs/` size: ~200 KB. Tiny.

## Trade-offs we accept

- **No offline support** for `resources/`. Acceptable; the team has internet.
- **No print-friendliness**. We don't need to print; if needed, the team uses the browser's print-to-PDF.
- **CDN dependency for math + code rendering**. Acceptable; jsdelivr is reliable.
- **No fancy interactivity** (no embedded Plotly, no calculators). Adds complexity. We can add if needed.

## Versioning

`resources/` is committed to git like any other code. Edits show up in `git log`. No binary files. No PDFs. Diff-able.

`docs/` is the same. The team (or a future agent) reads git log to see what changed.

## When to change format

If the team finds HTML awkward to edit, switch to `.md` with a static-site generator. Until then, HTML stays.

If the team wants offline support, bundle MathJax + Prism locally. Until then, CDN.
