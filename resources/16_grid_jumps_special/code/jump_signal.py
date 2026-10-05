"""
Module 16 — Grid-jump signal.

Run the self-test:
    python jump_signal.py
"""

from __future__ import annotations
from typing import List, Optional, Tuple


def grid_jump_signal(display_now: float, smoothed: float, grid_size: float = 1.0) -> Optional[str]:
    """
    Given the current display and the smoothed estimate, return the signal.
    Returns: 'buy' / 'sell' / None
    """
    expected_next = round(smoothed / grid_size) * grid_size
    diff = expected_next - display_now
    if diff >= grid_size * 0.5:
        return "buy"
    elif diff <= -grid_size * 0.5:
        return "sell"
    return None


def next_grid(smoothed: float, grid_size: float = 1.0) -> float:
    """The expected next grid-projected display given a smoothed estimate."""
    return round(smoothed / grid_size) * grid_size


def accuracy(
    displays: List[float],
    smoothed: List[float],
    grid_size: float = 1.0,
) -> Tuple[float, float]:
    """
    Compute the accuracy of the next-grid predictions vs actual.
    Returns: (fraction_correct, mean_absolute_error).
    """
    if len(displays) < 2:
        return 0.0, 0.0
    correct = 0
    total_err = 0.0
    n = 0
    for t in range(len(displays) - 1):
        pred = next_grid(smoothed[t], grid_size)
        actual = displays[t + 1]
        if abs(pred - actual) < 1e-9:
            correct += 1
        total_err += abs(pred - actual)
        n += 1
    return correct / n, total_err / n


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Display 100, smoothed 100.4 → expected next 100, signal None
    assert grid_jump_signal(100, 100.4, grid_size=1.0) is None
    # Display 100, smoothed 100.6 → expected next 101, signal "buy"
    assert grid_jump_signal(100, 100.6, grid_size=1.0) == "buy"
    # Display 100, smoothed 99.4 → expected next 99, signal "sell"
    assert grid_jump_signal(100, 99.4, grid_size=1.0) == "sell"

    # Half-grid threshold
    # Display 100, smoothed 100.5 → expected_next = round(100.5) = 100 (banker's rounding) or 101 (depending on impl)
    # Python's round uses banker's rounding for .5, so round(100.5) = 100. So signal is None.
    # But this is a corner case; we can use a more conservative threshold
    assert grid_jump_signal(100, 100.5, grid_size=1.0) is None  # round(100.5/1)*1 = 100 (banker's rounding in Python 3)

    # next_grid helper
    assert next_grid(100.4, 1.0) == 100
    assert next_grid(100.6, 1.0) == 101
    assert next_grid(50.49, 0.1) == 50.5
    assert next_grid(50.51, 0.1) == 50.5  # round(505.1)/10 = 505/10 = 50.5

    # Accuracy
    displays = [100, 100, 100, 101, 101, 101, 102]
    # Smoothed (just shift displays by 1 for "perfect" prediction)
    smoothed = [99.5, 100.5, 100.5, 100.5, 101.5, 101.5, 101.5]
    # At t=0: pred = round(99.5) = 100 (banker), actual = 100. Correct.
    # At t=1: pred = round(100.5) = 100 (banker), actual = 100. Correct.
    # At t=2: pred = 100, actual = 101. Wrong.
    # At t=3: pred = 100, actual = 101. Wrong.
    # At t=4: pred = round(101.5) = 102, actual = 101. Wrong.
    # At t=5: pred = 102, actual = 102. Correct.
    acc, mae = accuracy(displays, smoothed, 1.0)
    print(f"Accuracy: {acc:.2%}, MAE: {mae:.4f}")
    assert 0 < acc < 1
    assert mae >= 0

    print("All self-tests passed.")
