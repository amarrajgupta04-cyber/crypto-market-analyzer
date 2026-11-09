import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Add src folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from features import drawdown, log_returns, rolling_vol, sma, summary_stats
from ingest import fetch_ohlcv, save_raw
from quality import check_quality

# Page Configuration
st.set_page_config(
    page_title="Crypto Market Data Analyzer",
    page_icon="📈",
    layout="wide",
)

st.title("🚀 Crypto Market Data Analyzer Dashboard")
st.markdown(
    "Quantitative Data Pipeline & Risk Analytics Interface for Crypto Assets."
)

# Sidebar Options
st.sidebar.header("Pipeline Controls")
symbol = st.sidebar.selectbox(
    "Select Crypto Symbol", ["BTC-USD", "ETH-USD", "SOL-USD"]
)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-12-31"))

if st.sidebar.button("Run Analysis", type="primary"):
    with st.spinner("Fetching data and building pipeline..."):
        # 1. Ingestion
        df = fetch_ohlcv(symbol, start=str(start_date), end=str(end_date))
        save_raw(df, f"data/raw/{symbol}.csv")

        # 2. Quality Report Metrics
        st.subheader("🛡️ Data Quality Audit")
        q_report = check_quality(df)
        cols = st.columns(len(q_report))
        for i, (k, v) in enumerate(q_report.items()):
            cols[i].metric(
                label=k.replace("_", " ").title(),
                value=v,
                delta="Clean" if v == 0 else "Issue Detected",
                delta_color="normal" if v == 0 else "inverse",
            )

        # 3. Key Metrics
        close = df["Close"]
        rets = log_returns(close)
        stats = summary_stats(rets)
        dd = drawdown(close)

        st.subheader("📊 Risk & Quantitative Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ann. Volatility", f"{stats['annualized_volatility']:.2%}")
        m2.metric("Max Drawdown", f"{dd.min():.2%}")
        m3.metric("Skewness", f"{stats['skewness']:.2f}")
        m4.metric("Kurtosis", f"{stats['kurtosis']:.2f}")

        # 4. Multi-panel Visualization
        st.subheader("📈 Market Performance & Underwater Plot")
        fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
        sma50 = sma(close, 50)
        vol = rolling_vol(rets)

        axes[0].plot(close.index, close, label=f"{symbol} Close", color="#1f77b4")
        axes[0].plot(
            sma50.index,
            sma50,
            label="SMA 50",
            color="#ff7f0e",
            linestyle="--",
        )
        axes[0].set_ylabel("Price (USD)")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(
            vol.index, vol, label="30d Rolling Vol (Ann.)", color="#9467bd"
        )
        axes[1].set_ylabel("Volatility")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        axes[2].fill_between(
            dd.index, dd * 100, 0, color="#d62728", alpha=0.4, label="Drawdown %"
        )
        axes[2].set_ylabel("Drawdown %")
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        st.pyplot(fig)

        # Raw Data Table
        with st.expander("🔍 View Raw Downloaded Data"):
            st.dataframe(df.tail(100))
else:
    st.info("Sidebar me options select karke **'Run Analysis'** button dabao!")