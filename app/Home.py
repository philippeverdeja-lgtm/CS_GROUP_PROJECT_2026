#this imports streamlit into the program
import streamlit as st

#page configuration wide
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    [data-testid="column"] {
        min-height: 250px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Homepage Easy Investing")

st.info("Welcome!")

st.markdown("""
    <style>
    .monopoly-man {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 150px;
        z-index: 9999;
    }
    </style>
    <img class="monopoly-man" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWtleW5nNnJqdjA1aW5hODRsZGhzZzE5ZTJpcHRydDR4ZDU0Z21qayZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/C8976bDqhEUk40i8XU/giphy.gif">
""", unsafe_allow_html=True)

#divider for layout
st.divider()

# Layout with columns and themes
col1, col2, col3, col4, col5 = st.columns(5) 

with col1:
    st.subheader("Basics")
    st.write("Fundamentals of investing")
    st.page_link("pages/1_Basics.py", label="Click here for Basics")

with col2:
    st.subheader("Analyzer")
    st.write("Create and analyze your portfolio")
    st.page_link("pages/2_Analyzer.py", label="Click here for Analyzer")

with col3:
    st.subheader("Comparator")
    st.write("Compare stocks and ETFs")
    st.page_link("pages/3_Comparator.py", label="Click here for Comparator")

with col4:
    st.subheader("News")
    st.write("Stay updated with latest information")
    st.page_link("pages/4_News.py", label="Click here for News")


with col5:
    st.subheader("Profile")
    st.write("Find your investor profile!")
    st.page_link("pages/1_Basics.py", label="Click here for Profile")


st.divider()

st.info("Use the sidebar to navigate between features")
