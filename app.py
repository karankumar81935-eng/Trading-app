
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

st.title("Live Crypto Dashboard with Signals")

crypto = st.selectbox('Select Crypto', ['BTC-USD', 'ETH-USD', 'SOL-USD'])
data = yf.download(crypto, period='1mo', interval='1d')

data['SMA_20'] = ta.sma(data['Close'], length=20)

# Signal Logic
data['Signal'] = 'Hold'
valid_data = data.dropna()
data.loc[valid_data[valid_data['Close'] > valid_data['SMA_20']].index, 'Signal'] = 'Buy'
data.loc[valid_data[valid_data['Close'] < valid_data['SMA_20']].index, 'Signal'] = 'Sell'

latest_signal = data['Signal'].iloc[-1]
st.write(f"Latest Signal: {latest_signal}")

st.line_chart(data[['Close', 'SMA_20']])

