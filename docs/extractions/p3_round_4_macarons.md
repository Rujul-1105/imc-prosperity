# Extraction: P3 Round 4 — MAGNIFICENT_MACARONS

**Source**: Timo Diehm's `round_4_strategy.py`.
**Round**: P3 R4. Products: MAGNIFICENT_MACARONS, traded on TWO archipelago exchanges.

## The setup

MAGNIFICENT_MACARONS trades on Island 1 and Island 2. The fair value of macarons depends on:

- **Sugar price** (public, given).
- **Critical Sunlight Index** (public, given).
- **Transport cost** between islands.
- **Import tariff** charged on cross-island trades.

The strategy: compute the fair value on each island, account for transport + tariff, and trade the spread.

## The famous heuristic

```python
def macaron_arb_price(external_bid, sugar_idx, transport=1.0, tariff=0.02):
    """
    external_bid: best bid on the OTHER island
    sugar_idx:    normalized sugar & sunlight signal
    Returns: int price to quote on OUR island
    """
    return int(external_bid + 0.5)
```

The `int(external_bid + 0.5)` is the "round-and-tick" trick: when you see a bid on the other island, you can beat it by one tick *after* rounding for transport/tariff. The exact coefficients (transport, tariff) are tuned per round; Timo hard-codes them as constants from the round spec.

## What we extracted

### 1. Cross-exchange factor model

Build a model of fair value. The simpler, the better — when the spec gives you transport and tariff as constants, use them as constants.

```python
def fair_value_macarons(sugar_idx, sunlight_idx, transport, tariff, our_island):
    base = 100 + 2 * sugar_idx + 0.5 * sunlight_idx
    if our_island == 1:
        return base
    else:
        return base - transport - tariff
```

### 2. Trade on deviation

When the market price on our island is more than X above fair value, sell. When more than X below, buy.

### 3. Account for round-trip cost

Cross-exchange trades incur transport + tariff on each round trip. The threshold must exceed 2× (transport + tariff) to be profitable.

## How this maps to our modules

- **Module 08** (Cross-exchange arb): the entire module.

## What we did NOT extract

- The exact factor model coefficients. Per-round, per-spec.
- The order routing. (Prosperity has a `place_order` API; check if it auto-routes or you have to specify the exchange.)
- The "what if both islands are mispriced" case. Rare but possible.

## Source lines

- `TimoDiehm/imc-prosperity-3/round_4_strategy.py`

## Open questions for the team

- Is the sugar/sunlight index given as a time series or a per-tick value? The granularity matters.
- What's the position limit on cross-exchange trades?
- Is the tariff a percentage or absolute? (P3 was a percentage.)
