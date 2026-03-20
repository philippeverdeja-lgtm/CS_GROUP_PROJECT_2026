
# import modules, also put them in requirements
import streamlit as st
from yahooquery import Ticker

# title of the website
st.title("Stock Comparator - CS_GRPOUP_PROJECT_2026_11.5")



#text inputs for tickers
ticker1 = st.text_input("First stock (e.g. AAPL)")
ticker2 = st.text_input("Second stock (e.g. MSFT)")


#from chatGPT cache function --> saves results for 10 min (600 sec), if not 
#every refresh is a new call, crashed often before
@st.cache_data(ttl=60)

#definition of function
def get_stock_info(ticker):

    
    ticker = ticker.upper() #all upercase tickers now

    #creates yahoo finance object for this stock, does not call the data yet
    #but creates the "interface"
    t = Ticker(ticker)

    #get.ticekr gets my data
    financial_data = t.financial_data.get(ticker, {}) #t.financial_data 


    key_stats = t.key_stats.get(ticker, {}) # ratios evaluations


    summary_detail = t.summary_detail.get(ticker, {}) #market data


        #combines dictionaries into one (Chat gpt)
    return {**financial_data, **key_stats, **summary_detail}


#only run program if both inputs exist
if ticker1 and ticker2:

    #put the the ticker in the definition get_stock_info and gets all the data from yahooquery
    #this is where the program calls the informations
    stock1 = get_stock_info(ticker1)

    stock2 = get_stock_info(ticker2)

         #UX two columns
    
    
    col1, col2 = st.columns(2)


        #column one 
        #ticker 1 from input 1 gets in the header
    with col1:
        st.header(ticker1.upper())
        #stock1 this is where the program recalls the infromations it already has from get_stock_info and
        #now only calls some elements from it 
        st.write("Profit Margin:", stock1.get("profitMargins"))
        st.write("Revenue Growth:", stock1.get("revenueGrowth"))
        st.write("Return on Equity:", stock1.get("returnOnEquity"))
        st.write("P/E Ratio:", stock1.get("trailingPE"))
        st.write("EPS:", stock1.get("trailingEps"))
        st.write("Price/Book:", stock1.get("priceToBook"))
        st.write("EV/EBITDA:", stock1.get("enterpriseToEbitda"))
        st.write("EBITDA:", stock1.get("ebitda"))


    #same as with col1
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