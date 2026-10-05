# CLAUDE.md

This file is for future Claude Code (or other AI agents) working on this repo. Read it before making commits.

## Commit convention (enforced)

All commits in this repo are authored by **Rujul-1105 \<rujulmatta36@gmail.com\>**. No exceptions.

**Trailer rule — when to keep `Co-Authored-By: Claude Code`:**

- **KEEP** the trailer when the commit touches any of:
  - `docs/` (regeneration context, sources, extractions, prior_work)
  - `CLAUDE.md`
  - `README.md` (top-level)
  - `.claude/` (Claude Code settings)
  - Anything explicitly marked as agent/AI-facing meta-documentation.

- **STRIP** the trailer for everything else: `resources/`, `code/`, visualizer/backtester work, dataset changes, etc.

**Why:** the user wants the commit history to clearly show what was AI-assisted (agent-facing work) versus what they own directly (their actual study/build material). Mixing them dilutes the signal.

## Local git config (run once when starting a new session)

```bash
git config user.name  "Rujul-1105"
git config user.email "rujulmatta36@gmail.com"
```

Do NOT set these to a Claude identity. Verify with `git config user.name` before any commit.

## Commit message style

- Subject line: imperative mood, ≤72 chars (e.g. "Add module 07 (Options & Greeks)").
- Body: 3–6 bullets listing what changed. Verifications go in a final bullet ("All self-tests pass." or "Verified: ...") when applicable.
- Trailer: only the Co-Authored-By line, only on commits that warrant it per the rule above.

## Other conventions

- All `resources/` content is HTML (browser-renderable). See `docs/08_style_guide.md` for the canonical CSS, MathJax, and Prism usage.
- All `docs/` content is Markdown (machine-grep-friendly).
- Python code in `resources/XX/code/` runs `<5s` self-tests via `if __name__ == "__main__":`. Every script must pass its self-test before being committed.
- Don't push without the user's explicit "push" instruction.
