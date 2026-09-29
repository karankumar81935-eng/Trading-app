
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

st.title("Live Crypto Dashboard with Signals & News")

crypto = st.selectbox('Select Crypto', ['BTC-USD', 'ETH-USD', 'SOL-USD'])

# Intraday data
data = yf.download(crypto, period='5d', interval='5m')

data['SMA_20'] = ta.sma(data['Close'], length=20)
data.dropna(inplace=True)
data['Signal'] = 'Hold'
data.loc[data['Close'].values > data['SMA_20'].values, 'Signal'] = 'Buy'
data.loc[data['Close'].values < data['SMA_20'].values, 'Signal'] = 'Sell'

latest_signal = data['Signal'].iloc[-1]
st.write(f"Latest Signal: {latest_signal}")

st.line_chart(data[['Close', 'SMA_20']])

# News Section
st.subheader("Latest News")
ticker = yf.Ticker(crypto)
news = ticker.news
for item in news[:5]:
    st.write(f"- {item['title']}")




