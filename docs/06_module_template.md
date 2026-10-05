# Module Template

Every module in `resources/XX_module_name/` follows this exact skeleton. Use it to create new modules. The pattern is what makes the curriculum consistent.

## Folder layout

```
XX_module_name/
├── README.html         # 1-page: what this is, why it matters, where it shows in Prosperity
├── explain.html        # plain-English explanation (no math, no jargon, no refs)
├── source.html         # canonical book/paper (ONE main + 1-2 supplements)
├── extract.html        # formulas re-derived, code re-implemented, our words
├── exercises.html      # 3-5 Python exercises, each replicating a known winning pattern
└── code/               # tiny standalone .py scripts, each <200 lines, runnable on synthetic data
```

## README.html

Purpose: 1-page landing. The team should know in 30 seconds whether they need to read this module.

Sections:
1. **What you'll know after this module** — bulleted outcomes.
2. **Why this module comes [where it does]** — placement in the curriculum.
3. **Files in this module** — links to the other 4 HTML files.
4. **Where this shows up in Prosperity** — products, rounds, edge cases.
5. **Time budget** — hours per file.
6. **Prerequisites** — which earlier modules to know.

Tone: terse, scannable, no jargon without links.

## explain.html

Purpose: Build intuition. No math. No citations. Imagine explaining to a smart non-finance friend.

Sections:
1. **The story** — a 1-paragraph hook that motivates the concept.
2. **The mechanism** — how it works, in words.
3. **The edge case** — when does this break?
4. **The connection** — how does this show up in Prosperity?
5. **Pulling it together** — recap; link to extract.

Length: 500-1000 words. Tone: friendly, narrative.

Forbidden: equations, Greek letters, jargon without inline definition, citations to papers (those go in source.html).

## source.html

Purpose: Anchor in authority. Tell the team what to read (or skim) in the canonical source.

Sections:
1. **Main source** (highlighted) — book chapter, paper, GitHub repo.
2. **Read this** — specific chapters / sections. Skip the rest.
3. **Supplements** — 1-2 alternative sources for cross-reference.
4. **What this module does NOT cover** — where to look instead.
5. **Reading time budget** — be honest.

Forbidden: explanations of the concept itself (that's explain.html and extract.html).

## extract.html

Purpose: Translate the source into your own context. The file you actually do the math from.

Sections:
1. **The primitives** — named quantities with symbols.
2. **The formulas** — derived in your notation, with working code.
3. **The algorithm** — pseudocode, then a runnable Python sketch.
4. **A worked example** — using a real P3/P4 dataset.
5. **A cheat-sheet** — quick reference at the end.

Length: 1000-3000 words. Tone: technical, terse, runnable.

Allowed: equations (with MathJax), code (with Prism syntax highlighting), tables.

Forbidden: lengthy prose explanations (those go in explain.html).

## exercises.html

Purpose: Build muscle memory. Replicate known winning patterns.

Each exercise:
- Title + difficulty + time estimate.
- Goal: what you're implementing.
- Steps: pseudocode.
- Verify: how to know it worked.
- Reference: which past round / winner this replicates.

Format: 3-5 exercises per module, increasing in difficulty. Each exercise corresponds to one script in `code/`.

Forbidden: theory. Exercises are about doing.

## code/

Purpose: Runnable, <200 lines each. Drop-in scripts for the team's experiments.

Conventions:
- Top of file: module docstring with one-line summary and usage.
- Bottom of file: `if __name__ == "__main__":` with a self-test.
- Use `numpy`, `pandas`, `statsmodels` as needed; nothing exotic.
- No external data files. Use synthetic data inside the script, or point to a documented CSV path the team already has.

Style: PEP 8. Type hints. No comments explaining what the code does (the code should be self-evident). One comment per non-obvious decision.

## How the team uses a module

Weekly:

1. Read `README.html` (5 min).
2. Read `explain.html` (30 min).
3. Skim `source.html` to know where it comes from (15 min).
4. Read `extract.html` carefully, reproducing the formulas by hand (60 min).
5. Open `exercises.html`, do one exercise per day (60 min × 5).
6. Commit by Sunday.

## Naming conventions

- Module folders: `XX_module_name/` with leading numeric prefix. `02_microstructure`, `03_market_making`, etc.
- Numbering reflects recommended order, not strict requirement.
- Special folders (not modules): `00_README.html`, `00_glossary.html`, `weekly_plan.html`, `01_past_winners/`, `20_mock_competition/`.
