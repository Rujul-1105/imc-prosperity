# Extraction: P3 Round 1 — RAINFOREST_RESIN, KELP, SQUID_INK

**Source**: Timo Diehm's `round_1_strategy.py` (https://github.com/TimoDiehm/imc-prosperity-3).
**Round**: P3 R1. ~1k teams. Products: RAINFOREST_RESIN (FFV), KELP (?), SQUID_INK (?).

## What we extracted

### 1. The Wall-Mid strategy

Timo's signature. Place bid at the level just inside the largest visible bid wall, ask at the level just outside the largest ask wall. The intuition: walls reveal other participants' intent, and being 1 tick inside means you fill before they do.

```python
def wall_mid_quotes(book, our_position, max_pos=20):
    bids = sorted(book['bids'], key=lambda x: -x[1])  # largest first
    asks = sorted(book['asks'], key=lambda x: -x[1])
    if not bids or not asks:
        return None, None

    bid_wall_price, _ = bids[0]
    ask_wall_price, _ = asks[0]

    # inventory skew
    skew = our_position // 5
    bid = bid_wall_price + 1 - skew
    ask = ask_wall_price - 1 - skew

    # hard cap
    if our_position >= max_pos:
        bid = None
    elif our_position <= -max_pos:
        ask = None
    return bid, ask
```

### 2. Inventory hard-cap

Every market-making strategy in Timo's code has a hard inventory cap. The `max_pos=20` here is a parameter, but the structure — "if you hit the cap, stop quoting on that side" — is universal.

### 3. Skew per 5 units of inventory

`skew = our_position // 5` — one tick of skew per 5 units of inventory. Linear. Simple. Timo's choice; we can tune, but starting from this is fine.

## What we did NOT extract (because it's a Timo-specific choice)

- The exact values of `max_pos` (round-specific; check the spec).
- The exact `skew` divisor (5 here; could be 3, 10, etc.).
- The hard cap direction logic (which side to halt when long vs short).

These should be parametrized in the team's code, not hard-coded.

## How this maps to our modules

- **Module 02** (Microstructure): the order book parsing and wall detection.
- **Module 03** (Market making): the Wall-Mid quoting logic.

## Open questions for the team

- What was KELP's data process? (P3 R1 had it; Timo's strategy file handles it.)
- What was SQUID_INK's? (Noise / GBM archetype.)
- Are the wall signals different per product, or shared?

## Source lines

- `TimoDiehm/imc-prosperity-3/round_1_strategy.py` (line numbers vary; the Wall-Mid function is the load-bearing one).
- The full repo has unit tests and a small backtester; trace one tick through to understand the fill model.
