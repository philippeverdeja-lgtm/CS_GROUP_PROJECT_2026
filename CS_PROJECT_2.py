import streamlit as st
from yahooquery import Ticker

st.set_page_config(page_title="Stock Comparator", layout="wide")
st.title("Comparator of 2 stocks (CS_PROJECT_1)")

METRICS = [
    ("P/E Ratio",      "trailingPE"),
    ("EPS",            "trailingEps"),
    ("Profit Margin",  "profitMargins"),
    ("ROE",            "returnOnEquity"),
    ("Revenue Growth", "revenueGrowth"),
    ("Price/Book",     "priceToBook"),
    ("EV/EBITDA",      "enterpriseToEbitda"),
    ("EBITDA",         "ebitda"),
]

PERCENT_METRICS = {"Profit Margin", "ROE", "Revenue Growth"}


@st.cache_data(ttl=600)
def get_info(symbol: str) -> dict:
    symbol = symbol.upper()
    t = Ticker(symbol)
    merged = {}

    for module, data in [
        ("financial_data", t.financial_data),
        ("key_stats",      t.key_stats),
        ("summary_detail", t.summary_detail),
        ("asset_profile",  t.asset_profile),
    ]:
        if isinstance(data, dict) and symbol in data and isinstance(data[symbol], dict):
            merged.update(data[symbol])

    # Grab company name from price module
    price = t.price
    if isinstance(price, dict) and symbol in price and isinstance(price[symbol], dict):
        merged["longName"] = price[symbol].get("longName", symbol)
    else:
        merged ["longName"] = symbol

    return merged


def format_value(label: str, value) -> str:
    if value is None or not isinstance(value, (int, float)):
        return "N/A"
    if label in PERCENT_METRICS:
        return f"{value:.2%}"
    if label == "EBITDA":
        if abs(value) >= 1e12:
            return f"${value / 1e12:.2f}T"
        if abs(value) >= 1e9:
            return f"${value / 1e9:.2f}B"
        if abs(value) >= 1e6:
            return f"${value / 1e6:.2f}M"
    return f"{value:.2f}"


def render_header(info: dict, symbol: str):
    st.subheader(info.get("longName", symbol.upper()))
    st.write(f"**Ticker:** {symbol.upper()}")


def render_metric(label: str, info: dict):
    raw = info.get(next(key for lbl, key in METRICS if lbl == label))
    st.metric(label, format_value(label, raw))


# interface

col1, col2 = st.columns(2)
with col1:
    ticker1 = st.text_input("First Ticker (e.g. AAPL)").strip()
with col2:
    ticker2 = st.text_input("Second Ticker (e.g. MSFT)").strip()

if ticker1 and ticker2:
    with st.spinner("Fetching data…"):
        info1 = get_info(ticker1)
        info2 = get_info(ticker2)

    if not info1.get("longName") or not info2.get("longName"):
        st.error("One or both tickers could not be found. Please check the symbols.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            render_header(info1, ticker1)
        with col2:
            render_header(info2, ticker2)

        st.divider()

        for label, key in METRICS:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label, format_value(label, info1.get(key)))
            with col2:
                st.metric(label, format_value(label, info2.get(key)))

elif ticker1 or ticker2:
    st.info("Please enter both tickers to compare.")