
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
 data.loc[data['Close'] > data['SMA_20'], 'Signal'] = 'Buy'
data.loc[data['Close'] < data['SMA_20'], 'Signal'] = 'Sell'.

data['Close'].values < data['SMA_20'].values

latest_signal = data['Signal'].iloc[-1]
st.write(f"Latest Signal: {latest_signal}")

st.line_chart(data[['Close', 'SMA_20']])
