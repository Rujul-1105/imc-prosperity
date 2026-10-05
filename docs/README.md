# docs/ — Regeneration Context

This directory is the **complete context dump** for producing `resources/`. Its purpose: if a new agent (or a new system) starts from scratch with only this folder, it should be able to rebuild a near-identical `resources/` curriculum.

## What goes here vs. `resources/`

| Folder | Audience | Format | Purpose |
|---|---|---|---|
| `resources/` | The team learning | `.html` (browser) | The actual curriculum — explanations, source pointers, extracted notes, exercises |
| `docs/` | Future agents / context restoration | `.md` (machine-grep) | The raw research, design rationale, source catalog, and extractions that produced `resources/` |

`resources/` is the artifact. `docs/` is the provenance.

## Folder layout

```
docs/
├── README.md                          # this file
├── 00_team_context.md                 # who we are, what we did in P4, stakes
├── 01_prosperity_overview.md          # what the competition is, structure, scoring
├── 02_past_winners.md                 # Timo, jmerle, Leo-Hawking, pe049395 with key takeaways
├── 03_product_archetypes.md           # recurring product types and what they require
├── 04_winning_strategies.md           # strategy catalog
├── 05_curriculum_design.md            # the explain / source / extract pattern
├── 06_module_template.md              # standard module skeleton
├── 07_case_study_template.md          # case study format (Timo is the prototype)
├── 08_style_guide.md                  # HTML conventions, MathJax, Prism, code style
├── 09_weekly_plan_rationale.md        # why 16 weeks, why this ordering
├── 10_format_decisions.md             # why HTML for resources, .md for docs
│
├── sources/                           # every external source we used
│   ├── 00_books.md                    # Harris, Hull, Chan, López de Prado, etc.
│   ├── 01_papers.md                   # Avellaneda-Stoikov, Engle-Granger, BIS, etc.
│   ├── 02_github_repos.md             # Timo, jmerle, Leo-Hawking, pe049395
│   └── 03_web_resources.md            # QuantConnect, QuantInsti, thinkbayes
│
├── extractions/                       # what we extracted from each source
│   ├── p3_round_1_rainforest_resin.md
│   ├── p3_round_2.md
│   ├── p3_round_3_gift_basket.md
│   ├── p3_round_4_macarons.md
│   ├── p3_round_5_ash_fruit.md
│   ├── p4_round_5_grid_jumps.md
│   ├── jmerle_hybrid_framework.md
│   ├── leo_hawking_p4_retrospective.md
│   └── avellaneda_stoikov_paper.md
│
└── prior_work/                        # what we did in P4, what failed
    └── prosperity_4_summary.md
```

## How to use this folder

**If you're an agent regenerating resources/ from scratch:**
1. Start with `00_team_context.md` and `01_prosperity_overview.md` to understand the task.
2. Read `05_curriculum_design.md` and `06_module_template.md` to learn the pattern.
3. Use `sources/` to know what to read.
4. Use `extractions/` as pre-extracted raw material — copy into `resources/XX_module/extract.html` rather than re-reading the source.
5. Mirror the style in `08_style_guide.md`.

**If you're the team and want to add a new module:**
1. Read `06_module_template.md`.
2. Find the right book in `sources/00_books.md`.
3. Read the relevant chapter.
4. Write your notes following the extract pattern.
5. Add a new entry to `extractions/` so future agents don't re-do your work.

**If you're auditing the curriculum:**
1. Cross-check every claim in `resources/02_microstructure/extract.html` against `extractions/avellaneda_stoikov_paper.md` (or whichever source).
2. Verify style with `08_style_guide.md`.

## Conventions

- **Markdown** for everything in this folder. No HTML, no PDFs.
- **Source citations** always as full links: book chapter, paper section, GitHub commit hash.
- **Tone**: research notes. Write to be useful to a future agent, not to read like prose.
- **Updates**: this folder is a living document. Every time a new module is built, also add the extraction notes here.
