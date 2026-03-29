import streamlit as st
import pandas as pd
from yahooquery import Ticker

col1, col2, col3, col4 = st.columns (4)

with col1:
    stock1 = st.text_input("first ticker")


df = pd.DataFrame({
    'Ticker': [stock1, 'MSFT'],
    'Price': [150, 300]
})

st.dataframe(df)