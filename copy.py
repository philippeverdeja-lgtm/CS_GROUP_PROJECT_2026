# import modules, also put them in requirements
import streamlit as st
import pandas as pd
from yahooquery import Ticker



st.set_page_config(layout="wide")
# title of the website
st.title("Stock Comparator - CS_GRPOUP_PROJECT_2026_11.5")

#text inputs for tickers




col1, col2, col3, col4 = st.columns(4)

with col1:
    ticker1 = st.text_input("First stock (e.g. AAPL)")

with col2:
    ticker2 = st.text_input("Second stock (e.g. MSFT)")

with col3:
    ticker3 = st.text_input("Third stock (e.g. GOOG)")

with col4:
    ticker4 = st.text_input("Fourth stock (e.g. AMZN)")


#from chatGPT cache function --> saves results for 10 min (600 sec), if not 
#every refresh is a new call, crashed often before
@st.cache_data(ttl=100)

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

    price_data = t.price.get(ticker,{})


    long_name = price_data.get("longName") or ticker

    #combines dictionaries into one
    stock_info = {**financial_data, **key_stats, **summary_detail}
    stock_info["longName"] = long_name

    return stock_info


#only run program if both inputs exist
if ticker1 or ticker2 or ticker3 or ticker4:

    #put the the ticker in the definition get_stock_info and gets all the data from yahooquery
    #this is where the program calls the informations

    if ticker1:
        stock1 = get_stock_info(ticker1)
    else:
        stock1 = {}

    if ticker2:
        stock2 = get_stock_info(ticker2)
    else:
        stock2 = {}
    
    if ticker3:
        stock3 = get_stock_info(ticker3)
    else:
        stock3 = {}

    if ticker4:
        stock4 = get_stock_info(ticker4)
    else:
        stock4 = {}

    col1, col2, col3, col4 = st.columns(4)


        #column one 
        #ticker 1 from input 1 gets in the header


    with col1:
        st.subheader(ticker1.upper())
        #stock1 this is where the program recalls the infromations it already has from get_stock_info and
        #now only calls some elements from it

        name1 = stock1.get("longName") or ticker1.upper()
        st.subheader(name1)

        price1 = stock1.get("currentPrice")
        st.subheader(f"Stock Price: {price1}") 

        pm1 = stock1.get("profitMargins")
        st.markdown(f"##### Profit Margins: {pm1}")

        rg1 = stock1.get("revenueGrowth")
        st.markdown(f"##### Revenue Growth: {rg1}")

        roe1 = stock1.get("returnOnEquity")
        st.markdown(f"##### ROE: {roe1}")

        pe1 = stock1.get("trailingPE")
        st.markdown(f"##### P/E: {pe1}")

        eps1 = stock1.get("trailingEPS")
        st.markdown(f"##### EPS: {eps1}")

        pb1 = stock1.get("priceToBook")
        st.markdown(f"##### Price/Book: {pb1}")

        evebitda1 = stock1.get("entrepriseToEbitda")
        st.markdown(f"##### EV/EBITDA: {evebitda1}")

        ebitda1 = stock1.get("ebitda")
        st.markdown(f"##### EBITDA: {ebitda1}")
      

    #same as with col1
    with col2:
        st.subheader(ticker2.upper())

        name2 = stock2.get("longName") or ticker2.upper()
        st.subheader(name2)

        price2 = stock2.get("currentPrice")
        st.subheader(f"Stock Price: {price2}")

        pm2 = stock2.get("profitMargins")
        st.markdown(f"##### Profit Margin: {pm2}")

        rg2 = stock2.get("revenueGrowth")
        st.markdown(f"##### Revenue Growth: {rg2}")

        roe2 = stock2.get("returnOnEquity")
        st.markdown(f"##### ROE: {roe2}")

        pe2 = stock2.get("trailingPE")
        st.markdown(f"##### P/E: {pe2}")

        eps2 = stock2.get("trailingEPS")
        st.markdown(f"##### EPS: {eps2}")

        pb2 = stock2.get("priceToBook")
        st.markdown(f"##### Price/Book: {pb2}")

        evebitda2 = stock2.get("entrepriseToEbitda")
        st.markdown(f"##### EV/EBITDA: {evebitda2}")

        ebitda2 = stock2.get("ebitda")
        st.markdown(f"##### EBITDA: {ebitda2}")


    with col3:
        
        st.subheader(ticker3.upper())

        name3 = stock3.get("longName") or ticker3.upper()
        st.subheader(name3)

        price3 = stock3.get("currentPrice")
        st.subheader(f"Stock Price: {price3}")

        pm3 = stock3.get("profitMargins")
        st.markdown(f"##### Profit Margin: {pm3}")

        rg3 = stock3.get("revenueGrowth")
        st.markdown(f"##### Revenue Growth: {rg3}")

        roe3 = stock3.get("returnOnEquity")
        st.markdown(f"##### ROE: {roe3}")

        pe3 = stock3.get("trailingPE")
        st.markdown(f"##### P/E: {pe3}")

        eps3 = stock3.get("trailingEPS")
        st.markdown(f"##### EPS: {eps3}")

        pb3 = stock3.get("priceToBook")
        st.markdown(f"##### Price/Book: {pb3}")

        evebitda3 = stock3.get("entrepriseToEbitda")
        st.markdown(f"##### EV/EBITDA: {evebitda3}")

        ebitda3 = stock3.get("ebitda")
        st.markdown(f"##### EBITDA: {ebitda3}")


    with col4:
        st.subheader(ticker4.upper())

        name4 = stock4.get("longName") or ticker4.upper()
        st.subheader(name4)

        price4 = stock4.get("currentPrice")
        st.subheader(f"Stock Price: {price4}")

        pm4 = stock4.get("profitMargins")
        st.markdown(f"##### Profit Margin: {pm4}")

        rg4 = stock4.get("revenueGrowth")
        st.markdown(f"##### Revenue Growth: {rg4}")

        roe4 = stock4.get("returnOnEquity")
        st.markdown(f"##### ROE: {roe4}")

        pe4 = stock4.get("trailingPE")
        st.markdown(f"##### P/E: {pe4}")

        eps4 = stock4.get("trailingEPS")
        st.markdown(f"##### EPS: {eps4}")

        pb4 = stock4.get("priceToBook")
        st.markdown(f"##### Price/Book: {pb4}")

        evebitda4 = stock4.get("entrepriseToEbitda")
        st.markdown(f"##### EV/EBITDA: {evebitda4}")

        ebitda4 = stock4.get("ebitda")
        st.markdown(f"##### EBITDA: {ebitda4}")


    df = pd.DataFrame({
        'Indicators': ['Stock Price', 'Profit Margin', 'Revenue Growth', 'ROE', 'P/E Ratio', 'EPS', 'Price/Book', 'EV/EBITDA', 'EBITDA'],
        name1 : [price1, pm1, rg1, roe1, pe1, eps1, pb1, evebitda1, ebitda1],
        name2 : [price2, pm2, rg2, roe2, pe2, eps2, pb2, evebitda2, ebitda2],
        name3 : [price3, pm3, rg3, roe3, pe3, eps3, pb3, evebitda3, ebitda3],
        name4 : [price4, pm4, rg4, roe4, pe4, eps4, pb4, evebitda4, ebitda4] 
    })

    df = df.set_index('Indicators')

    st.dataframe(df)







col_left, col_center, col_right = st.columns(3)

with col_left:
    st.caption("Data from Yahoo Finance")