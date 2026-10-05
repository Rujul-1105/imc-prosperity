# Team Context

## The team

- **Size**: 2 people.
- **Background**: Beginner in finance/trading. Both learning from scratch.
- **Stakes**: This competition is their primary shot at breaking into quant. IMC uses Prosperity as a recruiting funnel. The team's prior round (Prosperity 4) reached approximately rank #1000 globally in Rounds 1–2 before dropping out of the competition.
- **Commitment**: Both fully dedicated. Treating this as full-time prep.

## Prior work

The team has prior work in a sibling folder: `/home/rujul/projects/a/prosperity-4/`.

What they did in P4 (per the README and code in that folder):
- Used Docker + a Rust backtester to run strategies.
- Round 1: explored a "pepper roots" strategy with multiple iterations (`v1`, `v3`, `v5`, `v6`).
- Round 2: combined `266993.py` with `combined_for_r2.py`.
- Round 3: traded `HYDROGEL_PACK` with EMA + z-score mean-reversion, book imbalance, microprice, trend filter, inventory hard-cap at 140, edge-based timing.
- Round 3 also had a `trader_ojas_5.py` (teammate named Ojas; possibly joining again this cycle).
- After Round 3 they dropped out.

What worked in P4:
- Round 1 RAINFOREST_RESIN-type market making (the "pepper roots" variants).
- Microprice + z-score mean reversion on a basket-like product.

What failed / was missing in P4:
- They never solved the basket arb edges (GIFT_BASKET, PEBBLE) cleanly.
- They didn't capture the options round (P3 R5 ASH/FRUIT; P4 equivalent).
- They didn't capture the cross-exchange arb round (P3 R4 MACARONS; P4 equivalent).
- They exited at Round 3, possibly due to time pressure, possibly due to running out of ideas.

The implication: the curriculum must build strength specifically in **structural edges** (basket, options, cross-exchange, grid jumps) that the team did not capture last cycle. The basics (market making, mean reversion) are partially in hand.

## What they have access to

- Python venv (still in `prosperity-4/venv/`).
- Past P3/P4 round CSVs in `prosperity-4/data_capsule/ROUND_{1,2,3}/`.
- Rust backtester at `/home/rujul/projects/testing/prosperity_rust_backtester/`.
- A separate `portfolio/` project elsewhere — out of scope.
- A separate `crypto-exchange/` project — out of scope.

## What we are building

For Prosperity 5 (and beyond):

- **`resources/`** — a 16-week finance curriculum in HTML. Self-study material organized by module.
- **`docs/`** — this folder. The research dossier behind `resources/`.
- **Visualizer/backtester** — to be built in a separate folder, on the team's schedule. They will tell us when to start.
- **`code/`** — created when Prosperity drops. Submissions live here.

## Target

**Global rank #1** is the stated goal. Realistic but hard. Top 10 is the floor. The curriculum is calibrated to enable #1: assume the team will master every archetype of round, plus the structural edges (basket, options, cross-exchange, grid jumps) that distinguish top-100 from top-10.
