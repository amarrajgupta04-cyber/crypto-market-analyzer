import os
import pandas as pd
import yfinance as yf


def fetch_ohlcv(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily OHLCV data for a given crypto symbol using yfinance.
    """
    print(f"Fetching data for {symbol} from {start} to {end}...")
    df = yf.download(symbol, start=start, end=end, progress=False)

    # MultiIndex columns handle karna
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df


def save_raw(df: pd.DataFrame, filepath: str) -> None:
    """
    Save DataFrame to CSV format inside data/raw directory.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath)
    print(f"Saved raw data to {filepath}")


if __name__ == "__main__":
    # Fetch daily OHLCV data for BTC and ETH from 2021 to 2024
    btc_df = fetch_ohlcv("BTC-USD", start="2021-01-01", end="2024-12-31")
    save_raw(btc_df, "data/raw/BTC-USD.csv")

    eth_df = fetch_ohlcv("ETH-USD", start="2021-01-01", end="2024-12-31")
    save_raw(eth_df, "data/raw/ETH-USD.csv")