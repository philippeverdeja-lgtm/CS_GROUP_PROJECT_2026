"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Portfolio Allocation"-page, where the user can build a portfolio by searching and adding stocks one by one.
The idea is to give the user a quick way to see how his portfolio is balanced across currencies, regions, industries and risk levels.
On top of that, beta values from Yahoo Finance are used to label each stock as low, medium or high risk so the user can spot concentration issues at a glance.
"""

#All the libraries we need are imported at the top so they are available everywhere
#Streamlit is the framework we use to turn our python code into a real web app
import streamlit as st
#Pandas is for handling tables of data
import pandas as pd
#Plotly is the chart library we use because its charts are interactive
#the user can hover, zoom, etc. and they integrate nicely with streamlit
import plotly.express as px
#graph_objects gives us lower-level chart control, needed for the performance chart
import plotly.graph_objects as go
#yfinance fetches stock prices, company info and historical data from Yahoo Finance
import yfinance as yf
#The requests library is the standard way to call web APIs in python
import requests
#random is used to pick stocks and weights for the random portfolio generator
import random


#Browser tab title, page icon (logo without text), use the full width of the screen and also title/subtitle for this page
#Logo and tab icon by Claude
st.set_page_config(
    page_title="Portfolio Allocation",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)

st.title("Portfolio Allocation")

st.markdown("Search for ticker, company name, ISIN or valor")

st.page_link("Home.py", label="Go to Homepage")

#Adds the logo of our website at the top right corner
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


#A list of known and large MSCI World stocks across the US, Europe and Asia
#These are used by the random portfolio generator so the user always different stocks
MSCI_WORLD_STOCKS = [
    ("AAPL",  "Apple Inc."),       ("MSFT",  "Microsoft"),
    ("NVDA",  "NVIDIA"),           ("AMZN",  "Amazon"),
    ("GOOGL", "Alphabet"),         ("META",  "Meta"),
    ("BRK-B", "Berkshire Hathaway"),("LLY",  "Eli Lilly"),
    ("JPM",   "JPMorgan Chase"),   ("V",     "Visa"),
    ("XOM",   "ExxonMobil"),       ("UNH",   "UnitedHealth"),
    ("JNJ",   "Johnson & Johnson"),("PG",    "Procter & Gamble"),
    ("MA",    "Mastercard"),       ("HD",    "Home Depot"),
    ("ABBV",  "AbbVie"),           ("MRK",   "Merck"),
    ("COST",  "Costco"),           ("CVX",   "Chevron"),
    ("PEP",   "PepsiCo"),          ("KO",    "Coca-Cola"),
    ("WMT",   "Walmart"),          ("BAC",   "Bank of America"),
    ("CRM",   "Salesforce"),       ("TMO",   "Thermo Fisher"),
    ("NFLX",  "Netflix"),          ("TSLA",  "Tesla"),
    ("AMD",   "AMD"),              ("INTC",  "Intel"),
    ("NESN.SW","Nestlé"),          ("NOVN.SW","Novartis"),
    ("ROG.SW","Roche"),            ("ABBN.SW","ABB"),
    ("ZURN.SW","Zurich Insurance"),("LONN.SW","Lonza"),
    ("ASML",  "ASML"),             ("SAP",   "SAP"),
    ("LVMUY", "LVMH"),             ("TTE",   "TotalEnergies"),
    ("SIE.DE","Siemens"),          ("BAYZF", "Bayer"),
    ("DGEAF", "Diageo"),           ("HSBC",  "HSBC"),
    ("BP",    "BP"),               ("AZN",   "AstraZeneca"),
    ("SHEL",  "Shell"),            ("TSM",   "Taiwan Semiconductor"),
    ("TM",    "Toyota"),           ("SONY",  "Sony"),
    ("BABA",  "Alibaba"),          ("TCEHY", "Tencent"),
    ("NVO",   "Novo Nordisk"),     ("RIO",   "Rio Tinto"),
    ("BHP",   "BHP Group"),
]

#Asigns region to stock
def get_region(ticker_info):
    """Map a stock's exchange code to a readable region name.
    We fall back to the country field if the exchange isn't in our map,
    and to "Other" if neither is available."""
    exchange = ticker_info.get("exchange", "")
    country  = ticker_info.get("country", "")
    mapping = {
        #North American exchanges
        "NMS":"North America","NYQ":"North America","NGM":"North America",
        "PCX":"North America","ASE":"North America","TSX":"North America",
        #European exchanges
        "LSE":"Europe","XETRA":"Europe","EPA":"Europe","BIT":"Europe",
        "SWX":"Europe","AMS":"Europe","MCE":"Europe",
        #Asian exchanges
        "TYO":"Asia","HKG":"Asia","SHH":"Asia","SHZ":"Asia",
        "NSE":"Asia","BSE":"Asia","KSC":"Asia","TWO":"Asia",
        #Other exchanges
        "ASX":"Oceania","SAO":"Latin America","BMV":"Latin America",
        "TLV":"Middle East","DFM":"Middle East","JSE":"Africa",
    }
    #yfinance returns a exchange code and a country. First it looks up the code
    #in the above section. If there are no matches the country comes into play
    #if this is also empty it just uses "other"
    return mapping.get(exchange, country if country else "Other")


def get_risk(beta):
    """Convert a beta value into a low/medium/high risk label.
    Beta measures how much a stock moves relative to the market.
    Below 0.8 means it moves less than the market (low risk),
    above 1.3 means it moves more than the market (high risk)."""
    #If yfinance does not return a beta, stock cannot be classified
    if beta is None: return "Unkown"
    #Below 0.8 a stock is less vlatile and considered low risk
    if beta < 0.8:   return "Low"
    #Between 0.8 and 1.3 stock moves more or less with the market
    if beta < 1.3:   return "Medium"
    #Above 1.3 stock moves more than the market and is considered high risk
    return "High"


#@st.cache_data means streamlit remembers the result for the same query
#so yfinance is not requested again if the user types the same thing twice -> increases speed
@st.cache_data(show_spinner=False)
def search_stocks(query):
    """Call Yahoo Finance's search endpoint and return matching stocks.
    We filter to only equities, ETFs and mutual funds to avoid noise."""
    #Only start search after user wrote 2 characters
    if not query or len(query) < 2:
        return []
    #We do a try/except in case Yahoo is unreachable, so app doesn't crash
    try:
        url = (f"https://query2.finance.yahoo.com/v1/finance/search"
               f"?q={query}&quotesCount=8&newsCount=0&enableFuzzyQuery=true")
        #Yahoo blocks requests from bots -> needs to pretend to be a browser
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        results = []
        for item in r.json().get("quotes", []):
            ticker   = item.get("symbol", "")
            #Use long name if available, otherwise fall back to short name
            name     = item.get("longname") or item.get("shortname") or ""
            exchange = item.get("exchDisp", "")
            typ      = item.get("quoteType", "")
            #Only keep results that are actual tradeable instruments
            if ticker and typ in ("EQUITY", "ETF", "MUTUALFUND"):
                results.append({
                    "label":  f"{ticker} — {name} ({exchange})",
                    "ticker": ticker,
                    "name":   name,
                })
        return results
    except Exception:
        return []


#Same cache logic as above — if the user re-analyzes with the same ticker
#and quantity, reuse the cached result instead of calling yfinance again
@st.cache_data(show_spinner=False)
def fetch_stock(ticker, quantity):
    """Fetch a single stock's current price and metadata from Yahoo Finance.
    Returns a dict with everything we need for the portfolio table, or None on failure."""
    try:
        info     = yf.Ticker(ticker).info
        #Trys three different price fields in order of preference
        price    = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
        currency = info.get("currency", "USD")
        #Uses industry first, fall back to sector if industry isn't available
        industry = info.get("industry") or info.get("sector") or "Unknown"
        beta     = info.get("beta")
        name     = info.get("shortName") or ticker
        if price is None:
            return None, f"Could not get price for **{ticker}**"
        return {
            "Ticker":      ticker.upper(),
            "Name":        name,
            "Quantity":    quantity,
            "Price":       price,
            "Currency":    currency,
            #Total value of this position in USD
            "Value (USD)": round(price * quantity, 2),
            "Industry":    industry,
            "Region":      get_region(info),
            "Risk":        get_risk(beta),
        }, None
    except Exception as e:
        return None, f"Error fetching **{ticker}**: {str(e)}"

#Cache key is portfolio_rows_tuple (a tuple of ticker/quantity pairs) and period
#Uses tuple instead of list because lists are not hashable and can't be used as cache keys
@st.cache_data(show_spinner=False)
def fetch_portfolio_history(portfolio_rows_tuple, period):
    """Download historical closing prices for all stocks in the portfolio,
    multiply each by its quantity to get position values, then sum everything
    into a single portfolio value series and normalise it to 100 at the start."""
    #Maps period labels user can see to the strings yfinance accepts
    period_map = {
        "1M": "1mo", "3M": "3mo", "YTD": "ytd",
        "1Y": "1y",  "3Y": "3y",  "5Y": "5y", "All": "max",
    }

    frames = []
    for ticker, quantity in portfolio_rows_tuple:
        #Try/except so faulty ticker doesn't crash the whole chart
        try:
            hist = yf.Ticker(ticker).history(period=period_map[period])["Close"].dropna()
            if not hist.empty:
                #Multiply price by quantity to get the position's value over time
                frames.append(hist * quantity)
        except Exception:
            pass
    if not frames:
        return pd.Series(dtype=float)
    #Aligns all series on the same dates, forward-fill then backward-fill gaps
    #(holidays or missing data for some markets), then drop any rows still all-NaN
    df = pd.concat(frames, axis=1).ffill().bfill().dropna(how='all')
    portfolio_value = df.sum(axis=1)
    #Normalise to 100 at the start so % change can be shown regardless of portfolio size
    return portfolio_value / portfolio_value.iloc[0] * 100

#generation of random 20000 portfolio
def generate_random_portfolio(target_chf=20_000, n=10):
    """Pick n random stocks from the MSCI World list and calculate quantities
    so the total portfolio value is approximately target_chf.
    We use random weights so each stock gets a different allocation."""
    #Rough USD/CHF conversion so the final portfolio value is roughly in CHF
    USD_TO_CHF = 0.90
    target_usd = target_chf / USD_TO_CHF
    #random.sample picks n unique items from the list without replacement
    selected   = random.sample(MSCI_WORLD_STOCKS, n)
    #Generate n random numbers and normalise them so they sum to 1
    raw_w      = [random.random() for _ in range(n)]
    weights    = [w / sum(raw_w) for w in raw_w]
    portfolio  = []
    for (ticker, name), weight in zip(selected, weights):
        #Try/except so one stock failing doesn't break the whole generator
        try:
            info  = yf.Ticker(ticker).info
            price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
            if price and price > 0:
                #Divide this stock's allocated budget by its price to get the quantity
                #max(1, ...) ensures we always buy at least 1 share
                portfolio.append({
                    "ticker":   ticker,
                    "name":     name,
                    "quantity": max(1, round((weight * target_usd) / price)),
                })
        except Exception:
            pass
    return portfolio


#Session state persists across reruns of the page, unlike regular variables
#Used to keep the portfolio list and the analysis results between interactions
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "analysis_results" not in st.session_state:
    #None means no analysis has been run yet
    st.session_state.analysis_results = None


st.markdown("---")
st.subheader("Search & add stocks")

#Key parameter is important because every streamlit widget needs a unique key
#so streamlit can remember the value between reruns and tell widgets apart
search_query = st.text_input(
    "Search for a stock",
    placeholder="e.g. Apple, AAPL, NESN, CH0012221716...",
    key="search_box",
)
#Creation of individual portfolio
selected_ticker = None
selected_name   = None

if search_query:
    with st.spinner("Searching..."):
        results = search_stocks(search_query)
    if results:
        #Prepended a placeholder option so the selectbox doesn't auto-select the first result
        options = ["select a stock"] + [r["label"] for r in results]
        chosen  = st.selectbox("Results", options, key="search_select")
        #Only updates the selection if the user actually picked something
        if chosen != "select a stock":
            match = next((r for r in results if r["label"] == chosen), None)
            if match:
                selected_ticker = match["ticker"]
                selected_name   = match["name"]
    else:
        st.warning("No results found. Try a different search term.")

if selected_ticker:
    #st.columns() splits the page into vertical columns side by side
    col_qty, col_btn = st.columns([2, 1])
    with col_qty:
        qty = st.number_input(f"Quantity for {selected_ticker}", min_value=1, value=1, key="qty_input")
    with col_btn:
        #Small spacer so the button lines up vertically with the number input
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Add to portfolio", type="primary"):
            #Checks if this ticker is already in the portfolio to avoid duplicates
            if any(r["ticker"] == selected_ticker for r in st.session_state.portfolio):
                st.warning(f"{selected_ticker} is already in your portfolio!")
            else:
                st.session_state.portfolio.append(
                    {"ticker": selected_ticker, "name": selected_name, "quantity": qty}
                )
                #Clears old analysis results since the portfolio has changed
                st.session_state.analysis_results = None
                st.success(f"✅ Added {selected_ticker}!")
                #st.rerun() reruns the whole page so the portfolio list updates immediately
                st.rerun()

#Button "random portfolio" and "clear"
st.markdown("---")
#Two buttons side by side: one to load a random portfolio, one to clear everything
col_sample, col_clear = st.columns([2, 5])
with col_sample:
    if st.button("Random Portfolio (approx. CHF 20'000)"):
        with st.spinner("Picking 10 random MSCI World stocks..."):
            st.session_state.portfolio = generate_random_portfolio()
        st.session_state.analysis_results = None
        st.rerun()
with col_clear:
    if st.button("Clear") and st.session_state.portfolio:
        st.session_state.portfolio = []
        st.session_state.analysis_results = None
        st.rerun()
#Active selection of stocks in portfolio builder
if st.session_state.portfolio:
    st.subheader("Your portfolio")
    updated_rows = []
    for i, row in enumerate(st.session_state.portfolio):
        #Four columns: ticker, company name, quantity input, delete button
        c1, c2, c3, c4 = st.columns([1.5, 3, 1.5, 0.5])
        c1.markdown(f"**{row['ticker']}**")
        c2.markdown(row.get("name", ""))
        #The quantity input is editable so user can adjust shares without re-searching
        quantity = c3.number_input("Qty", value=int(row["quantity"]),
                                   min_value=1, key=f"qty_{i}",
                                   label_visibility="collapsed")
        if not c4.button("❌", key=f"del_{i}"):
            #Only keeps this row if the delete button was NOT pressed
            updated_rows.append({**row, "quantity": quantity})
        else:
            #Clears analysis results if the user removes a stock
            st.session_state.analysis_results = None
    st.session_state.portfolio = updated_rows
else:
    st.info("Search for a stock first and see your analysis")
 #--------------------------------------------------------------------------------------------------------

#The analyze button fetches live data for every stock and stores the results
#in session state so switching time periods later doesn't trigger the fetch again
st.markdown("")
if st.button("Analyze Portfolio", type="primary", use_container_width=True):
    rows = st.session_state.portfolio
    if not rows:
        st.warning("Please add at least one stock first.")
    else:
        results, errors = [], []
        with st.spinner("Fetching data from Yahoo Finance..."):
            for row in rows:
                data, err = fetch_stock(row["ticker"], row["quantity"])
                if data: results.append(data)
                else:    errors.append(err)
        for e in errors:
            st.error(e)
        if results:
            #Save to session state so the results stay during period button clicks
            st.session_state.analysis_results = results


#This block runs on every rerun, including when user switches the time period
#because analysis_results is in session state it is still available after a rerun
if st.session_state.analysis_results:
    df    = pd.DataFrame(st.session_state.analysis_results)
    total = df["Value (USD)"].sum()
    #Still needs the raw portfolio rows for the history chart
    rows  = st.session_state.portfolio

    st.markdown("---")
    st.subheader("Portfolio Breakdown")
    #Shows the total value as a headline metric at the top
    st.metric("Total Portfolio Value", f"${total:,.2f}")
#Creation of pie charts
    #Consistent color palette for all four pie charts
    COLORS = px.colors.qualitative.Set3

    def make_pie(group_col, title):
        """Group the portfolio by a given column and draw a donut pie chart.
        hole=0.35 gives the donut shape, textposition='inside' keeps labels clean."""
        g = df.groupby(group_col)["Value (USD)"].sum().reset_index()
        g.columns = [group_col, "Value"]
        fig = px.pie(g, values="Value", names=group_col,
                     title=title, color_discrete_sequence=COLORS, hole=0.35)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(showlegend=True, title_font_size=16,
                          margin=dict(t=60, b=20, l=20, r=20))
        return fig

    def make_risk_pie(title):
        """Same as make_pie but for the risk column, with a richer hover tooltip
        that lists all the stocks in each risk category and their individual values."""
        #Build a string of stock names and values for each risk level
        rg = df.groupby("Risk").apply(
            lambda g: "<br>".join(
                f"{r['Ticker']} ({r['Name']}): ${r['Value (USD)']:,.0f}"
                for _, r in g.iterrows()
            )
        ).reset_index()
        rg.columns = ["Risk", "Stocks"]
        g = df.groupby("Risk")["Value (USD)"].sum().reset_index()
        g.columns = ["Risk", "Value"]
        #Merges the stock list into the main dataframe so we can pass it as custom_data
        g = g.merge(rg, on="Risk")
        fig = px.pie(g, values="Value", names="Risk", title=title,
                     color_discrete_sequence=COLORS, hole=0.35, custom_data=["Stocks"])
        fig.update_traces(
            textposition="inside", textinfo="percent+label",
            #custom_data[0] holds the stock list string built above
            hovertemplate="<b>%{label}</b><br>Value: $%{value:,.0f}<br>(%{percent})<br><br>Stocks:<br>%{customdata[0]}<extra></extra>"
        )
        fig.update_layout(showlegend=True, title_font_size=16,
                          margin=dict(t=60, b=20, l=20, r=20))
        return fig

    #Two columns, two charts each: currency/region on the left, industry/risk on the right
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_pie("Currency", "By Currency"), use_container_width=True)
        st.plotly_chart(make_pie("Region",   "By Region"),   use_container_width=True)
    with col2:
        st.plotly_chart(make_pie("Industry", "By Industry"), use_container_width=True)
        st.plotly_chart(make_risk_pie("By Risk"),            use_container_width=True)
#creation of past performance chart
    st.markdown("---")
    st.subheader("Portfolio Past Performance")
    st.caption("Indexed to 100 at the start of each period — shows % gain or loss since then.")

    #Radio buttons to switch the time period -> clicking one triggers a rerun
    #but analysis_results is still in session state so we don't re-run anything
    period = st.radio(
        "Time period",
        ["1M", "3M", "YTD", "1Y", "3Y", "5Y", "All"],
        horizontal=True,
        key="perf_period",
    )

    #Convert to a tuple so it's hashable and can be used as a cache key
    portfolio_rows_tuple = tuple((r["ticker"], r["quantity"]) for r in rows)

    with st.spinner("Loading historical prices..."):
        perf = fetch_portfolio_history(portfolio_rows_tuple, period)

    if perf.empty:
        st.warning("Could not load historical data for this portfolio.")
    else:
        #Calculates the overall return for the selected period
        change_pct = perf.iloc[-1] - 100.0
        arrow = "▲" if change_pct >= 0 else "▼"
        color = "green" if change_pct >= 0 else "red"

        #Shows the period return as a coloured headline above the chart
        st.markdown(
            f"**Period return:** "
            f"<span style='color:{color}; font-size:1.1em'>{arrow} {change_pct:+.2f}%</span>",
            unsafe_allow_html=True,
        )

        #We use go.Figure instead of px because we want to combine a filled area
        #with a reference line
        fig = go.Figure()
        #The main line with a light blue fill underneath it
        fig.add_trace(go.Scatter(
            x=perf.index,
            y=perf.values,
            mode="lines",
            line=dict(color="#4C9BE8", width=2),
            fill="tozeroy",
            fillcolor="rgba(76,155,232,0.12)",
            name="Portfolio value",
            hovertemplate="%{x|%d %b %Y}<br>Index: %{y:.2f}<extra></extra>",
        ))
        #Dotted horizontal line at 100 so it's easy to see if the portfolio is up or down
        fig.add_hline(y=100, line_dash="dot", line_color="gray",
                      annotation_text="Start", annotation_position="left")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Indexed value (start = 100)",
            hovermode="x unified",
            showlegend=False,
            margin=dict(t=30, b=40, l=60, r=20),
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

        #An expander keeps the explanation out of the way until the user wants it
        with st.expander("How to read this chart"):
            st.write("""
            - The portfolio value is **normalised to 100** at the start of the selected period.
            - A value of **110** means the portfolio gained **+10%** since then.
            - A value of **85** means the portfolio lost **-15%** since then.
            - Each asset contributes proportionally based on the number of shares you hold.
            - Prices are in each stock's local currency -> no FX conversion is applied.
            - If an asset is only listed since a few months -> only avaliable data is used and calculated in the performance 
            """)
#Creation of summary
    st.markdown("---")
    st.subheader("Portfolio Summary")
    #Add a weight column so the user can see how concentrated each position is
    df["Weight (%)"] = (df["Value (USD)"] / total * 100).round(2)
    #Sort by value descending so the biggest positions appear at the top
    st.dataframe(
        df[["Ticker", "Name", "Quantity", "Price", "Currency",
            "Value (USD)", "Weight (%)", "Industry", "Region", "Risk"]]
        .sort_values("Value (USD)", ascending=False),
        use_container_width=True,
    )
