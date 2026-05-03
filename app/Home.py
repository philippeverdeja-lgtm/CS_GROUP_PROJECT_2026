"""
This code is part of the Computer Science Project of group 11.05:
Philippe Verdeja, Yannick Hafner, Remi de la Fortelle, Mara Ciglia and Sam Pellaud.
It contains the "Homepage" of the website, with five sections describing each page and matching navigation buttons.
The idea is to give the user a clear entry point that explains what every part of the website does.
On top of that, the user can jump to any page either through these buttons or through the streamlit sidebar.
"""

# This imports streamlit into the program
import streamlit as st

# Page configuration, title, subtitle and tab icon (logo without text)
# Logo and tab icon by Claude
st.set_page_config(
    page_title="Easy Investing",
    page_icon="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjAgMzYwIj48cmVjdCB3aWR0aD0iMzYwIiBoZWlnaHQ9IjM2MCIgcng9IjUwIiBmaWxsPSIjMGQxYjJhIi8+PHJlY3QgeD0iNjAiIHk9IjE4MCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjE1MCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIxNTIiIHk9IjIzMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjEwMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB4PSIyNDQiIHk9IjEyMCIgd2lkdGg9IjU1IiBoZWlnaHQ9IjIxMCIgcng9IjQiIGZpbGw9IiNmZmZmZmYiLz48cG9seWxpbmUgcG9pbnRzPSIzNSwyNjAgODcuNSwxODAgMTc5LjUsMjMwIDI4NSwxMDgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzFmOGZmZiIgc3Ryb2tlLXdpZHRoPSIxNCIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjg1LDEwOCkgcm90YXRlKC00MS42MykiPjxwb2x5Z29uIHBvaW50cz0iLTI2LC0yMiAyMiwwIC0yNiwyMiIgZmlsbD0iIzFmOGZmZiIgc3Ryb2tlPSIjMWY4ZmZmIiBzdHJva2Utd2lkdGg9IjYiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L2c+PC9zdmc+",
    layout="wide"
)
st.title("Homepage Easy Investing")
st.info("Welcome!")

# Adds the logo of our website at the top right corner
st.markdown("""
    <style>
    .easy-investing-logo {
        position: fixed;
        top: 60px;
        right: 20px;
        width: 130px;
        z-index: 9999;
    }
    </style>
    <div class="easy-investing-logo">
        <svg viewBox="0 0 680 500" xmlns="http://www.w3.org/2000/svg">
            <rect x="160" y="40" width="360" height="360" rx="50" fill="#0d1b2a"/>
            <rect x="220" y="220" width="55" height="150" rx="4" fill="#ffffff"/>
            <rect x="312" y="270" width="55" height="100" rx="4" fill="#ffffff"/>
            <rect x="404" y="160" width="55" height="210" rx="4" fill="#ffffff"/>
            <polyline points="195,300 247.5,220 339.5,270 445,148"
                      fill="none" stroke="#1f8fff" stroke-width="14"
                      stroke-linecap="round" stroke-linejoin="round"/>
            <g transform="translate(445,148) rotate(-41.63)">
                <polygon points="-26,-22 22,0 -26,22" fill="#1f8fff"
                         stroke="#1f8fff" stroke-width="6" stroke-linejoin="round"/>
            </g>
            <text x="340" y="465" font-size="58" font-weight="800"
                  text-anchor="middle" letter-spacing="-1"
                  font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">
                <tspan fill="#1f8fff">Easy</tspan><tspan fill="#ffffff"> Investing</tspan>
            </text>
        </svg>
    </div>
""", unsafe_allow_html=True)

# Divider for layout
st.divider()

# Layout with columns and themes for basic overview and understanding of our website
col1, col2, col3, col4, col5 = st.columns(5) 
with col1:
    st.subheader("Basics")
    st.write("Understand the fundamentals of investing")
with col2:
    st.subheader("Portfolio Allocation")
    st.write("Create and analyze your portfolio")
with col3:
    st.subheader("Comparator")
    st.write("Compare stocks and financial data")
with col4:
    st.subheader("News")
    st.write("Stay updated with latest News")
with col5:
    st.subheader("Profile")
    st.write("Find your investor profile!")

# Here are the buttons that allow the navigation between the different pages of our website.
st.markdown("""
    <style>
    .stPageLink button {
        background-color: #FF6B6B !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.page_link("pages/1_Basics.py", label="Go to Basics")
with col2:
    st.page_link("pages/2_Portfolio Allocation.py", label="Go to Analyzer")
with col3:
    st.page_link("pages/3_Comparator.py", label="Go to Comparator")
with col4:
    st.page_link("pages/4_News.py", label="Go to News")
with col5:
    st.page_link("pages/5_Profile.py", label="Go to Profile")

st.divider()

st.info("Use the sidebar or click on the buttons")
