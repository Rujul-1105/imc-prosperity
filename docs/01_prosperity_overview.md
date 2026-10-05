# IMC Prosperity — Competition Overview

This file is the canonical reference for what the competition is. Update it when IMC publishes new structure (they revise between editions).

## What it is

A global algorithmic trading competition hosted by **IMC Trading** (Amsterdam-headquartered global proprietary trading firm / market maker). The competition is simultaneously:

- A real-money-free trading game (you trade "XIRECs" or "SeaShells" — virtual currencies).
- A recruiting funnel. IMC's quant trader / quant researcher hires are heavily sourced from Prosperity alumni.
- An educational event. Tutorials introduce order books, options, etc.

## Format

- **1 tutorial round + 5 official rounds** in a ~15-day window.
- **Phase 1** (Rounds 1–2): ~72 hours each. Open to all comers.
- **Phase 2** (Rounds 3–5): ~48 hours each. Rankings reset.
- **Each round = Algorithmic challenge (Python submission) + Manual challenge (hand-submitted math/probability puzzles).**
- Both algorithmic and manual components contribute to the score.

## Teams

- Solo or up to 5 members.
- Team composition is editable in Rounds 1–2, then locked.

## Scale

- ~18,803 teams in Prosperity 4 (the prior cycle).
- Total prize pool: $50,000 (P4: 1st $25K, 5th $1.5K, manual winner $5K).
- The team's prior P4 result: ~rank 1000 globally in R1 and R2, then dropped out.

## How the algorithmic round works

1. IMC publishes a "round spec" PDF with:
   - Product names (e.g., AMETHYSTS, STARFRUIT, GIFT_BASKET, ORCHIDS, ASH, FRUIT).
   - The data files (CSV: order book snapshots, trades, external state) at [days -2, -1, 0, 1, 2].
   - Position limits, fee structure, market-maker rebate.
   - For each product, the underlying "world" — fair value evolution, exogenous factors, exchange structure.

2. You submit a Python file `trader.py` exposing a `Trader` class with a `run(state: TradingState) -> tuple[list[Order], int, str]` method.

3. IMC runs your trader against the round's actual price path. Your PnL is the score.

4. Top-N teams from R1 and R2 advance to Phase 2 (the team dropped out before this in P4).

## Manual round

- Hand-submitted answer to a math/puzzle question. ~25% of the score.
- Past puzzles have included: optimal stopping problems, expected value calculations, game-theoretic reasoning, simple optimization.
- All manual submissions are by team; only one answer is accepted per team.

## Product archetypes (the round types)

Recurring from P3 and P4:

1. **Fixed-fair-value** — e.g., AMETHYSTS at FV=10,000. Pure market-making.
2. **Mean-reverting (AR(1) / OU)** — e.g., STARFRUIT, ASH, FRUIT. z-score strategy.
3. **Noisy/volatile (GBM)** — generic dS = σ·dW. Short-horizon momentum or reversion.
4. **Externally-driven fundamentals** — e.g., ORCHIDS. Sunlight, humidity, shipping, tariff.
5. **Baskets/ETFs** — e.g., GIFT_BASKET = 4×CHOCOLATE + 6×STRAWBERRIES + 1×ROSES. PEBBLE where 5 assets sum to 50,000.
6. **Trend-following** — e.g., ROOT. Deterministic monotonic growth.
7. **Correlated groups** — e.g., SNACK (chocolate/vanilla neg correlated, strawberry/pistachio inverse raspberry with drift).
8. **Options on mean-reverting assets** — Black-Scholes, IV smile, delta-hedge.
9. **GBM-on-grid jumps** — coarse-grid projection of GBM, where ±100 jumps are exploitable (P4 R5 alpha).

The product mix changes year to year, but these archetypes recur.

## What beats the baseline

Top teams (P3 #1–#10, P4 #1–#20) consistently do:

1. Clean market making on fixed-FV rounds.
2. Mean-reversion fits (AR(1) or OU) on starfruit-style rounds.
3. Structural basket arb on GIFT_BASKET / PEBBLE rounds.
4. Cross-exchange factor model on ORCHIDS / MACARONS rounds.
5. Black-Scholes pricing + delta hedge on options rounds.
6. Microstructure edges: 1-tick-better pricing (no queue priority in Prosperity).
7. Bot fingerprinting: identify "informed" bots, mirror their trades, fade their anti-patterns.
8. PnL decomposition: separate spread, inventory drift, rebalance.

The team's prior P4 result suggests they did (1), (2) partially, and missed (3)–(7). This curriculum corrects that.

## Official resources

- https://prosperity.imc.com/ — the official portal. Per-round PDFs are gated; only authenticated users see them.
- https://www.imc.com/ — IMC corporate. They publish some retrospective material.
- Terms and Conditions PDF at https://prosperity.imc.com/docs/terms-and-conditions.pdf

The team has access to P3/P4 CSVs from prior cycles (in `prosperity-4/data_capsule/`). These are the substitute for the gated current round PDFs.

## Past editions and how they were won

See `02_past_winners.md` for full writeups. Highlights:

- **P3 #1** — Timo Diehm / Frankfurt Hedgehogs (2nd P3, 1st was a closely-related team). Open-source repo `TimoDiehm/imc-prosperity-3`. Read this.
- **P3 #25** — jmerle. Hybrid framework. Open-source at `jmerle/imc-prosperity-3`.
- **P4 #1** — "Seven-Deuce-Capital" (writeup still emerging).
- **P4 #96** — Leo Hawking. The richest retrospective in the public domain. `Leo-Hawking/IMC-Prosperity-4-Review`.

## Score

- PnL in XIRECs / SeaShells (virtual currency).
- Lower is worse, higher is better.
- Phase 1 and Phase 2 have separate rankings.
- Manual round is a separate leaderboard.
