# Past Winners — What #1 Teams Did

This is the dossier on every top-team writeup we can find. The team's curriculum (in `resources/01_past_winners/`) is built from this material.

---

## Timo Diehm / Frankfurt Hedgehogs — Prosperity 3, 2nd place

- **Repo**: https://github.com/TimoDiehm/imc-prosperity-3 (open source, ~1k stars)
- **Team size**: Small (2 people).
- **Style**: Heuristic-heavy. Heuristic > theory on tight deadlines.
- **Round-by-round**:
  - **R1 RAINFOREST_RESIN / KELP / SQUID_INK**: market making. The "Wall-Mid" approach. Place bid at the level just inside the largest visible bid wall, ask at the level just outside the largest ask wall. Captures distribution changes. Beats Avellaneda-Stoikov in this setting.
  - **R2** (adds CROISSANT, JAM, DJEMBE, PICNIC_BASKET): statistical arb + cross-asset. Detect liquidity-providing vs informed bots; quote with inventory skew.
  - **R3 GIFT_BASKET / CHOCOLATE / STRAWBERRIES / ROSES**: basket arb. Solve for basket constituents, trade basket-vs-legs spread.
  - **R4 MAGNIFICENT_MACARONS**: cross-exchange arb. External sunlight + transport + tariff. Famous heuristic: `int(external_bid + 0.5)`.
  - **R5 ASH / FRUIT options**: Black-Scholes + IV smile fit to historical. Quadratic in log-moneyness: `σ(K) = a + b·log(K/S) + c·log(K/S)²`. Coefficients: `[0.27362531, 0.01007566, 0.14876677]` for ASH. Delta-hedge in the underlying.
- **Patterns**:
  1. Heuristics <50 lines each. Avellaneda-Stoikov loses to Wall-Mid in practice.
  2. Hard-code round constants (transport, tariff, sun index). Don't model them.
  3. Separate "what to trade" from "how to interact with exchange."
  4. Always inventory-cap.
  5. PnL decomposition: spread capture, inventory drift, rebalance cost.
- **What they didn't do**: deep RL/ML, statistical cointegration tests, grid-jump alpha.
- **Extraction**: see `extractions/p3_round_1_rainforest_resin.md`, `p3_round_3_gift_basket.md`, `p3_round_4_macarons.md`, `p3_round_5_ash_fruit.md`.

---

## jmerle — Prosperity 3, 25th place

- **Repo**: https://github.com/jmerle/imc-prosperity-3
- **Style**: Clean abstraction layer. Code over heuristic.
- **Architecture**:
  - `Strategy` (base) → `StatefulStrategy` → `SignalStrategy` / `MarketMakingStrategy`.
  - `DeanonymizedTradesStrategy` for trading against Olivia's bot.
  - `RollingZScoreStrategy` for mean-reversion.
- **Tools also published**:
  - `prosperity3bt` (PyPI) — local backtester.
  - `prosperity-visualizer` (web) — visualize round output.
  - `prosperity-submit`, `prosperity-leaderboard` — submission + ranking helpers.
- **Use case**: Great template for the team's own visualizer/backtester. The hybrid.py abstraction is worth mirroring.

---

## Leo Hawking — Prosperity 4, 96th place

- **Repo**: https://github.com/Leo-Hawking/IMC-Prosperity-4-Review
- **Why this matters**: 96th is top 0.5%. The retrospective is the richest post-mortem in the public domain.
- **Key insights**:
  1. **Recheck assumptions per round** — spread, volatility, tick size, queue priority differ each round. Don't carry P3 intuitions into P4.
  2. **Statistical models fail where you need them most** (extreme deviations). Manually intervene or skip.
  3. **Two-person teams reinforce shared blind spots** — need adversarial voices. (Note: the team is 2 people. Be aware.)
  4. **Round-100 grid-jump trade** was the missed alpha in P4. Would have moved 96th to top 15. Don't dismiss "GBM has no alpha" as blanket truth — applies to GBM but not GBM projected onto a grid.
  5. **PnL decomposition matters** — separate spread, position drift, rebalancing cost.
- **Use case**: Required reading for module 16 (grid jumps) and module 19 (manual rounds).

---

## pe049395 (Korean team) — Prosperity 4, 2nd in R2

- **Repo**: https://github.com/pe049395/IMC-Prosperity-2024
- **Why this matters**: Top 3 in a single round, the only Asian team in the top 10 R2.
- **Key insight**: Heavy use of cross-sectional OLS regression across basket legs. More systematic than Timo's heuristics.

---

## Other top P3 / P4 teams (briefly)

- **P3 #1** — Anonymous (or related to Timo). Final PnL ~9.4M SeaShells.
- **P3 #7** — Chris Roberts, CMU Physics. Repo: `chrispyroberts`. Game-theoretic play.
- **P3 #9** — Carter T27 / "Alpha Animals". Repo: `CarterT27/imc-prosperity-3`.
- **P3 2nd overall** — Linear Utility. PnL 3.5M SeaShells.
- **P4 #4** — Une Baguette Fromage.
- **P4 #10** — FoxHenderson.
- **P4 #19** — JaneRT.
- **P4 #28** — DTU.
- **P4 #42** — Ape108.

---

## Patterns across all winners

1. **Wall-Mid or equivalent microstructure-aware quoting** is a top-100 baseline.
2. **Basket arb with OLS-solved weights** is the #1 differentiator in basket rounds.
3. **Black-Scholes + IV smile** is necessary for options rounds. Winners who skipped it finished bottom 50%.
4. **Cross-exchange factor model** with transport + tariff is the cross-exchange round's only edge.
5. **Bot fingerprinting** is rare but powerful. jmerle's DeanonymizedTradesStrategy is the only public example.
6. **Grid-jump alpha** is the most-missed edge. P4 R5. Anyone who did it moved up 80+ places.
7. **Manual round is 25% of score** and many teams ignore it. Top teams split a teammate onto it.
