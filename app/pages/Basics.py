import streamlit as st

# -----------------------------
# Finance App Tutorial Page
# -----------------------------

st.set_page_config(page_title="Finance Tutorial", page_icon="", layout="wide")

st.title("Welcome to Your Finance Basics Guide")
st.write("This page is designed to help beginners understand how the app works and the basic concepts of finance in a simple way.")

# -----------------------------
# What the app does
# -----------------------------

st.header("💡 What does this app do?")
st.write("""
This application helps you:
- Understand basic financial concepts
- Learn how investments grow over time
- Explore risk and return trade-offs
- Simulate simple financial scenarios
""")

# -----------------------------
# Basic finance concepts
# -----------------------------

st.header("📚 Basic Finance Concepts")

st.subheader("1. Money growth over time")
st.write("Money can grow when you invest it. The longer you leave it invested, the more it can grow.")

st.subheader("2. Interest")
st.write("Interest is the money you earn for lending your money or investing it.")

st.subheader("3. Compound Interest")
st.write("Compound interest means you earn interest on your initial money AND on the interest already earned. This is how wealth can grow faster over time.")

st.subheader("4. Risk and Return")
st.write("Higher potential returns usually come with higher risk. Safer investments usually grow more slowly.")

st.subheader("5. Diversification")
st.write("Diversification means spreading your money across different investments to reduce risk.")

# -----------------------------
# Financial instruments
# -----------------------------

st.header("🏦 Common Financial Instruments")

st.subheader("Stocks")
st.write("Stocks represent ownership in a company. If the company grows, your stock value may increase.")

st.subheader("Bonds")
st.write("Bonds are like loans you give to companies or governments. In return, they pay you interest.")

st.subheader("Cash / Savings")
st.write("Cash is the safest but usually grows the least over time.")

# -----------------------------
# Simple example
# -----------------------------

st.header("📈 Simple Example")
st.write("""
Imagine you invest 1,000 CHF:
- At 5% annual return
- For 10 years

Because of compound interest, your money grows faster over time, not just linearly.
""")

st.info("Tip: Time in the market is often more important than trying to time the market.")

# -----------------------------
# How to use the app
# -----------------------------

st.header("🧭 How to use this app")
st.write("""
1. Explore simulations (if available)
2. Adjust parameters like interest rate or time
3. Compare different investment scenarios
4. Learn by experimenting
""")

st.success("Start exploring and experimenting with different financial settings!")

