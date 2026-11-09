import numpy as np
import pandas as pd
import pytest
import sys
import os

# src path add karo imports ke liye
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from features import log_returns, drawdown, sma, rolling_vol


def test_log_returns_known_values():
    s = pd.Series([100.0, 110.0, 121.0])
    r = log_returns(s)
    expected = np.log(1.1)
    assert np.allclose(r.values, expected)


def test_drawdown_never_positive():
    s = pd.Series([100.0, 120.0, 90.0, 130.0])
    dd = drawdown(s)
    assert (dd <= 0).all()
    assert np.isclose(dd.iloc[2], (90 - 120) / 120)


def test_sma_calculation():
    s = pd.Series([10.0, 20.0, 30.0, 40.0])
    result = sma(s, window=2)
    assert result.iloc[1] == 15.0
    assert result.iloc[3] == 35.0