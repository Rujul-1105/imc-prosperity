# Product Archetypes

The recurring types of products Prosperity puts in front of you. Each archetype has a specific strategy recipe. Knowing which archetype you're in = knowing which `resources/` module to open.

---

## 1. Fixed-fair-value (FFV)

**Example**: AMETHYSTS (P3, P4) at FV=10,000.

**What's going on**: The asset has a known, deterministic fair value. It still trades on an L3 order book with a spread. Your job: capture the spread, don't get run over when the true value moves.

**Strategy**: Tight market making. Wall-Mid (Timo) or Avellaneda-Stoikov (paper). Inventory cap hard. PnL = spread capture − adverse selection.

**Module**: `resources/02_microstructure/` + `resources/03_market_making/`.

**Past-winner example**: Timo P3 R1 (Wall-Mid on RAINFOREST_RESIN — same archetype).

---

## 2. Mean-reverting (AR(1) / OU)

**Examples**: STARFRUIT (P3, P4), ASH (P3, P5?), FRUIT (P3, P5?).

**What's going on**: The price follows an AR(1) or OU process. It wanders but is pulled back to a center.

**Strategy**: Fit AR(1), compute half-life, z-score. When |z| > threshold, bet the spread closes. The harder part is not entry — it's sizing against the half-life.

**Module**: `resources/04_mean_reversion/`.

**Past-winner example**: jmerle's RollingZScoreStrategy.

---

## 3. Noisy / volatile (GBM)

**Example**: Generic products with `dS = σ·dW`.

**What's going on**: Pure noise. No mean reversion, no trend. The spread is the only edge, and it's small.

**Strategy**: Don't trade. Or: market-make very tightly with very high inventory caps. The "edge" is the rebate, not directional.

**Module**: `resources/03_market_making/`.

**Past-winner example**: SQUID_INK in P3 R1.

---

## 4. Externally-driven fundamentals

**Example**: ORCHIDS (P3, P4). Sunlight + humidity + shipping + tariff.

**What's going on**: The asset's fair value depends on observable external signals. The signals are given in the round spec. Compute fair value, trade the spread.

**Strategy**: Build a factor model. `FV = α + β₁·sunlight + β₂·humidity − β₃·tariff + ...`. Re-fit per round. Trade when market price deviates.

**Module**: `resources/08_cross_exchange_arb/` (this is the ORCHIDS module).

**Past-winner example**: P3 R4 MACARONS, P4 R3 ORCHIDS.

---

## 5. Basket / ETF

**Examples**: GIFT_BASKET (P3, P4) = 4×CHOCOLATE + 6×STRAWBERRIES + 1×ROSES. PEBBLE (P4) = sum of 5 assets = 50,000.

**What's going on**: The "basket" is a synthetic instrument with a known linear combination of constituents. If you can buy the basket and sell the legs (or vice versa) for more than zero, you have risk-free PnL.

**Strategy**:
- Solve for basket weights from the data (OLS or simple inspection).
- Compute NAV at every tick.
- Trade when `basket_market − NAV > threshold` (long basket, short legs) or vice versa.
- For PEBBLE-style: inner rebalancing gives pure PnL (zero directional risk).

**Module**: `resources/06_etf_basket_arb/`.

**Past-winner example**: Timo P3 R3 GIFT_BASKET.

---

## 6. Trend-following (deterministic monotonic)

**Example**: ROOT (P3, P4). Linear growth.

**What's going on**: The price increases by a fixed amount per tick. The "edge" is the spread you can capture while loading up.

**Strategy**: Two-stage position build. Start with a small position, scale up as you confirm the trend. Don't try to predict when it ends.

**Module**: `resources/09_trend_following/`.

**Past-winner example**: Timo P3 R? (specific to a trend round).

---

## 7. Correlated groups

**Example**: SNACK (P4). Chocolate/vanilla negatively correlated. Strawberry/pistachio inverse raspberry with drift.

**What's going on**: Multiple products with known relationships. The edge is finding pairs/triples that misprice together.

**Strategy**: Cross-sectional OLS. Compute the residuals, trade when residual is large.

**Module**: `resources/05_cointegration/`.

---

## 8. Options on mean-reverting assets

**Examples**: ASH options (P3, P4), FRUIT options (P3, P4).

**What's going on**: The underlying is mean-reverting, but you trade options on it. Black-Scholes assumes GBM, which is wrong. You need to fit an IV smile and hedge delta.

**Strategy**:
1. Fit IV smile in log-moneyness.
2. Price options with BS + smile.
3. Delta-hedge in underlying.
4. Manage vega exposure.

**Module**: `resources/07_options_greeks/`.

**Past-winner example**: Timo P3 R5 ASH/FRUIT options.

---

## 9. GBM-on-grid jumps

**Example**: P4 R5 (an alpha opportunity, not a specific product). A GBM projected onto a coarse price grid.

**What's going on**: When the true price moves by more than the grid spacing, the next-tick price "jumps" by the grid size. The jump is predictable if you can estimate the true price.

**Strategy**: Estimate true price (smoothed), trade the next jump.

**Module**: `resources/16_grid_jumps_special/`.

**Past-winner example**: Leo Hawking's P4 R5 retrospective. The team that did this moved from 96th to top 15.

---

## How to identify the archetype on a new round

When the round spec drops, ask:

1. Is the fair value given or computable? → FFV or externally-driven.
2. Is there a basket formula? → Basket.
3. Are there options? → Options.
4. Is there a separate "external" exchange? → Cross-exchange.
5. Are there multiple products with shared structure? → Correlated groups.
6. Does the price process look like AR(1) (lag-1 autocorrelation negative)? → Mean-reverting.
7. Does the price drift linearly? → Trend.
8. Otherwise: GBM. Don't trade, or market-make.

This taxonomy is the table of contents of the curriculum. Each module = one archetype (with overlap).
