import streamlit as st
from yahooquery import Ticker

st.title("Stock Comparator")

ticker1 = st.text_input("First stock (e.g. AAPL)")
ticker2 = st.text_input("Second stock (e.g. MSFT)")

if ticker1 and ticker2:
    t1 = Ticker(ticker1)
    t2 = Ticker(ticker2)

    stock1 = t1.financial_data[ticker1.upper()]
    stock2 = t2.financial_data[ticker2.upper()]

    # DEBUG - shows exactly what Yahoo is returning
    st.write("DEBUG stock1:", stock1)
    st.write("DEBUG stock2:", stock2)