import yfinance as yf
import streamlit as st

st.set_page_config(page_title="Stock Comparator", layout="centered")
st.title("Comparator of 2 stocks (CS_PROJECT_1)")

col1, col2 = st.columns(2)
with col1:
    ticker1 = st.text_input("First Ticker (e.g. AAPL)")
with col2:
    ticker2 = st.text_input("Second Ticker (e.g. MSFT)")

METRICS = [
    ("P/E Ratio",       "trailingPE"),
    ("Debt/Equity",     "debtToEquity"),
    ("ROE",             "returnOnEquity"),
    ("Free Cash Flow",  "freeCashflow"),
    ("Profit Margin",   "profitMargins"),
    ("EPS",             "trailingEps"),
    ("Revenue Growth",  "revenueGrowth"),
    ("Current Ratio",   "currentRatio"),
]

def get_info(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    return stock.info

def render_header(info, ticker_symbol):
    st.subheader(info.get("longName", ticker_symbol))
    st.write(f"**Ticker:** {ticker_symbol.upper()}")

def render_metric(label, value):
    st.metric(label, value if value is not None else "N/A")

if ticker1 and ticker2:
    info1 = get_info(ticker1)
    info2 = get_info(ticker2)

    col1, col2 = st.columns(2)
    with col1:
        render_header(info1, ticker1)
    with col2:
        render_header(info2, ticker2)

    st.divider()

    for label, key in METRICS:
        col1, col2 = st.columns(2)
        with col1:
            render_metric(label, info1.get(key))
        with col2:
            render_metric(label, info2.get(key))

elif ticker1 or ticker2:
    st.info("Please enter both tickers to compare.")