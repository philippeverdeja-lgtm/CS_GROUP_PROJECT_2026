#this imports streamlit into the program
import streamlit as st

#page configuration wide
st.set_page_config(layout="wide")

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

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.page_link("pages/1_Basics.py", label="Go to Basics")

with col2:
    st.page_link("pages/2_Analyzer.py", label="Go to Analyzer")

with col3:
    st.page_link("pages/3_Comparator.py", label="Go to Comparator")

with col4:
    st.page_link("pages/4_News.py", label="Go to News")

with col5:
    st.page_link("pages/1_Basics.py", label="Go to Profile")

    

st.info("Use the sidebar to navigate between features")
