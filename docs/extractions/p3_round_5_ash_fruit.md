# Extraction: P3 Round 5 — ASH / FRUIT options

**Source**: Timo Diehm's `round_5_strategy.py`.
**Round**: P3 R5. Products: ASH (underlying), ASH call/put options, FRUIT (underlying), FRUIT call/put options.

## The setup

Two mean-reverting underlyings (ASH, FRUIT) plus options on each. The options' "fair value" depends on Black-Scholes (assuming GBM) plus an IV smile fit to historical data. The trade:

1. Compute the IV smile from past option prices.
2. Price each option using BS + smile.
3. If market price diverges from theoretical, trade it.
4. Delta-hedge in the underlying.

## What we extracted

### 1. Quadratic IV smile in log-moneyness

Timo fits a quadratic in log-moneyness:

```python
def iv_smile(log_moneyness, a, b, c):
    """σ(K) = a + b · log(K/S) + c · log(K/S)²"""
    return a + b * log_moneyness + c * log_moneyness ** 2

IV_SMILE_COEFFS = {
    "ASH":   [0.27362531, 0.01007566, 0.14876677],
    # FRUIT coefficients to be re-fit per round
}
```

The coefficients are extracted from Timo's code (or, for FRUIT, re-fit from the round's option chain). They're round-specific; hard-code them after fitting.

### 2. Black-Scholes pricing

Use `py_vollib` (or similar) for the BS formula. Plug in the smile-adjusted vol.

```python
from py_vollib.black_scholes import black_scholes

def price_option(S, K, tau, r, sigma):
    return black_scholes('c', S, K, tau, r, sigma)
```

### 3. Delta-hedge in the underlying

```python
from py_vollib.greeks.analytical import delta

def hedge_delta(option_position, underlying_position, spot, strike, tau, vol):
    """Compute additional spot position to make total delta = 0."""
    d_opt = delta('c', spot, strike, tau, 0.0, vol) * option_position
    d_total = d_opt + underlying_position
    return -d_total
```

Timo hedges in the *underlying* (ASH or FRUIT), not in a futures contract. In Prosperity this matters because the underlying trades actively.

### 4. Position limits per option series

Each option has a position limit (e.g., 200 contracts). Timo respects these. So should we.

## How this maps to our modules

- **Module 07** (Options & Greeks): the entire module.

## What we did NOT extract

- The vega and theta management. Timo's repo has this; should extract.
- The smile re-fitting logic. (The team should write their own walk-forward fitter.)
- The trade when the IV smile is itself mispriced. (Smile arbitrage — rare but profitable.)

## Source lines

- `TimoDiehm/imc-prosperity-3/round_5_strategy.py`

## Open questions for the team

- What's the IV smile stability across the round? (If it shifts, you have to re-fit hourly.)
- What's the bid-ask on the options? (Sometimes 1 tick, sometimes 5. The "edge" is the IV smile mispricing minus the bid-ask.)
- Are the options European or American? (P3 ASH was European. P4 may have changed.)
