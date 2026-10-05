# Prior Prosperity 4 Work — Summary

**Source**: `/home/rujul/projects/a/prosperity-4/` (sibling folder).
**Cycle**: Prosperity 4.
**Result**: ~rank 1000 globally in Rounds 1-2, then dropped out.

## What they had

### Infrastructure

- Python venv at `prosperity-4/venv/`.
- Docker-based backtester. `run.sh` wraps `docker run rust-backtester` with the right paths.
- Rust backtester image at `/home/rujul/projects/testing/prosperity_rust_backtester/`.
- Submission packaging (zips per round) in `submissions/`.

### Data

P3/P4 round CSVs in `data_capsule/`:

```
data_capsule/
├── ROUND_1/  (prices_*.csv, trades_*.csv, days -2, -1, 0)
├── ROUND_2/  (days -1, 0, 1)
└── ROUND_3/  (days 0, 1, 2)
```

(Each CSV has columns for timestamp, product, bid/ask prices+volumes at multiple levels, plus trade data.)

### Code

- `round_1/`: 7 Python files. `datamodel.py`, `trader.py`, plus iterations `r1v3.py`, `r1v5.py`, `r1v6.py`, `v1_pepper.py`, `v5_final_pepper_roots.py`, `final_submission_r1.py`.
- `round_2/`: 3 files. `datamodel.py`, `266993.py`, `combined_for_r2.py`.
- `round_3/`: `datamodel.py`, `trader.py`, `trader_ojas_5.py`, plus a `logs/` folder.
- `manual_rounds/`: `r1_c1.js` and `r1_c2.js` (JavaScript? unusual — perhaps a different teammate or a manual calculation tool).
- `algo_rounds/`: `r1/{10k_ticks, final}/` (output dirs from the backtester), `plots/{r1, r2, r3}/` (charts).

## What worked

### Round 1 (RAINFOREST_RESIN / KELP / SQUID_INK)

The "pepper roots" strategy. Multiple iterations suggest they explored hard. The final version is `final_submission_r1.py`. Probable pattern: market making with inventory skew, similar to Wall-Mid. Reached rank ~1000 globally.

### Round 3 (HYDROGEL_PACK)

`round_3/trader.py` trades HYDROGEL_PACK with:
- EMA + z-score mean-reversion.
- Book imbalance signal.
- Microprice as fair value.
- Trend filter.
- Inventory hard-cap at 140.
- Edge-based timing.

This is solid. It got them through Round 3.

## What failed / was missing

- They did not solve basket arb cleanly. (P3 R3 GIFT_BASKET-style rounds; P4 equivalents.)
- They did not capture the options round. (P3 R5 ASH/FRUIT; P4 R? equivalent.)
- They did not capture the cross-exchange arb round. (P3 R4 MACARONS; P4 ORCHIDS equivalent.)
- They did not attempt grid-jump alpha. (P4 R5.)
- They dropped out after Round 3. Likely time pressure + running out of ideas.

## What this means for the curriculum

The team's strengths from P4:
- Order book mechanics (read/write).
- Basic market making (Wall-Mid or equivalent).
- Mean reversion (z-score, EMA).
- Microprice.
- Inventory caps.
- Edge-based timing.

The team's gaps from P4:
- Basket arb (the largest gap; P3's #1 differentiator).
- Options (the second-largest gap; P3's #5 differentiator).
- Cross-exchange arb.
- Game-theoretic / bot-fingerprinting play.
- Grid-jump alpha.

The curriculum is calibrated to:
- Skip the basics (week 1 covers vocabulary; week 2-3 assume they know microstructure).
- Spend weeks 6-10 on the missing pieces (cointegration, basket, options, cross-exchange).
- Spend week 13 on grid jumps (the highest-leverage single edge).
- Use weeks 17-20 only if needed (advanced microstructure, stochastic control).

## Specific code worth revisiting

The Round 3 `trader.py` is a useful starting point. It has:
- `OrderBook` parsing logic.
- EMA + z-score computation.
- Microprice calculation.
- Inventory cap logic.

We can lift these into the team's `code/` for module 02 (microstructure) and 04 (mean reversion). The team shouldn't re-derive what's already working.

## Notes on naming

- `pepper roots` (P4 R1) → unclear what the actual product was; the team named their strategy file that way.
- `266993.py` (P4 R2) → file named after an ID, probably the team's internal tracking.
- `trader_ojas_5.py` (P4 R3) → suggests a teammate "Ojas" was on the team. Possibly joining P5.

## Cleanup recommendations

Before P5:
- Archive the P4 folder: `mv prosperity-4 prosperity-4-archive-2025-XX-XX`.
- Don't delete; the data is useful for exercises.
- Lift the working code into the new `code/` (during the comp, not now).

## Source

- `/home/rujul/projects/a/prosperity-4/` — the full folder, ~50 MB.
- `Readme.md` — 2 lines (docker build/run instructions).
- The team's per-round code as listed above.
