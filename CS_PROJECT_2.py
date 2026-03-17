import streamlit as st
from yahooquery import Ticker

st.title("Stock Comparator")

ticker1 = st.text_input("First stock (e.g. AAPL)")
ticker2 = st.text_input("Second stock (e.g. MSFT)")

if ticker1 and ticker2:
    stock1 = Ticker(ticker1).financial_data[ticker1.upper()]
    stock2 = Ticker(ticker2).financial_data[ticker2.upper()]

    col1, col2 = st.columns(2)

    with col1:
        st.header(ticker1.upper())
        st.write("Profit Margin:", stock1.get("profitMargins"))
        st.write("Revenue Growth:", stock1.get("revenueGrowth"))
        st.write("Return on Equity:", stock1.get("returnOnEquity"))

    with col2:
        st.header(ticker2.upper())
        st.write("Profit Margin:", stock2.get("profitMargins"))
        st.write("Revenue Growth:", stock2.get("revenueGrowth"))
        st.write("Return on Equity:", stock2.get("returnOnEquity"))