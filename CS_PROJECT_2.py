import requests
import streamlit as st

st.set_page_config(page_title="Stock Comparator", layout="centered")
st.title("Comparator of 2 stocks (CS_PROJECT_1)")

METRICS = [
    ("P/E Ratio",      "pe"),
    ("Debt/Equity",    "debtToEquity"),
    ("ROE",            "roe"),
    ("Free Cash Flow", "freeCashFlow"),
    ("Profit Margin",  "profitMargin"),
    ("EPS",            "eps"),
    ("Current Ratio",  "currentRatio"),
]

@st.cache_data(ttl=600)
def get_info(ticker_symbol):
    api_key = st.secrets["FMP_API_KEY"]
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker_symbol}?apikey={api_key}"
    r = requests.get(url)
    data = r.json()
    st.write (data)
    return data[0] if data else {}

def render_header(info, ticker_symbol):
    st.subheader(info.get("companyName", ticker_symbol))
    st.write(f"**Ticker:** {ticker_symbol.upper()}")

def render_metric(label, value):
    st.metric(label, value if value is not None else "N/A")

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