import streamlit as st
import pandas as pd
from yahooquery import Ticker

df = pd.DataFrame({
    'Ticker': ['AAPL', 'MSFT'],
    'Price': [150, 300]
})