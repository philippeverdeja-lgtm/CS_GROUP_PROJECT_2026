"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Stock Analyzer"-page, split into "Key Metrics", "Charts" and "Forecast".
The idea is to give the user a quick and simple way to research any stock.
On top of that, up to 4 stocks can be put side by side and a 1-year price forecast is generated.
"""

# All the libraries we need are imported at the top so they are available everywhere
# Streamlit is the framework we use to turn our python code into a real web app
import streamlit as st
# Pandas is for handling tables of data, numpy is for fast math on arrays
import pandas as pd
import numpy as np
# Plotly is the chart library we use because its charts are interactive
# the user can hover, zoom, etc. and they integrate nicely with streamlit
import plotly.express as px
# The requests library is the standard way to call web APIs in python
import requests
# yfinance and yahooquery both fetch yahoo finance data, but each one returns
# different things, so we use both to get a more complete view of a stock
import yfinance as yf
from yahooquery import Ticker
# This is a widget that gives us a search box, nicer than the default streamlit text input 
from streamlit_searchbox import st_searchbox
# These are the machine learning models we will train to forecast prices
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


# Browser tab title, page icon (logo without text), use the full width of the screen and also title/subtitle for this page
# Logo and tab icon by Claude
st.set_page_config(
    page_title="Stock Analyzer",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)
st.title("Stock Analyzer")
st.write("Search for a stock to get detailed financial data, charts and comparisons.")

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

def search_stocks(query):
    """Return a list of (label, symbol) tuples from Yahoo's search API"""
    # If the user hasn't typed anything yet, return an empty list
    if query == "":
        return []
    # This is the public yahoo finance search endpoint and we ask for up to 5 results
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotesCount": 5}
    # Yahoo blocks requests without a User-Agent so we pretend to be a browser
    headers = {"User-Agent": "Mozilla/5.0"}
    # We do a try/except in case the yahoo is unreachable, so the app doesn't crash
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except:
        return []
    # Status code 200 means the request worked, anything else is a failure
    if response.status_code != 200:
        return []
    # We loop through the results and build a list that the searchbox can display to the user
    results = []
    for quote in response.json().get("quotes", []):
        symbol = quote.get("symbol", "")
        # Use the short name if available, otherwise fall back to the long name
        name = quote.get("shortname", "")
        if name == "":
            name = quote.get("longname", "")
        # Only add the result if we actually got a symbol back
        if symbol != "":
            results.append((symbol + " - " + name, symbol))
    return results


# Search bar for the first stock, it calls search_stocks() on every keystroke
# The key parameter is important because every streamlit widget needs a unique key
# so streamlit can remember the value between reruns and tell widgets apart
main_ticker = st_searchbox(
    search_function=search_stocks,
    placeholder="Search a stock (e.g. AAPL, GOOG, MSFT, NESN.SW)",
    key="main_search"
)
# Make sure main_ticker is always a string, never None because the searchbox returns 
# None before the user picks anything, but the rest of our code expects a string 
if main_ticker is None:
    main_ticker = ""


# We only show the comparison radio after the user picked a first stock
if main_ticker != "":
    # Buttons to let the user pick how many stocks to compare
    n_compare = st.radio("How many stocks do you want to compare?",
                         [1, 2, 3, 4], horizontal=True)
else:
    # Even if no stock is picked, we need n_compare otherwise the next lines would crash
    n_compare = 1


# The extra search bars if comparing more than 1 stock
all_tickers = [main_ticker]
# Only show extra bars after the first stock is picked
if n_compare > 1 and main_ticker != "":
    # st.columns() splits the page into equal vertical columns side by side
    extra_cols = st.columns(n_compare - 1)
    for i in range(n_compare - 1):
        # This tells streamlit to put the next widgets inside that specific column
        with extra_cols[i]:
            extra = st_searchbox(search_function=search_stocks,
                                 placeholder="Stock " + str(i + 2),
                                 # each searchbox needs a unique key
                                 key="extra_search_" + str(i))
            # Same None handling as before, but we still want a slot in the
            # list even if the user hasn't picked a stock yet, so we add ""
            if extra is not None:
                all_tickers.append(extra)
            else:
                all_tickers.append("")

# After the loop, all_tickers may have empty strings for searchboxes
# the user didn't fill in. We loop through and keep only the non-empty ones
clean_tickers = []
for t in all_tickers:
    if t != "":
        clean_tickers.append(t)
all_tickers = clean_tickers


# The cache tells streamlit to remember the results for 5 minutes.
# If the same ticker is asked again we get the saved answer instead of calling yahoo again. 
@st.cache_data(ttl=300, show_spinner=False)
def get_stock_data(ticker):
    """Fetch (info dict, income statement) for one stock"""
    # yahooquery's Ticker class is the entry point to all this data fetching
    yq = Ticker(ticker)
    # Current price and daily change
    price_info = yq.price.get(ticker, {})
    # Sometimes yahooquery returns a string error if the ticker doesn't exist, so we replace with empty dict
    if not isinstance(price_info, dict):
        price_info = {}
    # We merge 3 different dict from yahoo into a single info dict so we can look up any metric later
    info = {}
    for d in [yq.financial_data.get(ticker, {}), yq.key_stats.get(ticker, {}),
              yq.summary_detail.get(ticker, {})]:
        if isinstance(d, dict):
            info.update(d)
    # We then add the price info on top
    info["longName"] = price_info.get("longName", ticker)
    info["currentPrice"] = price_info.get("regularMarketPrice")
    info["change"] = price_info.get("regularMarketChangePercent", 0)
    info["currency"] = price_info.get("currency", "USD")
    # The income statement comes back as a pandas with many columns we only keep date + the 3 metrics
    try:
        income = yq.income_statement(frequency="a")
        cols = []
        for c in ["asOfDate", "TotalRevenue", "EBITDA", "NetIncome"]:
            # We check if the column exists before adding it to avoid a KeyError
            if c in income.columns:
                cols.append(c)
        income = income[cols].dropna()
    except:
        # If anything goes wrong we just return an empty dataframe so the rest of the app doesn't crash
        income = pd.DataFrame()
    return info, income


# st.stop() halts the script so nothing below this line runs if no ticker was picked
if len(all_tickers) == 0:
    st.info("Type a stock ticker above to get started.")
    st.stop()


# The data for each ticker is in a dict, the key is the ticker and the value is the tuple returned by get_stock_data
stock_data = {}
for t in all_tickers:
    # If yahoo can't find a ticker we show an error message but continue with the other valid tickers
    try:
        stock_data[t] = get_stock_data(t)
    except:
        st.error("Could not find data for " + t + ". Check the ticker symbol.")
# If none of the tickers worked, there is nothing to display so we stop here
if len(stock_data) == 0:
    st.stop()
st.divider()

# Section 1: company header and current price

# We make as many columns as we have stocks, so each stock gets its own header card
header_cols = st.columns(len(stock_data))
# We need a counter i to know which column to put each stock into
i = 0
for ticker in stock_data:
    info, _ = stock_data[ticker]
    with header_cols[i]:
        st.subheader(ticker)
        st.write("**" + str(info.get("longName", ticker)) + "**")
        price = info.get("currentPrice")
        currency = info.get("currency", "USD")
        # We only display the price if we actually have one (not None)
        # st.metric shows a value with a colored delta below it (green/red)
        if price is not None:
            st.metric("Current Price", currency + " " + str(round(price, 2)),
                      str(round(info.get("change", 0) * 100, 2)) + "%")
    i = i + 1
st.divider()

# Section 2: key financail metrics table

st.subheader("Key Financial Metrics")
# Dictionary that translates yahoo's API keys into readable labels for the table
metrics = {
    "currentPrice": "Price", "trailingPE": "P/E Ratio", "priceToBook": "Price / Book",
    "profitMargins": "Profit Margin", "operatingMargins": "Operating Margin",
    "revenueGrowth": "Revenue Growth", "returnOnEquity": "ROE",
    "returnOnAssets": "ROA", "trailingEps": "EPS", "enterpriseToEbitda": "EV / EBITDA",
}
# Keys whose values are decimals so we know to multiply them by 100 and add a % 
percent_keys = ["profitMargins", "operatingMargins", "revenueGrowth",
                "returnOnEquity", "returnOnAssets"]

# Build a table with one column per stock
table_data = {"Metric": list(metrics.values())}
for ticker in stock_data:
    info, _ = stock_data[ticker]
    currency = info.get("currency", "USD")
    # Values is a list with one entry per metric for this stock
    values = []
    for key in metrics:
        val = info.get(key)
        # If the value is missing we show "N/A" instead of crashing
        if val is None:
            values.append("N/A")
        # Special case: the price is shown with the currency symbol
        elif key == "currentPrice":
            values.append(currency + " " + str(round(val, 2)))
        # Floats get rounded for readability and we add % for percentages
        elif isinstance(val, float):
            if key in percent_keys:
                values.append(str(round(val * 100, 1)) + "%")
            else:
                values.append(str(round(val, 2)))
        else:
            # For anything else we just convert to a string
            values.append(str(val))
    table_data[ticker] = values

# We turn the dict into a dataframe and set "Metric" as the row index so the metric names show up as labels on the left 
st.dataframe(pd.DataFrame(table_data).set_index("Metric"), use_container_width=True)
st.divider()

# Section 3: price and metrics charts

st.subheader("Charts")
st.markdown("#### Price History")


# Let the user pick a time period on an horizontal radio, then map it to the lowercase code yfinance wants
period = st.radio("Select period:", ["YTD", "1Y", "5Y", "10Y", "Max"], horizontal=True)
period_map = {"YTD": "ytd", "1Y": "1y", "5Y": "5y", "10Y": "10y", "Max": "max"}


# Function is cached separately so changing the time period only gets the price history, not the PnL statement and key stats
@st.cache_data(ttl=300, show_spinner=False)
def get_price_history(ticker, period):
    """Fetch closing price history for one stock over the given period"""
    return yf.Ticker(ticker).history(period=period)


# Get price history for every stock, with the right period
all_prices = {}
for ticker in stock_data:
    h = get_price_history(ticker, period_map[period])
    if not h.empty:
        all_prices[ticker] = h


# Price data for the charts: native currency or change by % if there is more than 1 stock
# Plotly is used instead of matplotlib because its charts are interactive and work well in streamlit
show_percent = len(all_prices) > 1
# px.line() creates an empty plotly line chart that we then add traces to
price_fig = px.line()
for ticker in all_prices:
    h = all_prices[ticker]
    if show_percent:
        # Divide every closing price by the first day's price to get the % change
        y_values = (h["Close"] / h["Close"].iloc[0] - 1) * 100
    else:
        y_values = h["Close"]
    # Each call to add_scatter adds a new line to the chart
    price_fig.add_scatter(x=h.index, y=y_values, name=ticker, mode="lines")


# Pick the right axis label and title depending on whether we're showing % change or actual prices
if show_percent:
    y_label, chart_title = "Change (%)", "Stock Price (% change from start of period)"
else:
    # When there's only one stock we use its native currency on the y-axis
    only_ticker = list(all_prices.keys())[0]
    info, _ = stock_data[only_ticker]
    currency = info.get("currency", "USD")
    y_label, chart_title = "Price (" + currency + ")", "Stock Price"

# update_layout is plotly's way to set chart-wide options like axis titles
# hovermode="x unified" means hovering shows all stocks values for that date at once
price_fig.update_layout(title=chart_title, xaxis_title="Date", yaxis_title=y_label,
                        hovermode="x unified", legend_title="Stock")
# use_container_width=True makes the chart fill the available horizontal space
st.plotly_chart(price_fig, use_container_width=True)
st.divider()


# Charts for the Revenue, EBITDA and Net Income for the last 5 years
st.markdown("#### Financials (Last 5 Years)")


def clean_income(df):
    """Keep only annual data, last 5 years, one row per year"""
    # Check to not crash: if the dataframe is empty we just return it like that
    if df.empty:
        return df
    # Copy first because modifying the original could break the cache/other parts of the app that use the dataframe
    df = df.copy()
    # Extract just the year from the asOfDate column for easier grouping
    df["Year"] = pd.to_datetime(df["asOfDate"]).dt.year
    # sorted() sorts ascending, [-5:] takes the last 5 elements
    last_5 = sorted(df["Year"].unique())[-5:]
    df = df[df["Year"].isin(last_5)]
    # drop_duplicates keeps only one row per year because yahoo could returns multiple rows for the same year
    return df.drop_duplicates(subset="Year", keep="last")


def draw_grouped_bars(metric_name, y_label, title):
    """Grouped bar chart for one metric across all stocks with currency shown"""
    fig = px.bar(title=title)
    # has_data tracks whether we found any stock with data for this metric
    # if all stocks are missing it, we show a message instead of an empty chart
    has_data = False
    for ticker in stock_data:
        info, income = stock_data[ticker]
        # Only add bars for stocks that actually have this metric
        if not income.empty and metric_name in income.columns:
            clean = clean_income(income)
            currency = info.get("currency", "USD")
            # Year as string makes plotly treat it as a category (4 separate bars)
            # Dividing by 1e9 converts to billions for cleaner numbers on the axis
            fig.add_bar(x=clean["Year"].astype(str),
                        y=clean[metric_name] / 1e9,
                        name=ticker + " (" + currency + ")")
            has_data = True
    if not has_data:
        st.write("No data available for " + title)
        return
    # barmode="group" puts the bars side by side per year instead of stacked
    fig.update_layout(yaxis_title=y_label, xaxis_title="Year",
                      barmode="group", legend_title="Stock")
    st.plotly_chart(fig, use_container_width=True)


# Call to display two charts side by side (Revenue + EBITDA) and Net Income full width below
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown("##### Revenue")
    draw_grouped_bars("TotalRevenue", "Revenue (Billions, native currency)",
                      "Annual Revenue (Last 5Y)")
with chart_col2:
    st.markdown("##### EBITDA")
    draw_grouped_bars("EBITDA", "EBITDA (Billions, native currency)",
                      "Annual EBITDA (Last 5Y)")
st.markdown("##### Net Income")
draw_grouped_bars("NetIncome", "Net Income (Billions, native currency)",
                  "Annual Net Income (Last 5Y)")


# Section 4: 1-year price forecast (single stock)


# Score the company on 4 fundamentals (P/E count twice) to adjust the forecast
def score_fundamentals(info):
    """Return (score in -1..+1, breakdown dict) and none values are skipped"""
    # Each rule says: how to score one fundamental
    # - label: name shown in the breakdown
    # - value: actual value of this metric for the stock
    # - neutral: the value we consider average (gets a score of 0)
    # - half: how much above/below neutral counts as a full +1 or -1
    # - weight: how much this metric counts in the final average (P/E counts double)
    # - flip: if True, lower is better (low P/E is good, low margin is bad)
    rules = [
        ("P/E",    info.get("trailingPE"),     20,   20,   2, True),
        ("Margin", info.get("profitMargins"),  0.10, 0.15, 1, False),
        ("ROE",    info.get("returnOnEquity"), 0.15, 0.15, 1, False),
        ("Growth", info.get("revenueGrowth"),  0.05, 0.15, 1, False),
    ]
    # We accumulate a weighted total and the sum  so we can compute a weighted average at the end
    total, weights, breakdown = 0, 0, {}
    for name, val, neutral, half, weight, flip in rules:
        # If yahoo didn't return this metric we just skip it
        if val is None:
            continue
        # Distance from neutral, scaled by half-width
        s = (val - neutral) / half
        if flip:
            s = -s
        # Keep the score between -1 and +1 for extreme values
        if s > 1:
            s = 1
        if s < -1:
            s = -1
        breakdown[name] = s
        total += s * weight
        weights += weight
    # If all metrics were missing return a neutral 0 so it doesn't change anything
    if weights == 0:
        return 0, breakdown
    return total / weights, breakdown


def trend_forecast(ticker, info):
    """Train 3 models on 10y log-prices, pick the best on a test set and forecast 1 year"""
    # Get 10 years of price history (or whatever is available for newer stocks)
    hist = get_price_history(ticker, "10y")
    # We need at least 100 data points to train a meaningful model
    if hist.empty or len(hist) < 100:
        return None
    # .values turns the pandas series into a plain numpy array, which sklearn prefers
    prices = hist["Close"].values
    dates = pd.Series(hist.index).values
    n = len(prices)

    # Features are day numbers and .reshape(-1, 1) makes it a column instead of a row, which sklearn expects
    X = np.array(range(n)).reshape(-1, 1)
    # We model the log of prices instead of prices because percentage changesare more naturally additive than absolute changes
    y = np.log(prices)

    # Chronological (because of the nature of stock data) train/test split: first 80% for training, last 20% for evaluation
    # And we can't shuffle stock data like normal ML data because it's a time series
    cut = int(n * 0.8)
    X_train, X_test = X[:cut], X[cut:]
    y_train, y_test = y[:cut], y[cut:]

    # We don't know in advance which model fits best so we try three:
    # - Linear Regression: simple straight line
    # - Polynomial: a curve that can bend (good for accelerating growth)
    # - Huber: like linear regression but more robust to extreme outliers
    candidates = {
        "Linear Regression": LinearRegression(),
        "Polynomial (deg 2)": make_pipeline(PolynomialFeatures(2), LinearRegression()),
        "Huber": HuberRegressor(),
    }
    # We train each model and measure how good it is using MAPE
    results = {}
    for name, m in candidates.items():
        m.fit(X_train, y_train)
        # np.exp() reverses the np.log() we did earlier, so we compare in real prices
        # then we compute the average absolute % error vs the actual prices
        test_mape = (np.abs(prices[cut:] - np.exp(m.predict(X_test)))
                     / prices[cut:]).mean() * 100
        results[name] = test_mape

    # We loop through and keep track of the best one we've seen so far
    # the float("inf") starting value makes sure any real number beats it
    best_name, mape = None, float("inf")
    for name in results:
        if results[name] < mape:
            best_name, mape = name, results[name]
    model = candidates[best_name]

    # Comparison simpel baseline that assume price stays flat at the last training value
    baseline_pred = np.full(len(y_test), prices[cut - 1])
    baseline_mape = (np.abs(prices[cut:] - baseline_pred) / prices[cut:]).mean() * 100

    # Refit the chosen model on the entire history before forecasting the future
    model.fit(X, y)

    # Forecast the next 365 days and anchor day 1 to today's price for a smooth chart
    future_X = np.array(range(n, n + 365)).reshape(-1, 1)
    raw = np.exp(model.predict(future_X))
    last_price = prices[-1]
    trend_pred = raw * (last_price / raw[0])

    # We compute the predicted growth rate (0.15 = 15% return over 1 year)
    trend_growth = trend_pred[-1] / last_price - 1
    score, breakdown = score_fundamentals(info)
    # Good fundamentals add up to +10 percentage points, bad ones subtract up to 10.
    adj_growth = trend_growth + score * 0.10
    if trend_growth != 0:
        # Smooth scaling curve so the adjusted forecast slowly diverges from the trend forecast over the year
        scale = (1 + adj_growth) / (1 + trend_growth)
        curve = 1 + (scale - 1) * np.arange(1, 366) / 365
        adj_pred = trend_pred * curve
    else:
        adj_pred = trend_pred

    # Real forecasts get more uncertain the further into the future they look so we use ~2 standard deviations of past errors which covers ~95% of cases
    # sqrt(time) growth comes from random walk math: daily ups and downs partially cancel, so uncertainty grows more slowly than linear time
    log_unc = 2 * (y - model.predict(X)).std() * np.sqrt(np.arange(1, 366) / n)
    last_date = pd.Timestamp(dates[-1])
    # Build a list of future dates, one per day for the next year
    future_dates = []
    for i in range(1, 366):
        future_dates.append(last_date + pd.Timedelta(days=i))

    # We return everything as a dictionary so the calling code can pick out just what it needs by name 
    return {
        "prices": prices, "dates": dates, "last_price": last_price,
        "future_dates": future_dates, "trend_pred": trend_pred, "adj_pred": adj_pred,
        "upper": adj_pred * np.exp(log_unc), "lower": adj_pred * np.exp(-log_unc),
        "trend_growth": trend_growth, "adj_growth": adj_growth,
        "score": score, "breakdown": breakdown, "mape": mape,
        "baseline_mape": baseline_mape, "best_model": best_name,
        "all_results": results,
    }


# The whole chart section for a single stock
if len(stock_data) == 1:
    st.divider()
    st.subheader("1-Year Price Forecast")
    # st.info shows a blue info box that explains what we're doing to the user
    st.info(
        "We compare 3 models (Linear Regression, Polynomial, Huber Regressor) on a "
        "chronological train/test split (8 years train, 2 years test) and keep the best one. "
        "The forecast is then adjusted by current fundamentals "
    ) 

    # list(stock_data.keys())[0] gets the first (and only) ticker from our dict
    only_ticker = list(stock_data.keys())[0]
    info, _ = stock_data[only_ticker]
    currency = info.get("currency", "USD")
    f = trend_forecast(only_ticker, info)

    # If the forecast returned None it means there wasn't enough history
    if f is None:
        st.warning("Not enough price history available to train a model.")
    else:
        # Show model comparison: best model vs simple baseline
        st.write("**Best model:** " + f["best_model"])
        # Two columns side by side for the model error vs baseline error
        m1, m2 = st.columns(2)
        # A positive improvement means our model is better than the baseline
        improvement = f["baseline_mape"] - f["mape"]
        if improvement >= 0:
            delta_text = "+" + str(round(improvement, 1)) + "% vs baseline"
        else:
            delta_text = str(round(improvement, 1)) + "% vs baseline"
        m1.metric("Best model MAPE (test set)",
                str(round(f["mape"], 1)) + "%",
                delta=delta_text)
        m2.metric("Naive baseline MAPE", str(round(f["baseline_mape"], 1)) + "%")

        # We build a list of strings showing all 3 models and their errors so the user can see the full comparison
        all_results_str = []
        for k, v in f["all_results"].items():
            all_results_str.append(k + " " + str(round(float(v), 1)) + "%")
        st.caption(
            "MAPE = average % error on the last 20% of price history. "
            "Baseline = predict today's price stays unchanged. "
            "All models tested: " + ", ".join(all_results_str)
        )

        # We layer 5 things on the chart: history, upper band, lower band,trend forecast, and adjusted forecast
        fig = px.line(title=only_ticker + " - 1-Year Price Forecast")
        # The historical price line in blue
        fig.add_scatter(x=f["dates"], y=f["prices"], name="Historical",
                        mode="lines", line=dict(color="#1f77b4"))
        # Upper bound is invisible (width=0, hidden from legend) but plotly needs it as a reference for the fill area
        fig.add_scatter(x=f["future_dates"], y=f["upper"], name="Upper",
                        mode="lines", line=dict(width=0), showlegend=False)
        # fill="tonexty" fills the area between this line and the previous trace, creating the orange confidence band
        fig.add_scatter(x=f["future_dates"], y=f["lower"], name="Confidence band",
                        mode="lines", line=dict(width=0),
                        fill="tonexty", fillcolor="rgba(255,165,0,0.2)")
        # The dashed grey line shows what the model predicts based purely on the trend
        fig.add_scatter(x=f["future_dates"], y=f["trend_pred"], name="Trend only",
                        mode="lines", line=dict(color="gray", dash="dot", width=1))
        # The orange dashed line shows the trend after fundamentals adjustment
        fig.add_scatter(x=f["future_dates"], y=f["adj_pred"], name="Adjusted forecast",
                        mode="lines", line=dict(color="orange", dash="dash"))
        fig.update_layout(xaxis_title="Date", yaxis_title="Price (" + currency + ")",
                          hovermode="x unified", legend_title="Series")
        st.plotly_chart(fig, use_container_width=True)

        # Quick visual summary of price, prediction and fundamental adjusted prediction.
        c1, c2, c3 = st.columns(3)
        c1.metric("Current Price", currency + " " + str(round(f["last_price"], 2)))
        c2.metric("Trend prediction",
                  currency + " " + str(round(f["trend_pred"][-1], 2)),
                  str(round(f["trend_growth"] * 100, 1)) + "%")
        c3.metric("Fundamentals adjusted prediction",
                  currency + " " + str(round(f["adj_pred"][-1], 2)),
                  str(round(f["adj_growth"] * 100, 1)) + "%")


# When comparing multiple stocks we don't show all the model details, we just want a clean side-by-side view of expected returns
if len(stock_data) > 1:
    st.divider()
    st.subheader("1-Year Forecast Comparison (% change)")
    st.info(
        "Same forecast as the single stock view, run on each stock. "
        "We show % change from today so stocks at different price levels are comparable."
    )

    # Building the chart, we use percentage change from today on the y-axis 
    fig = px.line(title="1-Year Forecast - % change from today")
    # Rows accumulates the data we'll show in the summary table below the chart
    rows = []
    for ticker in stock_data:
        info, _ = stock_data[ticker]
        f = trend_forecast(ticker, info)
        # Skip any stock where the forecast couldn't be computed
        if f is None:
            continue
        currency = info.get("currency", "USD")
        # Convert the predicted price series to percent change from today
        pct = (f["adj_pred"] / f["last_price"] - 1) * 100
        fig.add_scatter(x=f["future_dates"], y=pct, name=ticker, mode="lines")
        # We append a dict with one row of summary info for this stock that we'll turn into a table at the end
        rows.append({
            "Stock": ticker,
            "Current": currency + " " + str(round(f["last_price"], 2)),
            "Best Model": f["best_model"],
            "Test MAPE": str(round(f["mape"], 1)) + "%",
            "Trend": str(round(f["trend_growth"] * 100, 1)) + "%",
            "Fundamentals Adjusted": str(round(f["adj_growth"] * 100, 1)) + "%",
        })

    fig.update_layout(xaxis_title="Date", yaxis_title="Change from today (%)",
                      hovermode="x unified", legend_title="Stock")
    st.plotly_chart(fig, use_container_width=True)
    # Only show the summary table if we actually have rows in it
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
