import streamlit as st
import yfinance as yf

st.title("Stock Comparator")

ticker1 = st.text_input("First stock (e.g. AAPL)")
ticker2 = st.text_input("Second stock (e.g. MSFT)")

if ticker1 and ticker2:
    stock1 = yf.Ticker(ticker1).info
    stock2 = yf.Ticker(ticker2).info

    if not isinstance(stock1, dict) or not isinstance(stock2, dict):
        st.error("One or both tickers could not be found.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.header(ticker1.upper())
            st.write("Profit Margin:", stock1.get("profitMargins"))
            st.write("Revenue Growth:", stock1.get("revenueGrowth"))
            st.write("Return on Equity:", stock1.get("returnOnEquity"))
            st.write("P/E Ratio:", stock1.get("trailingPE"))
            st.write("EPS:", stock1.get("trailingEps"))
            st.write("Price/Book:", stock1.get("priceToBook"))
            st.write("EV/EBITDA:", stock1.get("enterpriseToEbitda"))
            st.write("EBITDA:", stock1.get("ebitda"))

        with col2:
            st.header(ticker2.upper())
            st.write("Profit Margin:", stock2.get("profitMargins"))
            st.write("Revenue Growth:", stock2.get("revenueGrowth"))
            st.write("Return on Equity:", stock2.get("returnOnEquity"))
            st.write("P/E Ratio:", stock2.get("trailingPE"))
            st.write("EPS:", stock2.get("trailingEps"))
            st.write("Price/Book:", stock2.get("priceToBook"))
            st.write("EV/EBITDA:", stock2.get("enterpriseToEbitda"))
            st.write("EBITDA:", stock2.get("ebitda"))

