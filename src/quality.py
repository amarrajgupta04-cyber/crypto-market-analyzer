import pandas as pd


def check_quality(df: pd.DataFrame) -> dict:
    """
    Perform data quality and integrity checks on market data DataFrame.
    Returns a dictionary report.
    """
    report = {}

    # 1. Duplicate timestamps check
    report["duplicate_timestamps"] = int(df.index.duplicated().sum())

    # 2. Chronological order check
    report["not_sorted"] = not df.index.is_monotonic_increasing

    # 3. Negative or zero close prices check
    if "Close" in df.columns:
        report["non_positive_prices"] = int((df["Close"] <= 0).sum())

    # 4. Missing calendar days check
    if len(df) > 0:
        full_range = pd.date_range(df.index.min(), df.index.max(), freq="D")
        report["missing_days"] = int(len(full_range.difference(df.index)))
    else:
        report["missing_days"] = 0

    # 5. Single-day large price jump check (>30%)
    if "Close" in df.columns and len(df) > 1:
        pct_change = df["Close"].pct_change().abs()
        report["suspicious_jumps"] = int((pct_change > 0.30).sum())

    return report


if __name__ == "__main__":
    for symbol in ["BTC-USD", "ETH-USD"]:
        filepath = f"data/raw/{symbol}.csv"
        try:
            df = pd.read_csv(filepath, parse_dates=True, index_col=0)
            q_report = check_quality(df)
            print(f"\n--- Data Quality Report for {symbol} ---")
            for key, val in q_report.items():
                print(f"  {key}: {val}")
        except FileNotFoundError:
            print(f"[Error] File not found: {filepath}")