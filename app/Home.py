#This is the Homepage of our Website. From here our users can navigate to 
#all our other features by clicking on the buttons below the titles

#The layout of the files in the folder creates also a navigator througout the entire website


#this imports streamlit into the program
import streamlit as st

#page configuration and titles
st.set_page_config(layout="wide")

st.title("Homepage Easy Investing")

st.info("Welcome!")


#This is a little monopoly man winking his eye
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

# Layout with columns and themes for basic overview and understanding of our website
col1, col2, col3, col4, col5 = st.columns(5) 

with col1:
    st.subheader("Basics")
    st.write("Understand the fundamentals of investing")


with col2:
    st.subheader("Analyzer")
    st.write("Create and analyze your portfolio")


with col3:
    st.subheader("Comparator")
    st.write("Compare stocks")


with col4:
    st.subheader("News")
    st.write("Stay updated with latest News")



with col5:
    st.subheader("Profile")
    st.write("Find your investor profile!")




#Here are the buttons that allow the anvigation between the different pages of our website. 

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
    st.page_link("pages/2_Analyzer.py", label="Go to Analyzer")

with col3:
    st.page_link("pages/3_Comparator.py", label="Go to Comparator")

with col4:
    st.page_link("pages/4_News.py", label="Go to News")

with col5:
    st.page_link("pages/5_Profile.py", label="Go to Profile")


st.divider()

st.info("Use the sidebar or click on the buttons")
