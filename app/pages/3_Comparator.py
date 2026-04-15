# Stock Comparator with Yahoo Finance search
import streamlit as st
import pandas as pd
import requests
from yahooquery import Ticker

st.set_page_config(page_title="Stock Comparator", page_icon="📊", layout="wide")
st.title("📊 Stock Comparator - CS_GROUP_PROJECT_2026")
st.markdown("Search for stocks by ticker or company name")

# ── Search Yahoo Finance ──────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def search_stocks(query):
    """Search Yahoo Finance for stocks matching query"""
    if not query or len(query) < 2:
        return []
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=8&newsCount=0&enableFuzzyQuery=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()  # FIX
        data = r.json()

        results = []
        for item in data.get("quotes", []):
            ticker   = item.get("symbol", "")
            name     = item.get("longname") or item.get("shortname") or ""
            exchange = item.get("exchDisp", "")
            typ      = item.get("quoteType", "")
            if ticker and typ in ("EQUITY", "ETF", "MUTUALFUND"):
                label = f"{ticker} — {name} ({exchange})"
                results.append({"label": label, "ticker": ticker, "name": name})
        return results
    except Exception:
        return []

# ── Fetch stock data from yahooquery ──────────────────────────────────────────
@st.cache_data(show_spinner=False, ttl=1000)
def get_stock_info(ticker):
    """Fetch comprehensive stock data from Yahoo Finance"""
    if not ticker:
        return {}
    
    try:
        ticker = ticker.upper()
        t = Ticker(ticker)

        # SAFE dictionary handling
        financial_data = t.financial_data.get(ticker, {}) if isinstance(t.financial_data, dict) else {}
        key_stats = t.key_stats.get(ticker, {}) if isinstance(t.key_stats, dict) else {}
        summary_detail = t.summary_detail.get(ticker, {}) if isinstance(t.summary_detail, dict) else {}

        # FIX price handling
        price_all = t.price
        if isinstance(price_all, dict):
            price_data = price_all.get(ticker, {})
        else:
            price_data = {}

        long_name = price_data.get("longName", ticker)

        # Combine all data
        stock_info = {**financial_data, **key_stats, **summary_detail}
        stock_info["longName"] = long_name
        stock_info["currentPrice"] = price_data.get("regularMarketPrice")

        return stock_info
    
    except Exception as e:
        st.error(f"Error fetching {ticker}: {e}")  # SHOW ERROR
        return {}

# ── Format values ─────────────────────────────────────────────────────────────
def format_value(value):
    """Format numeric values nicely"""
    if value is None:
        return "N/A"
    if isinstance(value, float):
        if abs(value) < 1:
            return f"{value:.4f}"
        elif abs(value) > 1000000000:
            return f"${value/1e9:.2f}B"
        elif abs(value) > 1000000:
            return f"${value/1e6:.2f}M"
        else:
            return f"{value:.2f}"
    return str(value)

# ── Session state ─────────────────────────────────────────────────────────────
if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = [None, None, None, None]

# ── Search and selection interface ────────────────────────────────────────────
st.markdown("### 🔍 Search and Select Stocks")
st.caption("Search by ticker (AAPL), company name (Apple), or ISIN. Select up to 4 stocks to compare.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("**Stock 1**")
    search1 = st.text_input("Search Stock 1", 
                            placeholder="e.g. AAPL, Apple, NESN.SW...",
                            key="search1")
    selected1 = None
    if search1:
        with st.spinner("Searching..."):
            results1 = search_stocks(search1)
        if results1:
            options1 = ["— select —"] + [r["label"] for r in results1]
            chosen1 = st.selectbox("", options1, key="select1", label_visibility="collapsed")
            if chosen1 != "— select —":
                match1 = next((r for r in results1 if r["label"] == chosen1), None)
                if match1:
                    selected1 = match1["ticker"]
                    st.session_state.selected_tickers[0] = selected1
        else:
            st.warning("No results found")
    else:
        selected1 = st.session_state.selected_tickers[0]
    
    if selected1:
        st.success(f"✅ {selected1}")

with col2:
    st.markdown("**Stock 2**")
    search2 = st.text_input("Search Stock 2",
                            placeholder="e.g. MSFT, Microsoft...",
                            key="search2")
    selected2 = None
    if search2:
        with st.spinner("Searching..."):
            results2 = search_stocks(search2)
        if results2:
            options2 = ["— select —"] + [r["label"] for r in results2]
            chosen2 = st.selectbox("", options2, key="select2", label_visibility="collapsed")
            if chosen2 != "— select —":
                match2 = next((r for r in results2 if r["label"] == chosen2), None)
                if match2:
                    selected2 = match2["ticker"]
                    st.session_state.selected_tickers[1] = selected2
        else:
            st.warning("No results found")
    else:
        selected2 = st.session_state.selected_tickers[1]
    
    if selected2:
        st.success(f"✅ {selected2}")

with col3:
    st.markdown("**Stock 3**")
    search3 = st.text_input("Search Stock 3",
                            placeholder="e.g. GOOG, Google...",
                            key="search3")
    selected3 = None
    if search3:
        with st.spinner("Searching..."):
            results3 = search_stocks(search3)
        if results3:
            options3 = ["— select —"] + [r["label"] for r in results3]
            chosen3 = st.selectbox("", options3, key="select3", label_visibility="collapsed")
            if chosen3 != "— select —":
                match3 = next((r for r in results3 if r["label"] == chosen3), None)
                if match3:
                    selected3 = match3["ticker"]
                    st.session_state.selected_tickers[2] = selected3
        else:
            st.warning("No results found")
    else:
        selected3 = st.session_state.selected_tickers[2]
    
    if selected3:
        st.success(f"✅ {selected3}")

with col4:
    st.markdown("**Stock 4**")
    search4 = st.text_input("Search Stock 4",
                            placeholder="e.g. AMZN, Amazon...",
                            key="search4")
    selected4 = None
    if search4:
        with st.spinner("Searching..."):
            results4 = search_stocks(search4)
        if results4:
            options4 = ["— select —"] + [r["label"] for r in results4]
            chosen4 = st.selectbox("", options4, key="select4", label_visibility="collapsed")
            if chosen4 != "— select —":
                match4 = next((r for r in results4 if r["label"] == chosen4), None)
                if match4:
                    selected4 = match4["ticker"]
                    st.session_state.selected_tickers[3] = selected4
        else:
            st.warning("No results found")
    else:
        selected4 = st.session_state.selected_tickers[3]
    
    if selected4:
        st.success(f"✅ {selected4}")

# ── Get selected tickers ──────────────────────────────────────────────────────
selected_tickers = [t for t in st.session_state.selected_tickers if t]

if not selected_tickers:
    st.info("👆 Search for and select at least one stock to compare.")
    st.stop()

# ── Fetch data for all selected stocks ────────────────────────────────────────
st.divider()

with st.spinner("Fetching stock data from Yahoo Finance..."):
    stock_data = {}
    for ticker in selected_tickers:
        info = get_stock_info(ticker)
        if info:
            stock_data[ticker] = info
        else:
            st.error(f"Could not fetch data for {ticker}")

if not stock_data:
    st.stop()

# ── Display stock cards ───────────────────────────────────────────────────────
st.subheader("📊 Stock Details")

cols = st.columns(len(stock_data))

for col, (ticker, info) in zip(cols, stock_data.items()):
    with col:
        name = info.get("longName", ticker)
        price = info.get("currentPrice")
        
        st.subheader(ticker)
        st.write(f"**{name}**")
        
        if price is not None:
            st.metric("Stock Price", f"${price:,.2f}")
        else:
            st.metric("Stock Price", "N/A")
        
        st.markdown(f"**Profit Margin:** {format_value(info.get('profitMargins'))}")
        st.markdown(f"**Revenue Growth:** {format_value(info.get('revenueGrowth'))}")
        st.markdown(f"**ROE:** {format_value(info.get('returnOnEquity'))}")
        st.markdown(f"**P/E Ratio:** {format_value(info.get('trailingPE'))}")
        st.markdown(f"**EPS:** {format_value(info.get('trailingEPS'))}")
        st.markdown(f"**Price/Book:** {format_value(info.get('priceToBook'))}")
        st.markdown(f"**EV/EBITDA:** {format_value(info.get('enterpriseToEbitda'))}")
        st.markdown(f"**EBITDA:** {format_value(info.get('ebitda'))}")

st.divider()

# ── Comparison table ──────────────────────────────────────────────────────────
st.subheader("📋 Comparison Table")

table_data = {
    'Indicators': [
        'Stock Price',
        'Profit Margin',
        'Revenue Growth',
        'ROE',
        'P/E Ratio',
        'EPS',
        'Price/Book',
        'EV/EBITDA',
        'EBITDA'
    ]
}

for ticker, info in stock_data.items():
    table_data[ticker] = [
        format_value(info.get('currentPrice')),
        format_value(info.get('profitMargins')),
        format_value(info.get('revenueGrowth')),
        format_value(info.get('returnOnEquity')),
        format_value(info.get('trailingPE')),
        format_value(info.get('trailingEPS')),
        format_value(info.get('priceToBook')),
        format_value(info.get('enterpriseToEbitda')),
        format_value(info.get('ebitda'))
    ]

df = pd.DataFrame(table_data)
df = df.set_index('Indicators')
st.dataframe(df, use_container_width=True)

st.divider()

col_left, col_center, col_right = st.columns(3)
with col_left:
    st.caption("Data from Yahoo Finance")
