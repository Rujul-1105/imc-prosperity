# GitHub Repos — Canonical Sources

Every repo the curriculum uses or references.

---

## TimoDiehm/imc-prosperity-3 (2nd P3, Frankfurt Hedgehogs)

- **URL**: https://github.com/TimoDiehm/imc-prosperity-3
- **Stars**: ~1k
- **Why**: The cleanest, most directly teachable P3 winner repo.
- **Used in**: Module 01 (case study), plus specific extractions in Modules 03, 06, 07, 08.
- **What to read**:
  - `round_1_strategy.py` — Wall-Mid market making.
  - `round_3_strategy.py` — GIFT_BASKET basket arb.
  - `round_4_strategy.py` — MACARONS cross-exchange.
  - `round_5_strategy.py` — ASH/FRUIT options with IV smile.

## jmerle/imc-prosperity-3 (25th P3)

- **URL**: https://github.com/jmerle/imc-prosperity-3
- **Why**: The best abstraction layer. `Strategy` → `StatefulStrategy` → `SignalStrategy` / `MarketMakingStrategy`. Also publishes `prosperity3bt` (backtester) and `prosperity-visualizer`.
- **Used in**: Module 01 (case study), Module 02 (microstructure tools), Module 13 (DeanonymizedTradesStrategy for bot fingerprinting).
- **What to read**:
  - `prosperity/hybrid.py` — the abstraction layer.
  - `prosperity/strategies/` — example strategies including the rolling z-score.
  - `prosperity/data.py` — the TradingState / datamodel structure.

## jmerle/prosperity3bt (backtester)

- **URL**: https://github.com/jmerle/prosperity3bt
- **PyPI**: `pip install prosperity3bt`
- **Why**: A drop-in local backtester. Use this for module exercises until the team builds their own.
- **Used in**: Module 20 (mock competition).

## jmerle/prosperity-visualizer (web visualizer)

- **URL**: https://github.com/jmerle/prosperity-visualizer
- **Why**: A web-based visualizer for round output. Use this to debug your strategies.
- **Used in**: Module 20 (mock competition).

## Leo-Hawking/IMC-Prosperity-4-Review (P4 #96, post-mortem)

- **URL**: https://github.com/Leo-Hawking/IMC-Prosperity-4-Review
- **Why**: The richest retrospective. Required reading.
- **Used in**: Module 01 (case study), Module 16 (grid jumps), Module 19 (manual rounds).
- **What to read**: the README. Every paragraph.

## pe049395/IMC-Prosperity-2024 (P4 #2 in R2)

- **URL**: https://github.com/pe049395/IMC-Prosperity-2024
- **Why**: A Korean team in top 3 of a single round. Heavy use of cross-sectional OLS.
- **Used in**: Module 05 (cointegration), Module 06 (basket arb).

## BlackArbsCEO/Adv_Fin_ML_Exercises (López de Prado companion)

- **URL**: https://github.com/BlackArbsCEO/Adv_Fin_ML_Exercises
- **Why**: Exercises for AFML Ch 1-7. Used in Module 12.

## hudson-and-thames/mlfinlab (production ML for finance)

- **URL**: https://github.com/hudson-and-thames/mlfinlab
- **Why**: Production-grade implementation of AFML. Reference for the team's own implementation.
- **Used in**: Module 12.

## astraflow/avellaneda-stoikov (reference implementation)

- **URL**: https://github.com/astraflow/avellaneda-stoikov
- **Why**: A faithful C++ and Python implementation of the AS paper. Use to compare against your own.

## chrispyroberts/imc-prosperity-3 (P3 #7, CMU Physics)

- **URL**: search "chrispyroberts imc-prosperity-3" on GitHub
- **Why**: A physics-trained top-10 team. Game-theoretic play. Good supplement.

## CarterT27/imc-prosperity-3 (P3 #9, "Alpha Animals")

- **URL**: search on GitHub
- **Why**: Another top-10 open-source repo.

## GeyzsoN/prosperity-rs (Rust backtester, 20× faster)

- **URL**: search on GitHub
- **Why**: A Rust port of the backtester, much faster than the Python one. Useful for heavy ML experiments.

---

## How to use these

For each repo:

1. Clone it.
2. Read the README.
3. Find the file that corresponds to the round you care about.
4. Read the strategy code top-down. Note the structure (`__init__` state, `get_orders` decision, helpers).
5. Re-implement in your own code from scratch. Diff.
6. Don't copy. Copying teaches nothing.

If a repo's structure is appealing (jmerle's hybrid.py is the prime example), mirror the abstraction — not the implementation.
