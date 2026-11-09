import os
import matplotlib.pyplot as plt
import pandas as pd
from features import drawdown, log_returns, rolling_vol, sma


def plot_hero(close: pd.Series, symbol: str, output_path: str) -> None:
    """Generate 3-panel hero figure (Price+SMA, Rolling Vol, Drawdown)."""
    rets = log_returns(close)
    vol = rolling_vol(rets)
    dd = drawdown(close)
    sma50 = sma(close, 50)

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Panel 1: Price + SMA
    axes[0].plot(close.index, close, label=f"{symbol} Close", color="#1f77b4")
    axes[0].plot(
        sma50.index,
        sma50,
        label="SMA 50",
        color="#ff7f0e",
        linestyle="--",
    )
    axes[0].set_title(f"{symbol}: Price, Volatility & Drawdown Analysis")
    axes[0].set_ylabel("Price (USD)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Panel 2: Rolling Volatility
    axes[1].plot(
        vol.index,
        vol,
        label="30d Rolling Vol (Ann.)",
        color="#9467bd",
    )
    axes[1].set_ylabel("Annualized Volatility")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Panel 3: Drawdown Underwater Plot
    axes[2].fill_between(
        dd.index,
        dd * 100,
        0,
        color="#d62728",
        alpha=0.4,
        label="Drawdown %",
    )
    axes[2].set_ylabel("Drawdown %")
    axes[2].set_xlabel("Date")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Hero plot saved successfully to {output_path}")


if __name__ == "__main__":
    filepath = "data/raw/BTC-USD.csv"
    try:
        df = pd.read_csv(filepath, parse_dates=True, index_col=0)
        plot_hero(df["Close"], "BTC-USD", "reports/hero.png")
    except FileNotFoundError:
        print(f"[Error] {filepath} not found! Run src/ingest.py first.")