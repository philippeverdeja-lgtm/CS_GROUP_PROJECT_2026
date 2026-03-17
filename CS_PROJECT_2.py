
# import modules, also put them in requirements
import streamlit as st
from yahooquery import Ticker

# title of the website
st.title("Stock Comparator - CS_GRPOUP_PROJECT_2026_11.5")


#text inputs for tickers
ticker1 = st.text_input("First stock (e.g. AAPL)")
ticker2 = st.text_input("Second stock (e.g. MSFT)")


#from chatGPT cache function --> saves results for 10 min (600 sec), if not 
#every refresh is a new call
@st.cache_data(ttl=600)

#definition of function (Chat GPT)
def get_stock_info(ticker):

    #creates yahoo finance object for this stock
    t = Ticker(ticker)

    #ticker.upper --> every input is upper case letters
    financial_data = t.financial_data.get(ticker.upper(), {}) #probaility, margins


    key_stats = t.key_stats.get(ticker.upper(), {}) # ratios evaluations


    summary_detail = t.summary_detail.get(ticker.upper(), {}) #market data


        #combines dictionaries into one (Chat gpt)
    return {**financial_data, **key_stats, **summary_detail}


#only run program if both inputs exist
if ticker1 and ticker2:
    stock1 = get_stock_info(ticker1)
    stock2 = get_stock_info(ticker2)


        #UX two columns
    col1, col2 = st.columns(2)


        #column one 
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