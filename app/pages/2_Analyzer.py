"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Portfolio Allocation"-page, where the user can build a portfolio by searching and adding stocks one by one.
The idea is to give the user a quick way to see how his portfolio is balanced across currencies, regions, industries and risk levels.
On top of that, beta values from Yahoo Finance are used to label each stock as low, medium or high risk so the user can spot concentration issues at a glance.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import requests

# Page configuration, title, subtitle and tab icon (logo without text)
# Logo and tab icon by Claude
st.set_page_config(
    page_title="Portfolio Allocation",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)

st.title("Portfolio Allocation")

st.markdown("Search for ticker, company name, ISIN or valor")

st.page_link("Home.py", label="Go to Homepage")

# Adds the logo of our website at the top right corner
st.markdown("""
    <style>
    .easy-investing-logo {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 130px;
        z-index: 9999;
    }
    </style>
    <div class="easy-investing-logo">
        <svg viewBox="0 0 680 500" xmlns="http://www.w3.org/2000/svg">
            <rect x="160" y="40" width="360" height="360" rx="50" fill="#0d1b2a"/>
            <rect x="220" y="220" width="55" height="150" rx="4" fill="#ffffff"/>
            <rect x="312" y="270" width="55" height="100" rx="4" fill="#ffffff"/>
            <rect x="404" y="160" width="55" height="210" rx="4" fill="#ffffff"/>
            <polyline points="195,300 247.5,220 339.5,270 445,148"
                      fill="none" stroke="#1f8fff" stroke-width="14"
                      stroke-linecap="round" stroke-linejoin="round"/>
            <g transform="translate(445,148) rotate(-41.63)">
                <polygon points="-26,-22 22,0 -26,22" fill="#1f8fff"
                         stroke="#1f8fff" stroke-width="6" stroke-linejoin="round"/>
            </g>
            <text x="340" y="465" font-size="58" font-weight="800"
                  text-anchor="middle" letter-spacing="-1"
                  font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">
                <tspan fill="#1f8fff">Easy</tspan><tspan fill="#ffffff"> Investing</tspan>
            </text>
        </svg>
    </div>
""", unsafe_allow_html=True)


# ── Region mapping by exchange ────────────────────────────────────────────────
def get_region(ticker_info):
    exchange = ticker_info.get("exchange", "")
    country  = ticker_info.get("country", "")
    mapping = {
        "NMS": "North America", "NYQ": "North America", "NGM": "North America",
        "PCX": "North America", "ASE": "North America", "TSX": "North America",
        "LSE": "Europe", "XETRA": "Europe", "EPA": "Europe", "BIT": "Europe",
        "SWX": "Europe", "AMS": "Europe", "MCE": "Europe",
        "TYO": "Asia", "HKG": "Asia", "SHH": "Asia", "SHZ": "Asia",
        "NSE": "Asia", "BSE": "Asia", "KSC": "Asia", "TWO": "Asia",
        "ASX": "Oceania",
        "SAO": "Latin America", "BMV": "Latin America",
        "TLV": "Middle East", "DFM": "Middle East",
        "JSE": "Africa",
    }
    return mapping.get(exchange, country if country else "Other")

# ── Risk based on beta ────────────────────────────────────────────────────────
def get_risk(beta):
    if beta is None:
        return "Unknown"
    if beta < 0.8:
        return "Low"
    elif beta < 1.3:
        return "Medium"
    else:
        return "High"

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

# ── Fetch stock data from Yahoo Finance ──────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_stock(ticker, quantity):
    try:
        t    = yf.Ticker(ticker)
        info = t.info
        price    = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        currency = info.get("currency", "USD")
        industry = info.get("industry") or info.get("sector") or "Unknown"
        beta     = info.get("beta")
        name     = info.get("shortName") or ticker

        if price is None:
            return None, f"Could not get price for **{ticker}**"

        value  = round(price * quantity, 2)
        region = get_region(info)
        risk   = get_risk(beta)

        return {
            "Ticker":      ticker.upper(),
            "Name":        name,
            "Quantity":    quantity,
            "Price":       price,
            "Currency":    currency,
            "Value (USD)": value,
            "Industry":    industry,
            "Region":      region,
            "Risk":        risk,
        }, None
    except Exception as e:
        return None, f"Error fetching **{ticker}**: {str(e)}"

# ── Session state ─────────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

# ── Search section ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Search & add stocks")

search_query = st.text_input("Search for a stock",
                              placeholder="e.g. Apple, AAPL, NESN, CH0012221716...",
                              key="search_box")

selected_ticker = None
selected_name   = None

if search_query:
    with st.spinner("Searching..."):
        results = search_stocks(search_query)

    if results:
        options = ["select a stock"] + [r["label"] for r in results]
        chosen  = st.selectbox("Results", options, key="search_select")

        if chosen != "select a stock":
            match = next((r for r in results if r["label"] == chosen), None)
            if match:
                selected_ticker = match["ticker"]
                selected_name   = match["name"]
    else:
        st.warning("No results found. Try a different search term.")

if selected_ticker:
    col_qty, col_btn = st.columns([2, 1])
    with col_qty:
        qty = st.number_input(f"Quantity for {selected_ticker}",
                              min_value=1, value=1, key="qty_input")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add to portfolio", type="primary"):
            already = any(r["ticker"] == selected_ticker for r in st.session_state.portfolio)
            if already:
                st.warning(f"{selected_ticker} is already in your portfolio!")
            else:
                st.session_state.portfolio.append({
                    "ticker":   selected_ticker,
                    "name":     selected_name,
                    "quantity": qty,
                })
                st.success(f"✅ Added {selected_ticker}!")
                st.rerun()

# ── Current portfolio list ────────────────────────────────────────────────────
st.markdown("---")

col_sample, col_clear = st.columns([2, 5])
with col_sample:
    if st.button("Load sample portfolio"):
        st.session_state.portfolio = [
            {"ticker": "AAPL",    "name": "Apple Inc.",   "quantity": 10},
            {"ticker": "NESN.SW", "name": "Nestlé S.A.",  "quantity": 5},
            {"ticker": "TSLA",    "name": "Tesla Inc.",    "quantity": 3},
            {"ticker": "BABA",    "name": "Alibaba Group", "quantity": 8},
            {"ticker": "LVMUY",   "name": "LVMH",          "quantity": 4},
        ]
        st.rerun()
with col_clear:
    if st.button("Clear") and st.session_state.portfolio:
        st.session_state.portfolio = []
        st.rerun()

if st.session_state.portfolio:
    st.subheader("Your portfolio")
    updated_rows = []
    for i, row in enumerate(st.session_state.portfolio):
        c1, c2, c3, c4 = st.columns([1.5, 3, 1.5, 0.5])
        c1.markdown(f"**{row['ticker']}**")
        c2.markdown(row.get("name", ""))
        quantity = c3.number_input("Qty", value=int(row["quantity"]),
                                   min_value=1, key=f"qty_{i}",
                                   label_visibility="collapsed")
        remove = c4.button("❌", key=f"del_{i}")
        if not remove:
            updated_rows.append({**row, "quantity": quantity})
    st.session_state.portfolio = updated_rows
else:
    st.info("Search for a stck first and see your analysis")

# ── Analyze button ────────────────────────────────────────────────────────────
st.markdown("")
analyze = st.button("Analyze Portfolio", type="primary", use_container_width=True)

if analyze:
    rows = st.session_state.portfolio
    if not rows:
        st.warning("Please add at least one stock first.")
    else:
        results = []
        errors  = []
        with st.spinner("Fetching data from Yahoo Finance..."):
            for row in rows:
                data, err = fetch_stock(row["ticker"], row["quantity"])
                if data:
                    results.append(data)
                else:
                    errors.append(err)

        for e in errors:
            st.error(e)

        if results:
            df    = pd.DataFrame(results)
            total = df["Value (USD)"].sum()

            st.markdown("---")
            st.subheader("Portfolio Breakdown")
            st.metric("Total Portfolio Value", f"${total:,.2f}")

            COLORS = px.colors.qualitative.Set3

            def make_pie(group_col, title):
                grouped = df.groupby(group_col)["Value (USD)"].sum().reset_index()
                grouped.columns = [group_col, "Value"]
                fig = px.pie(grouped, values="Value", names=group_col,
                             title=title, color_discrete_sequence=COLORS, hole=0.35)
                fig.update_traces(textposition="inside", textinfo="percent+label")
                fig.update_layout(showlegend=True, title_font_size=16,
                                  margin=dict(t=60, b=20, l=20, r=20))
                return fig

            def make_risk_pie(title):
                risk_groups = df.groupby("Risk").apply(
                    lambda g: "<br>".join(
                        f"{row['Ticker']} ({row['Name']}): ${row['Value (USD)']:,.0f}"
                        for _, row in g.iterrows()
                    )
                ).reset_index()
                risk_groups.columns = ["Risk", "Stocks"]
                grouped = df.groupby("Risk")["Value (USD)"].sum().reset_index()
                grouped.columns = ["Risk", "Value"]
                grouped = grouped.merge(risk_groups, on="Risk")
                fig = px.pie(grouped, values="Value", names="Risk",
                             title=title, color_discrete_sequence=COLORS,
                             hole=0.35, custom_data=["Stocks"])
                fig.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>Value: $%{value:,.0f}<br>(%{percent})<br><br>Stocks:<br>%{customdata[0]}<extra></extra>"
                )
                fig.update_layout(showlegend=True, title_font_size=16,
                                  margin=dict(t=60, b=20, l=20, r=20))
                return fig

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(make_pie("Currency", "By Currency"), use_container_width=True)
                st.plotly_chart(make_pie("Region",   "By Region"),   use_container_width=True)
            with col2:
                st.plotly_chart(make_pie("Industry", "By Industry"), use_container_width=True)
                st.plotly_chart(make_risk_pie("By Risk"), use_container_width=True)

            st.markdown("---")
            st.subheader("Portfolio Summary")
            df["Weight (%)"] = (df["Value (USD)"] / total * 100).round(2)
            st.dataframe(
                df[["Ticker", "Name", "Quantity", "Price", "Currency",
                    "Value (USD)", "Weight (%)", "Industry", "Region", "Risk"]]
                .sort_values("Value (USD)", ascending=False),
                use_container_width=True
            )
