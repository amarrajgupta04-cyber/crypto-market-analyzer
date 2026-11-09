import numpy as np
import pandas as pd


def log_returns(close: pd.Series) -> pd.Series:
    """Compute daily log returns: ln(P_t / P_{t-1})."""
    return np.log(close / close.shift(1)).dropna()


def sma(close: pd.Series, window: int) -> pd.Series:
    """Compute Simple Moving Average."""
    return close.rolling(window=window).mean()


def ema(close: pd.Series, span: int) -> pd.Series:
    """Compute Exponential Moving Average."""
    return close.ewm(span=span, adjust=False).mean()


def rolling_vol(
    returns: pd.Series, window: int = 30, periods_per_year: int = 365
) -> pd.Series:
    """Compute 30-day rolling annualized volatility."""
    return returns.rolling(window=window).std() * np.sqrt(periods_per_year)


def drawdown(close: pd.Series) -> pd.Series:
    """Compute percentage drawdown from peak."""
    peak = close.cummax()
    return (close - peak) / peak


def summary_stats(returns: pd.Series) -> pd.Series:
    """Compute key statistical properties of log returns."""
    return pd.Series(
        {
            "mean_daily_return": returns.mean(),
            "std_daily_return": returns.std(),
            "annualized_volatility": returns.std() * np.sqrt(365),
            "skewness": returns.skew(),
            "kurtosis": returns.kurtosis(),
            "min_return": returns.min(),
            "max_return": returns.max(),
        }
    )


if __name__ == "__main__":
    filepath = "data/raw/BTC-USD.csv"
    try:
        df = pd.read_csv(filepath, parse_dates=True, index_col=0)
        close = df["Close"]

        rets = log_returns(close)
        vol = rolling_vol(rets)
        dd = drawdown(close)
        stats = summary_stats(rets)

        print("\n--- BTC-USD Summary Statistics ---")
        print(stats)
        print(f"\nMax Drawdown: {dd.min():.2%}")
    except FileNotFoundError:
        print(f"[Error] {filepath} not found! Run src/ingest.py first.")