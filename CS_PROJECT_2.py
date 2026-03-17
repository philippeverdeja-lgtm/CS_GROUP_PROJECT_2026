import streamlit as st
from yahooquery import Ticker

st.title("Stock Comparator")

def get_data(symbol):
    t = Ticker(symbol.upper())
    data = t.summary_detail
    if isinstance(data, dict) and symbol.upper() in data:
        return data[symbol.upper()]
    return {}

def format_val(x):
    if isinstance(x, (int, float)):
        return round(x, 2)
    return "N/A"

t1 = st.text_input("Stock 1 (e.g. AAPL)")
t2 = st.text_input("Stock 2 (e.g. MSFT)")

if t1 and t2:
    d1 = get_data(t1)
    d2 = get_data(t2)

    metrics = {
        "P/E": "trailingPE",
        "Price/Book": "priceToBook",
        "Profit Margin": "profitMargins"
    }

    for name, key in metrics.items():
        col1, col2 = st.columns(2)
        col1.metric(name, format_val(d1.get(key)))
        col2.metric(name, format_val(d2.get(key)))