# Weekly Plan Rationale

Why 16 weeks? Why this ordering? Why the splits?

## Total length: 16 weeks core + 4 advanced

The user specified 12-16 weeks core with the option to extend to 16-20 weeks advanced. We chose:

- **16 weeks core** — full coverage of all 20 modules at sustainable pace.
- **4 weeks advanced** (17-20) — stochastic control, queue priority, latency. The team's call whether to do these.

## Why not 8 weeks?

Tempting to compress, but each module is genuinely new to a beginner team. 1 week per module (heavy weeks like options get 1.5) is the fastest pace that doesn't sacrifice retention.

## Why not 24 weeks?

After 16 weeks, returns diminish. The team should be in mock-competition mode by then, not still reading chapters.

## Module ordering — pedagogical vs. competitive

We order modules by **pedagogical dependency**, not by when they appear in a typical Prosperity round.

| Order | Module | Why this slot |
|---|---|---|
| 1 | 00 + 15 (glossary + Python) | Foundation. Can't do anything without vocabulary and tools. |
| 2 | 02 (microstructure) | The vocabulary of order books, before any strategy. |
| 3-4 | 03 (market making) | The simplest strategy archetype, on top of microstructure. Replicate Wall-Mid on past data — first "win". |
| 5-6 | 04, 05 (mean reversion, cointegration) | The next archetype up. Builds on the order book understanding. |
| 7-8 | 06 (basket arb) | The first "structural" edge. Pairs reversion + cross-sectional intuition. Review week at 8. |
| 9 | 07 (options + Greeks) | The hardest standard archetype. After basket, before cross-exchange. |
| 10 | 08 (cross-exchange arb) | Builds on the factor-model idea from baskets. |
| 11 | 12 + 10 (ML + GARCH) | Split: one person on ML pipeline, one on vol model. Both feed into later modules. |
| 12 | 13 + 14 (bots + risk) | Game theory + position sizing. The defensive layer. |
| 13 | 16 (grid jumps) | The P4 R5 alpha. Specialized but high-leverage. |
| 14 | 11 (Bayesian) | Now that you have signals, learn to estimate them with uncertainty. |
| 15 | 19 (manual rounds) | 25% of score; collect past puzzles, solve 5. |
| 16 | 20 (mock competition) | End-to-end dry run. PnL decomposition. |
| 17-20 | 17, 18 (advanced) | Optional. Stochastic control, queue priority. Only after core is solid. |

The week-8 review is non-negotiable. Without it, week 9's options module collides with weak foundations in weeks 3-7.

## Why not order by Prosperity round sequence?

Because the team's prior P4 attempt dropped out at Round 3. They didn't experience Rounds 4-5. So we can't just say "do round 1 first" — they already did that, and the curriculum is partly to fix what they missed.

We order by **learning dependency**, not by round sequence.

## The 2-person split

Most weeks are parallel (both of you read the same thing, pair-program). Four weeks are explicitly split:

- **Week 6** (cointegration): Person A reads Engle-Granger; Person B reads Johansen. Reconcile Thursday.
- **Week 9** (options): Person A owns BS derivation + delta hedging; Person B owns IV smile + vol surface.
- **Week 11** (ML + vol): Person A owns AFML Ch 1-7 (XGBoost pipeline); Person B owns GARCH/EGARCH.
- **Week 16** (mock): split products. Each writes their trader's strategy solo, then merge.

The split assumes both people have read explain.html and source.html together. Only the extract is split. This avoids the failure mode where one person falls behind because they "didn't do the reading."

## Rest days

- Week 8: full review, no new content.
- Friday of every week: no new content. Catch-up + retro.
- Total hours per week: ~12-15 each.

## When the team is ahead

If the team finishes a week early, jump to the next week's extract.html. Don't skip the exercises — those are the muscle memory.

## When the team is behind

If the team is more than 3 days behind on a week, drop the exercises to 2 of 5 and keep the explain/source/extract intact. Exercises are replaceable; intuition is not.

## When Prosperity drops early

Stop the curriculum. Move to `code/`. Plug the visualizer/backtester. Use `resources/01_past_winners/` and `resources/04_mean_reversion/` etc. as your library of starting strategies.
