#this is the home page
import streamlit as st

st.set_page_config(
    page_title="CS Project App",
    page_icon="",
    layout="wide"
)

st.title("CS Group Project 2026 - Easy Investing")

st.write("Welcome! Choose a feature from the sidebar")

st.divider()

# Layout with columns
col1, col2, col3, col4, col5 = st.columns(5) 

with col1:
    st.subheader("Financial Basics")
    st.write("Different tutorials and explanations around investing")

with col2:
    st.subheader("Analyzer")
    st.write("Analyze your data and get insights")

with col3:
    st.subheader("Stocks")
    st.write("Compare different datasets or results")

with col4:
    st.subheader("News")
    st.write("Stay updated with latest information")

with col5:
    st.subheader("Profile")
    st.write("Find your investor profile!")

st.divider()

st.info("Use the sidebar to navigate between features")
