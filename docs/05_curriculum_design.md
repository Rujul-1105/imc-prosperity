# Curriculum Design

The single most important document in `docs/`. It defines the design pattern that every module in `resources/` follows.

## The principle

**`explain.html` is the teaching. Everything else is support.**

The `explain.html` file is a **complete, self-contained, textbook-quality treatment** of the module's concept. It is so thorough that you do NOT need to read the source books to understand the concept — they exist for revision and a second-pass deeper read.

This is a deliberate inversion of the standard "cite, summarize, link" pattern. Summaries and links make you feel productive without actually teaching you anything. An explain.html that *teaches* you the concept — with derivations, worked examples, edge cases, and the math worked out — is more valuable than ten bibliographic references.

The order of reading a module:

1. **`explain.html`** — primary learning. Spend 2-3 hours here on first read. This is where the actual teaching happens.
2. **`source.html`** — optional. Just the citations (book, chapter, paper). For revision, second-pass deep reading, or when you need to cite the source in a writeup.
3. **`extract.html`** — quick reference. The cheat-sheet, formulas in our notation, code skeleton. Use this when implementing.
4. **`exercises.html`** — practice. Hands-on Python exercises that build muscle memory.
5. **`code/`** — runnable scripts. Read these after `extract.html` shows the formulas; they show the implementation.

## Why this pattern (not the standard one)

The standard pedagogy is "read the book, summarize it, link to more." That doesn't work for self-study:

- Reading 400 pages of Harris Ch 1-7 to learn "bid, ask, mid, spread, depth" is inefficient. You'll forget 80% by the time you finish.
- Summarizing the book gives you bullet points, not understanding.
- "Links to more" defer the actual learning indefinitely.

A better pattern: a single teacher writes a complete tutorial on the concept, tailored to your level and context. That's what `explain.html` is. The source books exist for:

- **Revision** — re-reading the same concept from a different angle strengthens recall.
- **Second-pass depth** — once you know the basics, you can read the book to fill in gaps, get the historical context, or see alternative derivations.
- **Citation** — when you write a paper or share a strategy, you cite the source.

## What goes in each file

### explain.html (THE teaching)

- Plain English explanation of the concept.
- The mechanism — how it works, in words and with diagrams.
- The math — every formula, derived step by step, with the intuition for each term.
- Worked examples with concrete numbers.
- Edge cases and failure modes.
- Common confusions and clarifications.
- Connections to Prosperity (which products, which rounds).
- A summary at the end that the reader can use as a self-test.

Target length: 15-30 KB. Long enough to be exhaustive; short enough to read in 2-3 hours.

### source.html (citations only)

- ONE main source per module (book, paper, repo) with chapter/section.
- 1-2 supplementary sources.
- What this module does NOT cover (and where to look).
- A short note on which sections to skip in the source (you don't need to read 400 pages).

Target length: 1-3 KB. No prose; just pointers.

### extract.html (our notation, code skeleton)

- The formulas in our notation.
- The code skeleton that implements the formulas.
- A worked example showing the formula in action.
- A cheat-sheet at the end.

Target length: 5-10 KB. The file you keep open while implementing.

### exercises.html

- 3-5 hands-on Python exercises per module.
- Each exercise references a known winning pattern from P3/P4.
- Each exercise corresponds to one script in `code/`.

Target length: 3-6 KB.

### code/

- Runnable Python scripts.
- Top of file: module docstring.
- Bottom: `if __name__ == "__main__":` self-test (< 5 seconds).
- Each script < 200 lines.

### README.html

- 1-page summary: what you'll know after this module, why it matters, where it shows in Prosperity.
- File index pointing to the other 4 files.

## Module layout

```
XX_module_name/
├── README.html         # 1-page summary
├── explain.html        # THE teaching (exhaustive, self-contained)
├── source.html         # citations for revision
├── extract.html        # formulas + code skeleton
├── exercises.html      # practice
└── code/               # runnable scripts
```

## Pedagogical ordering

The team should read each module in the order: `explain.html` → `extract.html` → `code/` → `exercises.html` → `source.html` (optional, for revision).

`source.html` is intentionally last. The team should not feel obligated to read the source books until they've already understood the concept from `explain.html`.

## How to write a good explain.html

A great `explain.html`:

1. **Starts with intuition.** "Imagine you're a market-maker..." — ground the concept in a concrete scenario before any math.
2. **Builds up gradually.** Don't dump a formula. Show what each piece means, why it's there, what changes if you remove it.
3. **Derives every formula.** Each formula is preceded by the setup, motivated, derived, and checked against a numerical example.
4. **Includes worked examples with numbers.** "Suppose bid=99, ask=101, volume=10/20. Then the mid is 100, the spread is 2, the microprice is..." — numbers make it real.
5. **Names the failure modes.** "This breaks when..." — every method has limits; honest about them.
6. **Connects to Prosperity.** "You'll see this in AMETHYSTS-style rounds" — the team needs to know this isn't abstract.
7. **Ends with a self-test.** A few "do you understand?" questions at the end let the reader check their own comprehension.

## Why "extract from source" is now in extract.html, not explain.html

The previous design had `extract.html` as "what we extracted from the source." That conflated two purposes: (a) translating the source into our notation, and (b) implementing the math.

The new design separates:
- `explain.html` teaches the concept from scratch (the source book is one of many inputs, but `explain.html` doesn't have to mirror its structure).
- `extract.html` shows the formulas in our notation, ready to be coded.
- `source.html` is just citations.

This is cleaner. The source book is an input to `explain.html`, not a structure that `explain.html` follows.

## What this design is NOT

- Not a list of books to read.
- Not a summary of the source material.
- Not a research archive.

It IS a complete self-contained tutorial, with the source books as supporting material for revision.
