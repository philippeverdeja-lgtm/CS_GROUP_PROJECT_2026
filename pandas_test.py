import streamlit as st
import pandas as pd
from yahooquery import Ticker


st.set_page_config(layout="wide")

col1, col2, col3, col4 = st.columns (4)

with col1:
    stock1 = st.text_input("first ticker")

with col2:
    stock2 = st.text_input("Second ticker")

with col3:
    stock3 = st.text_input("Third ticker")

with col4:
    stock4 = st.text_input("Fourth ticker")

df = pd.DataFrame({
    'KPI': ['Price', 'Profit Margin', 'Revenur Growth', 'ROE'],
    stock1: ["price","pm", "rg", "ROE" ],
    stock2: ["price2", "pm2", "rg2", "ROE2"],
    stock3: ["price3", "pm3", "rg3", "ROE3"],
    stock4: ["price4", "pm4", "rg4", "ROE4"]
})

df = df.set_index('KPI')


st.dataframe(df)
