# Winning Strategies — Catalog

The complete list of strategies used by P3/P4 top teams. Each maps to a `resources/` module.

---

## 1. Fixed-FV market-making

- **Used for**: AMETHYSTS-style rounds.
- **Approach**: Tight two-sided quotes with inventory skew.
- **Code**: Wall-Mid (Timo) or Avellaneda-Stoikov (paper).
- **Edge**: 1-tick-better pricing in Prosperity's no-queue-priority exchange.
- **Module**: `resources/03_market_making/`.

## 2. Mean-reversion (OU / AR(1))

- **Used for**: STARFRUIT, ASH, FRUIT.
- **Approach**: Fit AR(1) (or OU), compute half-life, z-score. Bet mean reversion when |z| > threshold.
- **Edge**: Estimated from data; ~5-15% annualized is realistic.
- **Module**: `resources/04_mean_reversion/`.

## 3. Cross-exchange arbitrage

- **Used for**: ORCHIDS, MACARONS.
- **Approach**: Build a factor model. Net out transport + tariff. Trade when the two exchanges disagree.
- **Edge**: Often "free" if the round spec gives you the model coefficients.
- **Module**: `resources/08_cross_exchange_arb/`.

## 4. Basket arbitrage

- **Used for**: GIFT_BASKET, PEBBLE.
- **Approach**: Solve for basket weights. Compute NAV. Trade when `basket − NAV > threshold`.
- **Edge**: For PEBBLE-style rounds, inner rebalancing gives zero-risk PnL.
- **Module**: `resources/06_etf_basket_arb/`.

## 5. Linear trend capture

- **Used for**: ROOT-style rounds.
- **Approach**: Two-stage position build. Start small, scale up.
- **Edge**: The deterministic drift.
- **Module**: `resources/09_trend_following/`.

## 6. Options pricing + delta hedge

- **Used for**: ASH options, FRUIT options.
- **Approach**: Black-Scholes + IV smile fit. Delta-hedge in underlying. Manage vega.
- **Edge**: The mispricing between the smile-implied and the realized vol.
- **Module**: `resources/07_options_greeks/`.

## 7. Microstructure: 1-tick-better pricing

- **Used for**: All L3 books.
- **Approach**: Post a quote 1 tick inside the best bid/ask. Fill first because no queue priority.
- **Edge**: 1 tick per round-trip. Compounds.
- **Module**: `resources/02_microstructure/` (built into `resources/03_market_making/`).

## 8. Wall-mid

- **Used for**: AMETHYSTS-style rounds with visible walls.
- **Approach**: Bid at the level just inside the largest wall, ask just outside. Captures wall re-positioning.
- **Edge**: Walls are predictable; their movement is PnL.
- **Module**: `resources/03_market_making/`.

## 9. Bot fingerprinting

- **Used for**: Rounds with named "competitor" bots (Olivia, Mark14, Mark55, etc.).
- **Approach**: Identify each bot's strategy by their trade pattern. Mirror the informed ones, fade the uninformed ones.
- **Edge**: ~10-30% over baseline in the right round.
- **Module**: `resources/13_game_theory_bots/`.

## 10. Grid-jump alpha

- **Used for**: Coarse-grid GBM rounds (P4 R5).
- **Approach**: Smooth the price to estimate true GBM. Trade the next-grid-jump.
- **Edge**: ~50-100% in the right round. Rare opportunity.
- **Module**: `resources/16_grid_jumps_special/`.

## 11. Cross-sectional OLS (correlated groups)

- **Used for**: SNACK-style rounds.
- **Approach**: Regress prices on a common factor. Trade residual.
- **Edge**: Comparable to pairs trading.
- **Module**: `resources/05_cointegration/`.

## 12. Bayesian fair-value estimation

- **Used for**: Rounds with prior knowledge of the process.
- **Approach**: Maintain a posterior over fair value. Update on each tick. Trade when posterior diverges from market.
- **Edge**: Better than point estimates for noisy processes.
- **Module**: `resources/11_bayesian_signals/`.

## 13. ML signal generation (XGBoost, NN)

- **Used for**: Any round with enough features.
- **Approach**: Engineer features (microprice, imbalance, volatility). Train gradient boosting on past days. Predict next move.
- **Edge**: Modest (~3-8%) if features are good. **Do not** expect miracles.
- **Module**: `resources/12_ml_signals/`.

## 14. Inventory-aware market making

- **Used for**: All market-making rounds.
- **Approach**: Skew your quotes by inventory. When long, lower both sides. When short, raise both.
- **Edge**: Prevents inventory blowup, which is the #1 cause of negative PnL.
- **Module**: `resources/03_market_making/`.

## 15. Statistical arbitrage (cointegration pairs)

- **Used for**: Pairs of correlated assets.
- **Approach**: Engle-Granger test for cointegration. Bet the gap closes.
- **Edge**: Sharpe 1-3 if the pair is genuinely cointegrated.
- **Module**: `resources/05_cointegration/`.

## 16. Volatility trading (GARCH)

- **Used for**: Rounds where vol is tradeable.
- **Approach**: GARCH forecast of vol. Size positions by forecast.
- **Edge**: Better risk management, not direct PnL.
- **Module**: `resources/10_volatility/`.

---

## Common pitfalls (also from winners' retrospectives)

1. **Treating "negative lag-1 ACF" as always-untradable** (true only when jump size << spread). See `resources/04_mean_reversion/`.
2. **Sharing one backtester across rounds** (branch creep). Use per-round backtesters.
3. **Position drift dominating spread capture** in PnL. Always inventory-cap.
4. **Over-validating weak signals** while paralyzed on verified structures.
5. **Fitting on the entire training period** — overfits. Use walk-forward.
6. **Ignoring manual round** (25% of total score).
7. **Premature entry into a competitive round** without the right tooling.
