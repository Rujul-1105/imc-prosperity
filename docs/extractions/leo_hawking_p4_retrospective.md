# Extraction: Leo Hawking's P4 Retrospective

**Source**: https://github.com/Leo-Hawking/IMC-Prosperity-4-Review
**Result**: Prosperity 4, 96th place globally (top 0.5%).
**Why we read this**: It's the richest post-mortem in the public domain. Required reading.

## Key insights

### 1. Recheck assumptions per round

> "Spread, volatility, tick size, queue priority differ each round. Don't carry P3 intuitions into P4."

**Implication for our curriculum**: each module's `extract.html` should specify which round-type it applies to, and the team's `code/` should be parameterized on round constants, not hard-coded.

### 2. Statistical models fail where you need them most

> "The extreme-deviation regions are where your mean-reversion model is most uncertain, but also where you want to bet big. Manually intervene or skip."

**Implication**: build a confidence interval on your signal, and don't trade when the CI is wide.

### 3. Two-person teams reinforce shared blind spots

> "Need adversarial voices. (Note: the team is 2 people. Be aware.)"

**Implication for the team**: explicitly assign one person to play devil's advocate on each strategy. "Why is this wrong?" is more valuable than "is this right?"

### 4. The P4 R5 grid-jump alpha

> "The 96th-ranked team would have moved into top 15 by trading ±100 grid jumps on the coarse-grid GBM round. Don't dismiss 'GBM has no alpha' as blanket truth — applies to GBM but not GBM projected onto a grid."

**Implication**: module 16 (grid jumps) is not optional. It's the highest-leverage single edge in the curriculum.

### 5. PnL decomposition

> "Separate spread, position drift, rebalancing cost. If spread capture is negative, the strategy is broken — even if total PnL is positive from drift."

**Implication**: every backtest in `resources/` should report spread / inventory / rebalance separately. The team's tools should make this a one-liner.

## Specific P4 round commentary

(Pulled from Leo's README; verify against the actual repo for the latest version.)

- **R1**: AMETHYSTS-style. Most teams got this right. Basic Wall-Mid or AS. The mistake was not sizing up after proving the edge.
- **R2**: Starfruit / basket-precursor. AR(1) fit was the differentiator. Some teams had stale params.
- **R3**: ORCHIDS. Cross-exchange factor model. The hidden alpha was the transport-cost asymmetry.
- **R4**: Options. Black-Scholes with smile fit. The mistake was hedging in the wrong direction (positive gamma when short gamma was correct).
- **R5**: Grid-jump alpha. Estimated price → trade next jump. The most missed edge of P4.

## What the team should take from this

1. The grid-jump trade is not optional. Build it.
2. Decompose PnL every time. Never accept a backtest that doesn't.
3. Question shared assumptions. One of you play skeptic.
4. Don't trust a model outside its training range.

## Source

- `Leo-Hawking/IMC-Prosperity-4-Review/README.md` (and the per-round sub-folders).
- The repo is mostly prose; treat the README as a long-form post-mortem.
