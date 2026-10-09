# Module Template

Every module in `resources/XX_module_name/` follows this exact skeleton. Use it to create new modules.

## The principle (recap)

**`explain.html` is the teaching.** It's exhaustive, self-contained, and tailored to a beginner team. Reading the source books is not required.

## Folder layout

```
XX_module_name/
├── README.html         # 1-page summary: what, why, where in Prosperity
├── explain.html        # THE teaching (exhaustive, self-contained, 15-30 KB)
├── source.html         # citations for revision (1-3 KB, no prose)
├── extract.html        # formulas + code skeleton in our notation (5-10 KB)
├── exercises.html      # 3-5 hands-on Python exercises (3-6 KB)
└── code/               # runnable scripts, each < 200 lines
```

## README.html

Purpose: 1-page landing. The team should know in 30 seconds whether they need this module.

Sections:
1. **What you'll know after this module** — bulleted outcomes.
2. **Why this module comes [where it does]** — placement in the curriculum.
3. **Files in this module** — links to the other 4 files.
4. **Where this shows up in Prosperity** — products, rounds, edge cases.
5. **Time budget** — hours per file.
6. **Prerequisites** — which earlier modules to know.

Tone: terse, scannable.

## explain.html (THE teaching)

Purpose: complete self-contained tutorial. The team learns the concept here.

Sections (suggested):
1. **The story** — a 1-paragraph hook that motivates the concept in concrete terms.
2. **The mechanism** — how it works, in words, with diagrams (ASCII or simple).
3. **The math, derived** — every formula from setup to solution. Each term explained.
4. **Worked examples with numbers** — concrete scenarios, all numbers shown.
5. **Common confusions** — "this is NOT the same as X" clarifications.
6. **Failure modes** — when the method breaks, what happens.
7. **Connection to Prosperity** — which products, which rounds, what the team should do.
8. **Self-test** — 3-5 questions the reader can use to check comprehension.

Tone: like a private tutor explaining to a smart friend who's never taken a finance class.

Length: 15-30 KB (5,000-10,000 words). This is the bulk of the work.

Forbidden:
- "Read the source for more" (no — `explain.html` IS the teaching).
- Equations without surrounding prose explaining what they mean.
- Vague summaries.
- Skipping derivations.

## source.html

Purpose: just citations. The team consults this only for revision or citation.

Sections:
1. **Main source** (highlighted) — book chapter, paper, GitHub repo.
2. **Read this** — specific sections of the source. Skip the rest.
3. **Supplements** — 1-2 alternative sources.
4. **What this module does NOT cover** — where to look instead.
5. **Reading time budget** — be honest (e.g., "skim Ch 4 in 30 min if you want a second pass").

Tone: terse, no explanations. Just citations.

Length: 1-3 KB.

## extract.html

Purpose: formulas in our notation, ready to be coded. The file the team keeps open while implementing.

Sections:
1. **The primitives** — named quantities with symbols.
2. **The formulas, derived** — re-derived in our notation.
3. **The algorithm** — pseudocode, then a runnable Python sketch.
4. **A worked example** — using a real P3/P4 dataset or synthetic.
5. **A cheat-sheet** — quick reference.

Length: 5-10 KB.

Tone: technical, terse, runnable.

## exercises.html

Purpose: hands-on practice. Replicate known winning patterns.

Each exercise:
- Title + difficulty + time estimate.
- Goal: what you're implementing.
- Steps: pseudocode.
- Verify: how to know it worked.
- Reference: which past round / winner this replicates.

3-5 exercises per module, increasing in difficulty.

Length: 3-6 KB.

## code/

Purpose: runnable, < 200 lines each. Drop-in scripts for the team's experiments.

Conventions:
- Top of file: module docstring with one-line summary and usage.
- Bottom: `if __name__ == "__main__":` with a self-test.
- Use `numpy`, `pandas`, `statsmodels`, `scipy`, `py_vollib`, `arch`, `xgboost` as needed; nothing exotic.
- No external data files. Use synthetic data inside the script, or point to a documented CSV path the team already has.
- Style: PEP 8. Type hints. No comments explaining what the code obviously does.

## How the team uses a module

Weekly:

1. Open `README.html` (5 min).
2. Read `explain.html` carefully (2-3 hours). This is the bulk of the learning.
3. Open `extract.html` for the formulas and code skeleton.
4. Read `code/` scripts and run them.
5. Do `exercises.html` (1-2 hours).
6. Optionally, for revision: skim `source.html` and read the cited book chapter.

## Naming conventions

- Module folders: `XX_module_name/` with leading numeric prefix. `02_microstructure`, `03_market_making`, etc.
- Numbering reflects recommended order, not strict requirement.
- Special folders (not modules): `00_README.html`, `00_glossary.html`, `weekly_plan.html`, `01_past_winners/`, `20_mock_competition/`.
