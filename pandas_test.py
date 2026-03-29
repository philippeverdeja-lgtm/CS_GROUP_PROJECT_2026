import streamlit as st
import pandas as pd
from yahooquery import Ticker

df = pd.DataFrame({
    'Ticker': [st.text_input("Insert Ticker"), 'MSFT'],
    'Price': [150, 300]
})

st.dataframe(df)