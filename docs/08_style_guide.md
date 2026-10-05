# Style Guide

The conventions for writing files in `resources/`. Consistency lets the team skim fast and the future-agent regenerate fast.

## HTML

### Top-of-file boilerplate

Every HTML file starts with the same skeleton. Copy-paste from any existing module file.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Module XX — Title</title>
<style>...</style>
<script>MathJax = { tex: { inlineMath: [['$','$'], ['\\(','\\)']] } };</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/prismjs@1/themes/prism-tomorrow.css">
<script src="https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-core.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/prismjs@1/components/prism-python.min.js"></script>
</head>
<body>
<div class="wrap">
```

### Inline CSS

The full CSS used in the existing modules:

```css
:root { --fg:#1a1a1a; --muted:#666; --accent:#0a66c2; --bg:#fafafa; --card:#fff; --border:#e5e5e5; --alt:#f4f4f4; }
* { box-sizing: border-box; }
body { font: 16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; color:var(--fg); background:var(--bg); margin:0; padding:0; }
.wrap { max-width: 880px; margin: 0 auto; padding: 32px 24px 80px; }
header { border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }
h1 { font-size: 28px; margin: 0 0 8px; }
h2 { font-size: 22px; margin-top: 32px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
h3 { font-size: 17px; margin: 22px 0 4px; color: var(--accent); }
p { margin: 8px 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background: #f1f1f1; padding: 1px 5px; border-radius: 3px; font-size: 0.92em; }
pre { background: #1e1e1e; color: #d4d4d4; padding: 14px 18px; border-radius: 6px; overflow-x: auto; line-height: 1.45; font-size: 13px; }
pre code { background: transparent; padding: 0; color: inherit; font-size: inherit; }
ul, ol { padding-left: 22px; }
li { margin: 6px 0; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; vertical-align: top; }
th { background: #f4f4f4; font-weight: 600; }
tr:nth-child(even) td { background: #fcfcfc; }
blockquote { border-left: 4px solid var(--accent); margin: 16px 0; padding: 4px 16px; background: #f0f7ff; color: #333; }
.meta { color: var(--muted); font-size: 14px; }
.badge { display: inline-block; background: var(--accent); color: #fff; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 10px; }
.badge.adv { background: #6f42c1; }
footer { margin-top: 64px; padding-top: 16px; border-top: 1px solid var(--border); font-size: 13px; color: var(--muted); }
```

Don't add custom CSS unless the module truly needs it (e.g., graphs). Keep the look uniform.

### CDN dependencies

Only two are allowed:
- **MathJax 3** (jsdelivr).
- **Prism.js** (jsdelivr, with `prism-tomorrow` theme, `python` and `bash` languages).

No other CDNs. No Google Fonts (use system font stack). No images (use ASCII diagrams or skip).

### MathJax

Inline: `$x = 2$`. Display: not needed in current modules. Keep equations inline when possible.

### Prism

Use `class="language-python"` on `<pre><code>` blocks. Don't override colors. The default `prism-tomorrow` works.

## Markdown (docs/)

- Standard CommonMark.
- Headers: ATX (`#`, `##`). No Setext.
- Code fences with language hints.
- Tables: pipe tables.
- Links: `[text](url)` form. No reference-style.

## Python (code/)

- PEP 8.
- Type hints on every public function.
- Module docstring at the top with one-line summary and usage.
- `if __name__ == "__main__":` self-test that runs in <5 seconds.
- No external data files. Use synthetic data inline.
- Imports: `numpy`, `pandas`, `statsmodels`, `scipy`, `py_vollib`, `arch`, `xgboost`. Nothing exotic.
- Comments: one per non-obvious decision. No comments explaining what the code obviously does.

## Filenames

- `snake_case` for everything.
- `XX_module_name/` for module folders (e.g., `02_microstructure/`).
- `XX_specific_name.html` for files within a module (e.g., `00_README.html`).

## Voice

- Plain, direct, slightly informal.
- Address the team as "you" (or "we" when describing joint work).
- Don't be chatty. Don't be cute.
- No emoji. No "let me explain..." preambles.
- Citations: link with descriptive text (`[Harris Ch 3](https://...)` not `[click here](url)`).

## What to avoid

- Walls of text without headings.
- Equations without surrounding prose explaining what they mean.
- Code blocks without a "what this does" sentence before.
- Tables that don't have units in the column headers.
- "TODO" or "FIXME" left in committed files.
- Hard-coded paths like `/home/user/data/`. Use relative paths.
