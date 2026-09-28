
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

st.title("Live Crypto Trading Dashboard")

# Live Data Fetch
crypto = st.selectbox('Select Crypto', ['BTC-USD', 'ETH-USD', 'SOL-USD'])
data = yf.download(crypto, period='1mo', interval='1d')

# Simple Moving Average
data['SMA_20'] = ta.sma(data['Close'], length=20)

st.line_chart(data[['Close', 'SMA_20']])
