# Extraction: jmerle's Hybrid Framework

**Source**: https://github.com/jmerle/imc-prosperity-3
**Result**: 25th in P3.
**Why we extracted**: The cleanest abstraction layer in any open-source P3 repo. The team should mirror this design.

## The architecture

```
Strategy (abstract)
├── StatefulStrategy
│   ├── SignalStrategy (mean-reversion style)
│   └── MarketMakingStrategy (spread-capture style)
├── DeanonymizedTradesStrategy (bot-fingerprinting)
└── ... (other custom strategies)
```

Each strategy is a class with:
- `__init__(self, trader)`: state.
- `generate_orders(self, state, trader) -> list[Order]`: the decision.

The `Trader` (top-level) holds a list of strategies and aggregates their orders. Each strategy sees the full `TradingState` and can read the others' state.

## Key file: `prosperity/hybrid.py`

```python
class Strategy(ABC):
    @abstractmethod
    def generate_orders(self, state: TradingState) -> Dict[Symbol, List[Order]]:
        pass

class StatefulStrategy(Strategy):
    """A strategy that maintains state across ticks."""
    def __init__(self):
        self.state = {}

    def generate_orders(self, state: TradingState) -> Dict[Symbol, List[Order]]:
        # ... default: delegate to subclass
        pass

class SignalStrategy(StatefulStrategy):
    """A strategy that emits a signal (e.g., z-score), then trades on it."""
    def __init__(self, signal_fn, sizing_fn):
        super().__init__()
        self.signal_fn = signal_fn
        self.sizing_fn = sizing_fn

    def generate_orders(self, state: TradingState) -> Dict[Symbol, List[Order]]:
        signal = self.signal_fn(state)
        size = self.sizing_fn(signal, state)
        return {symbol: [Order(symbol, side, price, size)] for symbol, side, price in size}
```

## Key file: `prosperity/strategies/rolling_zscore.py`

The rolling z-score strategy:

```python
class RollingZScoreStrategy(SignalStrategy):
    def __init__(self, symbol, lookback=50, threshold=1.5):
        def signal_fn(state):
            prices = state.price_history[symbol][-lookback:]
            if len(prices) < lookback:
                return 0
            mean = sum(prices) / len(prices)
            std = (sum((p - mean)**2 for p in prices) / len(prices)) ** 0.5
            return (prices[-1] - mean) / std if std > 0 else 0
        def sizing_fn(signal, state):
            if signal > threshold:
                return [(symbol, "sell", state.mid(symbol), 1)]
            elif signal < -threshold:
                return [(symbol, "buy", state.mid(symbol), 1)]
            return []
        super().__init__(signal_fn, sizing_fn)
```

## What we extracted

### 1. The Strategy → StatefulStrategy → SignalStrategy / MarketMakingStrategy abstraction

This is the design pattern the team should use for their own code. Each new strategy inherits from one of the four bases. Each base handles a category of state (none / per-strategy / signal-based / market-making).

### 2. Signal vs Sizing separation

`SignalStrategy` separates the "what's my edge?" function from the "how much do I trade?" function. This is good. It lets you swap sizings without rewriting the signal.

### 3. DeanonymizedTradesStrategy

jmerle's approach to bot-fingerprinting. The idea: each named bot (Olivia, etc.) trades a recognizable pattern. Once you identify the pattern, mirror their trades or fade their anti-pattern.

```python
class DeanonymizedTradesStrategy(Strategy):
    def __init__(self, bot_name, side_to_take, fade=True):
        self.bot_name = bot_name
        self.side_to_take = side_to_take
        self.fade = fade

    def generate_orders(self, state):
        # Find recent trades by the bot
        bot_trades = [t for t in state.market_trades if t.buyer == self.bot_name or t.seller == self.bot_name]
        # If fade: trade opposite. If mirror: trade same.
        ...
```

## How this maps to our modules

- **Module 02** (Microstructure): the TradingState / datamodel structures.
- **Module 03** (Market making): MarketMakingStrategy.
- **Module 04** (Mean reversion): RollingZScoreStrategy.
- **Module 13** (Bots): DeanonymizedTradesStrategy.
- The team's visualizer/backtester should mirror the hybrid.py abstraction.

## What we did NOT extract

- The full `prosperity3bt` backtester. (Useful but heavy; the team should build their own.)
- The `prosperity-visualizer` UI. (Useful but the team has their own visualizer planned.)
- The submission tooling.

## Source

- `jmerle/imc-prosperity-3/prosperity/hybrid.py`
- `jmerle/imc-prosperity-3/prosperity/strategies/`
- The `prosperity3bt` PyPI package for backtesting locally.
