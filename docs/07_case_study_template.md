# Case Study Template

Used for `resources/01_past_winners/` — the dossier of top teams. The Timo Diehm writeup is the prototype.

## When to write a case study

For each top team that has public material (repo, writeup, video). Goal: another team member should be able to reproduce the team's strategy in <50 lines after reading.

## Structure (single HTML file)

```
01_timo_diehm_p3.html
├── Profile (team name, result, repo, style, stack)
├── Round-by-round breakdown (table)
├── Strategy deep-dive #1 (with code)
├── Strategy deep-dive #2 (with code)
├── Strategy deep-dive #3 (with code)
├── Patterns across rounds
├── What they did NOT do (and what we should)
├── Reproduce their work (steps)
└── Sources (links)
```

## Each strategy deep-dive has

1. **What is it?** — 1-paragraph plain English.
2. **Why it works** — the mechanism.
3. **Code** — extracted from the team's repo, lightly cleaned, with comments.
4. **Honest assessment** — pros, cons, when it fails.

## Required fields per case study

- Team name + members (if known).
- Result (rank, PnL).
- Repo / writeup links.
- Round-by-round product list.
- At least 2 deep-dives with code.
- A "what they didn't do" section.
- Reproducibility: anyone reading should know what to clone / what to read.

## Anti-patterns

- **Hero worship** — "Timo is so smart" is not useful. **What** did he do, **how** did it work?
- **Vague summaries** — "He used a market-making approach" is not enough. Show the code.
- **Marketing tone** — case studies are research notes, not testimonials.
- **Without code** — a case study without a code extract is a blog post. Skip it.

## Source material

Most useful:
- GitHub repos with clear strategy folders.
- Public writeups (Medium, blog posts).
- YouTube walkthroughs (transcripts).
- Past prosperity CSV data + the team's strategy to reproduce against.

Less useful:
- "I made rank X" tweets without code.
- Forum posts that summarize without showing.

## Maintenance

- Each new case study takes ~3-4 hours of work.
- Plan to add 1-2 case studies per curriculum cycle.
- Existing case studies: update if a new round drops material that the team later shared.
