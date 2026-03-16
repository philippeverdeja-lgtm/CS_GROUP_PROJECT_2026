import yfinance as yf #import the yahoo finance module
import streamlit as st

st.title("Comparator of 2 stocks (CS_PROJECT_2)")

st.text_input("type in a first ticker")

stock = yf.Ticker(input("Type your first Ticker")) #type in the ticker of the first stock


info = stock.info


print("Name :", info.get("longName"))

print(f"Ticker: {stock.ticker}")

print("\nP/E Ratio :", info.get("trailingPE"))
print("Debt/Equity :", info.get("debtToEquity"))
print("ROE :", info.get("returnOnEquity"))
print("Free Cash Flow :", info.get("freeCashflow"))
print("Profit Margin :", info.get("profitMargins"))
print("EPS :", info.get("trailingEps"))
print("Revenue Growth :", info.get("revenueGrowth"))
print("Current Ratio :", info.get("currentRatio"))

print("\n-----------------------")

stock = yf.Ticker(input("second ticker")) #type in the ticker of the second stock



info = stock.info

print("\nName :", info.get("longName"))
print(f"Ticker: {stock.ticker}")

print("\nP/E Ratio:", info.get("trailingPE"))
print("Debt/Equity:", info.get("debtToEquity"))
print("ROE :", info.get("returnOnEquity"))
print("Free Cash Flow :", info.get("freeCashflow"))
print("Profit Margin :", info.get("profitMargins"))
print("EPS :", info.get("trailingEps"))
print("Revenue Growth :", info.get("revenueGrowth"))
print("Current Ratio :", info.get("currentRatio"))
print("-------------------------")


