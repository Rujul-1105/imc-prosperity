# Extraction: P3 Round 3 — GIFT_BASKET

**Source**: Timo Diehm's `round_3_strategy.py`.
**Round**: P3 R3. Products: GIFT_BASKET, CHOCOLATE, STRAWBERRIES, ROSES, plus the basket's constituents.

## The setup

GIFT_BASKET = 4 × CHOCOLATE + 6 × STRAWBERRIES + 1 × ROSES.

If the basket trades at $basket and the constituents are $choc, $straw, $rose, the theoretical NAV is:

```
NAV = 4 * choc + 6 * straw + 1 * rose
```

The trade: when `basket_market > NAV + threshold`, sell basket / buy legs. When `basket_market < NAV - threshold`, buy basket / sell legs. Capture the spread.

## What we extracted

### 1. Threshold-based structural arb

Timo's basket strategy is the simplest possible: compute NAV, compare to market, trade when the gap exceeds a threshold.

```python
def basket_quote(basket_mid, leg_mids, weights, threshold=10):
    """
    basket_mid: current mid of GIFT_BASKET
    leg_mids: dict of leg -> mid
    weights: dict of leg -> weight (4, 6, 1)
    threshold: trade when |spread| > this
    Returns: list of orders
    """
    nav = sum(weights[leg] * leg_mids[leg] for leg in weights)
    spread = basket_mid - nav
    orders = []
    if spread > threshold:
        # basket is rich; sell basket, buy legs
        orders.append(Order("GIFT_BASKET", "sell", basket_mid - 1, 1))
        for leg, w in weights.items():
            orders.append(Order(leg, "buy", leg_mids[leg] + 1, w))
    elif spread < -threshold:
        # basket is cheap; buy basket, sell legs
        orders.append(Order("GIFT_BASKET", "buy", basket_mid + 1, 1))
        for leg, w in weights.items():
            orders.append(Order(leg, "sell", leg_mids[leg] - 1, w))
    return orders
```

### 2. Hard-coded weights

Timo hard-codes the weights `4, 6, 1`. The spec gives them; don't model them. But: also build a self-discovering version (OLS on past data) so you can detect spec changes between rounds.

### 3. Threshold tuning

`threshold=10` here is illustrative. Timo tunes this per round by looking at the historical spread distribution. Too tight → too many trades, lose to fees. Too wide → miss the easy PnL.

## How this maps to our modules

- **Module 06** (ETF / basket arb): the entire module.

## What we did NOT extract

- The actual data on which the threshold was tuned. The team should write their own threshold selector (rolling median + MAD).
- Cross-product inventory netting. (When you sell basket + buy legs, you have a complex net position. Manage it.)

## Source lines

- `TimoDiehm/imc-prosperity-3/round_3_strategy.py`

## Open questions for the team

- What if a leg is illiquid? The basket is liquid; one leg is not. The leg-side trade is the bottleneck.
- What's the round-trip cost? 2 trades (basket + legs), so fees on both sides. The threshold must exceed 2× fee.
- What if NAV drifts? (If the constituents are themselves mean-reverting, NAV is too. The trade is "trade the spread of the spread.")
