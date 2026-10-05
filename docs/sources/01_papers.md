# Papers — Canonical Sources

Every paper the curriculum draws from.

---

## Avellaneda & Stoikov (2008) — High-frequency trading in a limit order book

- **Link**: arXiv:1708.04928 (repost of original 2008 paper).
- **Why**: The market-making paper. Defines the framework every subsequent paper uses.
- **Used in**: Module 03 (Market making).
- **Read**: §2.1-2.3. Focus on equations (3) and (5) — reservation price and optimal spread.
- **Code**: `astraflow/avellaneda-stoikov` (GitHub) — C++ + Python reference implementation.
- **Extraction notes**: see `extractions/avellaneda_stoikov_paper.md`.

## Engle & Granger (1987) — Co-integration and error correction

- **Link**: Econometrica 55(2), 251-276. Search "Engle Granger 1987 co-integration" if no direct link.
- **Why**: The cointegration paper. Defines the augmented Dickey-Fuller test and the two-step procedure.
- **Used in**: Module 05 (Cointegration).

## Johansen (1988) — Statistical analysis of cointegration vectors

- **Link**: Journal of Economic Dynamics and Control 12, 231-254. Search for the paper.
- **Why**: The likelihood-based alternative to Engle-Granger. More powerful for multiple cointegrating vectors.
- **Used in**: Module 05 (Cointegration).

## BIS Working Paper — Anatomy of ETF Arbitrage

- **Link**: bis.org → search "ETF arbitrage" or "ETFs" → "Anatomy of ETF Arbitrage" (working paper, ~2021).
- **Why**: The cleanest description of how ETF/basket arbitrage actually works. Modern. Pro-trade.
- **Used in**: Module 06 (ETF/basket arb).

## Bouchaud, Bonart, Donier, Gould — Trades, Quotes and Prices (2018)

- **Link**: Cambridge University Press. Free PDF on the authors' pages.
- **Why**: Modern market microstructure with explicit math. Better than Harris for stochastic models.
- **Used in**: Module 17 (Advanced microstructure).

## Cartea, Jaimungal, Penã — various papers on stochastic control for trading

- **Links**: searchable on arXiv.
- **Why**: The mathematical underpinnings of optimal market-making under risk aversion.
- **Used in**: Module 18 (Stochastic control).

## Cont, Rama — Empirical properties of asset returns (2001)

- **Link**: Quantitative Finance 1, 223-236.
- **Why**: Stylized facts of returns: heavy tails, vol clustering, no autocorrelation in returns. The motivation for GARCH.
- **Used in**: Module 10 (Volatility).

## Glosten & Milgrom (1985) — Bid, ask and transaction prices in a specialist market

- **Link**: Journal of Financial Economics 13, 71-100.
- **Why**: The adverse-selection model for market-makers. The math behind "widen your spread when there's more information asymmetry."
- **Used in**: Module 17 (Advanced microstructure).

## Kyle (1985) — Continuous auctions and insider trading

- **Link**: Econometrica 53(6), 1315-1336.
- **Why**: The model of how informed traders move prices. The math of "how much can a market-maker learn from flow?"
- **Used in**: Module 13 (Game theory / bots).

## Almgren & Chriss (2001) — Optimal execution of portfolio transactions

- **Link**: Journal of Risk 3, 5-40.
- **Why**: Optimal execution with impact cost. Used in module 14 (risk/sizing).
- **Used in**: Module 14 (Risk & sizing).

---

## How to read these

The team should not read every paper cover-to-cover. The pattern is:

1. Read the abstract.
2. Read the introduction.
3. Skip to the model section.
4. Read the propositions.
5. Re-derive the result in your own notation (this is what goes in `extract.html`).
6. Implement and backtest.

For each paper, write a 1-page extraction in `extractions/`. Do not re-read the paper twice.
