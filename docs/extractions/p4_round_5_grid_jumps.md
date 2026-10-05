# Extraction: P4 R5 Grid-Jump Alpha

**Source**: Leo Hawking's P4 retrospective (https://github.com/Leo-Hawking/IMC-Prosperity-4-Review).
**Significance**: The most-missed edge in P4. Moved 96th to top 15 if exploited.

## What is the grid-jump alpha?

A geometric Brownian motion `dS = σ S dW` projected onto a coarse price grid produces discrete jumps. The jumps are predictable from the true (smoothed) price.

In a P4 R5-style round:

- The true price is GBM with vol σ.
- The exchange rounds prices to a grid (e.g., 1.0 increments).
- The "next tick" price is `round(true_price / grid_size) × grid_size`.
- When true_price moves by more than grid_size between ticks, the displayed price jumps by grid_size.

## The trade

Estimate true_price with a Kalman filter or simple EMA. Compute `expected_next_price = round(true_price / grid_size) × grid_size`. If the current market price is 1 tick below `expected_next_price`, the price will jump up next tick. Buy now.

## Pseudo-code

```python
def grid_jump_signal(prices, grid_size=1.0, alpha=0.1):
    """
    prices: list of past mid prices (most recent last)
    grid_size: the rounding grid
    alpha: EMA smoothing factor
    Returns: expected next grid price, current price
    """
    # Smoothed estimate of true price
    smoothed = prices[0]
    for p in prices[1:]:
        smoothed = alpha * p + (1 - alpha) * smoothed

    # Next grid price
    next_grid = round(smoothed / grid_size) * grid_size
    return next_grid, prices[-1]

def grid_jump_trade(current_price, expected_next, grid_size=1.0, threshold=0.5):
    """
    If current is 1 tick below expected next, buy.
    If current is 1 tick above expected next, sell.
    """
    diff = expected_next - current_price
    if diff >= grid_size * threshold:
        return "buy"
    elif diff <= -grid_size * threshold:
        return "sell"
    else:
        return None
```

## Why this works

The grid projection creates a "sticky" price. When the true price drifts to a new grid level, the displayed price stays put for a few ticks, then jumps. The jump direction is predictable from the smoothed estimate.

## When this works

- The product is genuinely GBM-projected-onto-grid.
- The grid size is large enough that the smoothed estimate is reliable (a tiny grid is just continuous GBM, no alpha).
- The team is small enough that their trade doesn't itself move the price (Prosperity is small; the grid is round-level constant, so this is true).

## When this doesn't work

- The product isn't GBM (mean-reverting, FFV, basket — different story).
- The grid is too small.
- The order arrival rate is high (real market would adjust before the jump).

## How this maps to our modules

- **Module 16** (Grid jumps): the entire module.

## Source

- `Leo-Hawking/IMC-Prosperity-4-Review`
- No canonical paper; the "alpha" is implicit in the round spec.
