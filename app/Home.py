#this is the home page
import streamlit as st

st.set_page_config(
    page_title="CS Project App",
    page_icon="",
    layout="wide"
)

st.title("Homepage Easy Investing")

st.write("Welcome! Choose a feature from the sidebar")

st.divider()

# Layout with columns
col1, col2, col3, col4, col5 = st.columns(5) 

with col1:
    st.subheader("Basics")
    st.write("Fundamentals of investing")

with col2:
    st.subheader("Analyzer")
    st.write("Create and analyze your portfolio")

with col3:
    st.subheader("Comparator")
    st.write("Compare stocks and ETFs")

with col4:
    st.subheader("News")
    st.write("Stay updated with latest information")

with col5:
    st.subheader("Profile")
    st.write("Find your investor profile!")

st.divider()

st.info("Use the sidebar to navigate between features")
