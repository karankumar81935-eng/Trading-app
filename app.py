 
import streamlit as st
import pandas as pd
import numpy as np

st.title("Crypto Trading Dashboard")
st.write("Real-time price & signals")

# Sample data for demonstration
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['BTC', 'ETH', 'SOL']
)
st.line_chart(chart_data)

