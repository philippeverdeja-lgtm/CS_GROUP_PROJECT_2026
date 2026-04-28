# this is the main stock analysis page
# it shows detailed info for one stock and lets you compare multiple stocks

import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
from yahooquery import Ticker
import requests

# page setup
st.set_page_config(page_title="Stock Analyzer", page_icon="", layout="wide")

st.title(" Stock Comparator")
st.write("Search for a stock to get detailed financial data, charts and comparisons.")

st.markdown("""
    <style>
    .monopoly-man {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 150px;
        z-index: 9999;
    }
    </style>
    <img class="monopoly-man" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWtleW5nNnJqdjA1aW5hODRsZGhzZzE5ZTJpcHRydDR4ZDU0Z21qayZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/C8976bDqhEUk40i8XU/giphy.gif">
""", unsafe_allow_html=True)

# ── Search Yahoo Finance ──────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def search_stocks(query):
    if not query or len(query) < 2:
        return []
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=8&newsCount=0&enableFuzzyQuery=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
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

# --- Search bar for first stock ---
search_query = st.text_input("Search a stock (e.g. Nestlé, AAPL, GOOG, MSFT)", 
                              placeholder="Type company name or ticker...",
                              key="main_search")

ticker_input = None

if search_query:
    with st.spinner("Searching..."):
        results = search_stocks(search_query)
    
    if results:
        options = ["select a stock"] + [r["label"] for r in results]
        chosen = st.selectbox("Results", options, key="main_selectbox")
        
        if chosen != "select a stock":
            match = next((r for r in results if r["label"] == chosen), None)
            if match:
                ticker_input = match["ticker"]
    else:
        st.warning("No results found. Try a different search term.")

# --- Ask how many stocks to compare ---
# we only show extra inputs if user wants to compare
n_compare = st.radio(
    "How many stocks do you want to compare?",
    [1, 2, 3, 4],
    horizontal=True
)

# --- Extra ticker inputs if comparing ---
# we store all tickers in a list
all_tickers = []
if ticker_input:
    all_tickers = [ticker_input]

if n_compare > 1 and ticker_input:
    st.markdown("##### Add stocks to compare")
    extra_cols = st.columns(n_compare - 1)
    for i, col in enumerate(extra_cols):
        with col:
            extra_search = st.text_input(f"Stock {i+2} (company name or ticker)",
                                         placeholder="Type to search...",
                                         key=f"extra_search_{i}")
            
            extra_ticker = None
            if extra_search:
                with st.spinner("Searching..."):
                    extra_results = search_stocks(extra_search)
                
                if extra_results:
                    extra_options = ["select"] + [r["label"] for r in extra_results]
                    extra_chosen = st.selectbox("Results", extra_options, 
                                               key=f"extra_selectbox_{i}",
                                               label_visibility="collapsed")
                    
                    if extra_chosen != "select":
                        extra_match = next((r for r in extra_results if r["label"] == extra_chosen), None)
                        if extra_match:
                            extra_ticker = extra_match["ticker"]
            
            if extra_ticker:
                all_tickers.append(extra_ticker)

# remove empty tickers from list
all_tickers = [t for t in all_tickers if t]

# --- Function to fetch all data for one stock ---
# we cache it for 5 min so the app doesn't call Yahoo Finance every second
@st.cache_data(ttl=300)
def get_stock_data(ticker):
    # get 1 year of daily price history from yfinance
    hist = yf.Ticker(ticker).history(period="1y")

    # get fundamentals from yahooquery
    yq = Ticker(ticker)

    # price info - current price and daily change
    price_info = yq.price.get(ticker, {})
    if not isinstance(price_info, dict):
        price_info = {}

    # financial metrics - margins, ROE etc.
    fin = yq.financial_data.get(ticker, {})
    stats = yq.key_stats.get(ticker, {})
    summary = yq.summary_detail.get(ticker, {})

    # combine everything into one dictionary
    info = {**fin, **stats, **summary}
    info["longName"]     = price_info.get("longName", ticker)
    info["currentPrice"] = price_info.get("regularMarketPrice")
    info["change"]       = price_info.get("regularMarketChangePercent", 0)

    # income statement - revenue, ebitda, net income over time
    try:
        income = yq.income_statement(frequency="a")
        # keep only the columns we need
        cols_we_want = ["asOfDate", "TotalRevenue", "EBITDA", "NetIncome"]
        cols_available = [c for c in cols_we_want if c in income.columns]
        income = income[cols_available].dropna()
    except:
        income = pd.DataFrame()

    return hist, info, income

# --- Only run if user typed at least one ticker ---
if not all_tickers:
    st.info("👆 Search for a stock above to get started.")
    st.stop()

# fetch data for all tickers
with st.spinner("Fetching data from Yahoo Finance..."):
    stock_data = {}
    for t in all_tickers:
        try:
            hist, info, income = get_stock_data(t)
            stock_data[t] = (hist, info, income)
        except:
            st.error(f"Could not find data for {t}. Check the ticker symbol.")

if not stock_data:
    st.stop()

st.divider()

# =============================================================
# SECTION 1 - COMPANY HEADER AND KEY METRICS
# =============================================================

# show company name, price and daily change for each stock
header_cols = st.columns(len(stock_data))
for col, (ticker, (hist, info, income)) in zip(header_cols, stock_data.items()):
    with col:
        name   = info.get("longName", ticker)
        price  = info.get("currentPrice")
        change = info.get("change", 0) * 100
        arrow  = "🟢 +" if change >= 0 else "🔴 "

        st.subheader(f"{ticker}")
        st.write(f"**{name}**")
        if price:
            st.metric(
                label="Current Price",
                value=f"${price:,.2f}",
                delta=f"{change:.2f}%"
            )

st.divider()

# =============================================================
# SECTION 2 - KEY FINANCIAL METRICS TABLE
# shows all metrics side by side for comparison
# =============================================================

st.subheader("📋 Key Financial Metrics")

# list of metrics we want to show and their readable names
metrics = {
    "currentPrice":       "Price",
    "trailingPE":         "P/E Ratio",
    "priceToBook":        "Price / Book",
    "profitMargins":      "Profit Margin",
    "operatingMargins":   "Operating Margin",
    "revenueGrowth":      "Revenue Growth",
    "returnOnEquity":     "ROE",
    "returnOnAssets":     "ROA",
    "totalDebtToEquity":  "Debt / Equity",
    "trailingEps":        "EPS",
    "ebitda":             "EBITDA",
    "enterpriseToEbitda": "EV / EBITDA",
}

# build a table with one column per stock
table_data = {"Metric": list(metrics.values())}
for ticker, (hist, info, income) in stock_data.items():
    values = []
    for key in metrics:
        val = info.get(key)
        if val is None:
            values.append("N/A")
        elif isinstance(val, float):
            # format percentages and large numbers nicely
            if key in ["profitMargins", "operatingMargins", "revenueGrowth", "returnOnEquity", "returnOnAssets"]:
                values.append(f"{val*100:.1f}%")
            elif key == "ebitda":
                values.append(f"${val/1e9:.1f}B")
            else:
                values.append(f"{val:.2f}")
        else:
            values.append(str(val))
    table_data[ticker] = values

# show as a table
df_metrics = pd.DataFrame(table_data).set_index("Metric")
st.dataframe(df_metrics, use_container_width=True)

st.divider()

# =============================================================
# SECTION 3 - CHARTS
# =============================================================

st.subheader("📈 Charts")

# --- Price History with time period selector ---
st.markdown("#### Price History")

# let user pick the time period - yfinance accepts these directly
period = st.radio(
    "Select period:",
    ["YTD", "1Y", "5Y", "10Y", "Max"],
    horizontal=True
)

# convert our labels to yfinance format
period_map = {
    "YTD": "ytd",
    "1Y":  "1y",
    "5Y":  "5y",
    "10Y": "10y",
    "Max": "max"
}

# fetch price history again with the selected period
# we do this separately from the main data fetch so it updates when period changes
@st.cache_data(ttl=300)
def get_price_history(ticker, period):
    return yf.Ticker(ticker).history(period=period)

price_fig = px.line(title="Stock Price")
for ticker in stock_data:
    hist = get_price_history(ticker, period_map[period])
    if not hist.empty:
        price_fig.add_scatter(
            x=hist.index,
            y=hist["Close"],
            name=ticker,
            mode="lines"
        )

price_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    hovermode="x unified",
    legend_title="Stock"
)
st.plotly_chart(price_fig, use_container_width=True)

st.divider()

# --- Revenue, EBITDA, Net Income - last 5 years, one bar per year ---
st.markdown("#### Financials (Last 5 Years)")

# helper function to clean up income data
# keeps only annual data and last 5 years, one row per year
def clean_income(income_df):
    if income_df.empty:
        return income_df
    # convert date to year only
    income_df = income_df.copy()
    income_df["Year"] = pd.to_datetime(income_df["asOfDate"]).dt.year
    # keep only last 5 years
    last_5 = sorted(income_df["Year"].unique())[-5:]
    income_df = income_df[income_df["Year"].isin(last_5)]
    # one row per year - take the last entry if duplicates
    income_df = income_df.drop_duplicates(subset="Year", keep="last")
    return income_df

chart_col1, chart_col2 = st.columns(2)

# Revenue chart
with chart_col1:
    st.markdown("##### Revenue")
    rev_fig = px.bar(title="Annual Revenue (Last 5Y)")
    for ticker, (hist, info, income) in stock_data.items():
        if not income.empty and "TotalRevenue" in income.columns:
            clean = clean_income(income)
            rev_fig.add_bar(
                x=clean["Year"].astype(str),
                y=clean["TotalRevenue"] / 1e9,
                name=ticker
            )
    rev_fig.update_layout(
        yaxis_title="Revenue (USD Billions)",
        xaxis_title="Year",
        barmode="group"
    )
    st.plotly_chart(rev_fig, use_container_width=True)

# EBITDA chart
with chart_col2:
    st.markdown("##### EBITDA")
    ebitda_fig = px.bar(title="Annual EBITDA (Last 5Y)")
    for ticker, (hist, info, income) in stock_data.items():
        if not income.empty and "EBITDA" in income.columns:
            clean = clean_income(income)
            ebitda_fig.add_bar(
                x=clean["Year"].astype(str),
                y=clean["EBITDA"] / 1e9,
                name=ticker
            )
    ebitda_fig.update_layout(
        yaxis_title="EBITDA (USD Billions)",
        xaxis_title="Year",
        barmode="group"
    )
    st.plotly_chart(ebitda_fig, use_container_width=True)

# Net Income - full width
st.markdown("##### Net Income")
ni_fig = px.bar(title="Annual Net Income (Last 5Y)")
for ticker, (hist, info, income) in stock_data.items():
    if not income.empty and "NetIncome" in income.columns:
        clean = clean_income(income)
        ni_fig.add_bar(
            x=clean["Year"].astype(str),
            y=clean["NetIncome"] / 1e9,
            name=ticker
        )
ni_fig.update_layout(
    yaxis_title="Net Income (USD Billions)",
    xaxis_title="Year",
    barmode="group"
)
st.plotly_chart(ni_fig, use_container_width=True)
