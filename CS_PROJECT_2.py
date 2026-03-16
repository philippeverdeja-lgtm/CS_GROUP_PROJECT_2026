import requests
import streamlit as st

st.set_page_config(page_title="Stock Comparator", layout="centered")
st.title("Comparator of 2 stocks (CS_PROJECT_1)")

METRICS = [
    ("P/E Ratio",      "PERatio"),
    ("EPS",            "EPS"),
    ("Profit Margin",  "ProfitMargin"),
    ("ROE",            "ReturnOnEquityTTM"),
    ("Revenue Growth", "QuarterlyRevenueGrowthYOY"),
    ("Debt/Equity",    "DebtToEquityRatio"),
    ("Current Ratio",  "CurrentRatio"),
    ("Free Cash Flow", "OperatingCashflowTTM"),
]

@st.cache_data(ttl=600)
def get_info(ticker_symbol):
    api_key = st.secrets["AV_API_KEY"]
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker_symbol}&apikey={api_key}"
    r = requests.get(url)
    return r.json()

def render_header(info, ticker_symbol):
    st.subheader(info.get("Name", ticker_symbol))
    st.write(f"**Ticker:** {ticker_symbol.upper()}")

def render_metric(label, value):
    st.metric(label, value if value not in (None, "None", "-") else "N/A")

col1, col2 = st.columns(2)
with col1:
    ticker1 = st.text_input("First Ticker (e.g. AAPL)")
with col2:
    ticker2 = st.text_input("Second Ticker (e.g. MSFT)")

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