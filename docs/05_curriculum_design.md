# Curriculum Design

The single most important document in `docs/`. It defines the design pattern that every module in `resources/` follows.

## The principle

**Explain first. Then source. Then extract. Then practice.**

Every concept is taught in this exact order:

1. **Explain** — plain English. No math, no jargon, no citations. Imagine explaining to a smart friend who's never taken a finance class.
2. **Source** — point to the canonical book/paper. Chapter, page, link. ONE main source + 1-2 supplements.
3. **Extract** — formulas re-derived, code re-implemented, key diagrams re-described in **our** words. The file you actually do the math from.
4. **Practice** — Python exercises that replicate a known winning pattern.

This is the optimal learning loop for a self-study team:

- Read `explain.html` until you can describe the concept in plain words.
- Glance at `source.html` to know where it came from.
- Use `extract.html` to actually do the math or write the code.
- Run the exercises in `code/`.
- Commit when done.

## Why this pattern works

| Step | Cognitive load | Purpose |
|---|---|---|
| Explain | Low (just words) | Build intuition. "What is it, why does it matter?" |
| Source | Low (just a pointer) | Anchor in authority. "Is this real? Where do I learn more?" |
| Extract | Medium (math + code) | Make it actionable. "How do I do this myself?" |
| Practice | High (run code) | Build muscle memory. "Can I do this under time pressure?" |

The four steps map to Bloom's taxonomy: Understand → Recall → Apply → Analyze. Skipping any step leaves a gap.

## Why "extract" not "summarize"

A summary tells you what the source said. An **extraction** translates the source into your context.

- For Harris Ch 1–3: a summary is "Harris defines a limit order book as...". An extraction is "Here are the five primitives we use every day: bid, ask, mid, spread, microprice. Here are the formulas in our notation. Here's code that implements them."
- For Avellaneda–Stoikov: a summary is "AS solves a stochastic control problem...". An extraction is "Here are the four equations you actually code. The first gives the reservation price, the second the optimal spread. γ and κ are parameters; how to fit them on a past round is in exercises."

Extract, don't summarize.

## The "Prosperity-shaped" requirement

Every module must answer:

- **Which past product does this apply to?** (AMETHYSTS, STARFRUIT, etc.)
- **What is the typical PnL contribution of getting this right?**
- **What is the loss from getting this wrong?**

If a module can't answer these, it's not a Prosperity module — it's general finance trivia.

## The 2-person optimization

Each module is self-contained enough that two people can work in parallel on different modules and reconvene to share extract files. The `weekly_plan.html` flags split weeks (5, 9, 11, 16).

## Pacing

- **1 week per module** is the average. Heavy modules (7 — options) get more time. Light modules (15 — Python toolkit) get less.
- **Total**: 16 weeks core + 4 weeks advanced.
- **Rest**: week 8 is review, no new content. Use it to consolidate.
- **Mock round**: week 16 is a full dry run on past data.

## File-level details

- Each module is one folder: `XX_module_name/`.
- Each folder has 5 files: `README.html`, `explain.html`, `source.html`, `extract.html`, `exercises.html`.
- Plus a `code/` subfolder with runnable Python scripts.
- The README is a 1-page summary; everything deeper is in the other four files.

See `06_module_template.md` for the exact skeleton.

## What this design is NOT

- Not a list of books to read. Reading the books is one of five steps, not the whole thing.
- Not a video course. No videos. (Walls of text are skim-able; videos aren't.)
- Not a notebook dump. We write pedagogical notes, not research logs.
- Not a research archive. Research notes go in `extractions/`; only the polished extract makes it into `resources/`.
