import streamlit as st
import feedparser
import yfinance as yf
import pandas as pd
from datetime import datetime

st.sidebar.title("Morning Market Digest")

st.set_page_config(page_title="Morning Market Digest", layout="centered")

st.title("Morning Market Digest")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}") #date automatically updates every time the page loads

@st.cache_data(ttl=1800) #cache so that there aren't constant requests to the external websites and thus no risk of being blocked due to too high usage
def get_headlines():
    feeds=["https://www.cnbc.com/id/100727362/device/rss/rss.html"] #possibility of using multiple websites, but this one works well enough
    entries=[]
    for url in feeds:
        feed=feedparser.parse(url)
    return [(entry.title, entry.link) for entry in feed.entries[:6]] #takes the top 6 headlines and embeds the URL towards them on streamlit as well

def get_index_change(ticker):
    hist=yf.Ticker(ticker).history(period="5d") #looks at the last 5 days so that even if the market is closed over the weekend or holiday it works
    if len(hist)<2:
        return None, None
    prev=hist["Close"].iloc[-2]
    last=hist["Close"].iloc[-1]
    change=((last - prev) / prev) * 100
    return round(last, 2), round(change, 2) #so that the numbers show up with rounded decimals, I experimented with float but it's ugly

@st.cache_data(ttl=300) #main reason I used caches, since yfinance regularly crashes if one user calls upon it too much
def get_all_indices():
    tickers=["^GSPC", "^STOXX", "^HSI", "^N225", "^KS200"] #selection of biggest tickers, I tried MSCI world but it kept malfunctioning so I took it out
    data=yf.download(tickers, period="5d", group_by="ticker")
    results={}
    for ticker in tickers:
        try:
            df=data[ticker].dropna() #the dropna drops missing values from the downloaded tickers
            if len(df)<2:
                results[name]=(None, None)
                continue

            hist=data[ticker]
            prev=df["Close"].iloc[-2]
            last=df["Close"].iloc[-1]
            change=((last - prev) / prev)*100
            
            results[ticker]=(round(last, 2), round(change, 2))
        except:
            results[ticker]=(None, None)
    return results

def fmt_price(x): #ChatGPT did this, don't really know what it does tbh
    if x is None or pd.isna(x): 
        return "N/A"
    return f"{x:.2f}"

def fmt_change(x): #same here as for the part above
    if x is None or pd.isna(x):
        return "N/A"
    return f"{color} {x:.2f}%"

headlines=get_headlines()

results = get_all_indices()

sp500_price, sp500_change=results["^GSPC"]
eurostoxx600_price, eurostoxx600_change=results["^STOXX"]
HangSeng_price, HangSeng_change=results["^HSI"]
Nikkei225_price, Nikkei225_change=results["^N225"]
Kospi200_price, Kospi200_change=results["^KS200"]

st.subheader("Top News") #formatting

for title, link in headlines:
    st.markdown(f"- [{title}]({link})") #putting the markdown allows for nice bulletpoints and then we have the titles with their links displayed

st.subheader("Markets")

col1, col2, col3, col4, col5=st.columns(5) #five different columns, one for each ticker

with col1:
    st.metric("S&P 500", sp500_price, f"{sp500_change}%")

with col2:
    st.metric("EuroStoxx 600", eurostoxx600_price, f"{eurostoxx600_change}%")

with col3:
    st.metric("HangSeng Index", HangSeng_price, f"{HangSeng_change}%")

with col4:
    st.metric("Nikkei 225", Nikkei225_price, f"{Nikkei225_change}%")

with col5:
    st.metric("Kospi 200", Kospi200_price, f"{Kospi200_change}%")
