
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

st.title("Live Crypto Dashboard with Signals & News")

crypto = st.selectbox('Select Crypto', ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'DOT-USD'])

data = yf.download(crypto, period='5d', interval='5m')

if not data.empty:
    data['SMA_20'] = ta.sma(data['Close'], length=20)
    data.dropna(inplace=True)

    data['Signal'] = 'Hold'
    data.loc[data['Close'].values > data['SMA_20'].values, 'Signal'] = 'Buy'
    data.loc[data['Close'].values < data['SMA_20'].values, 'Signal'] = 'Sell'

    latest_signal = data['Signal'].iloc[-1]
    st.write(f"Latest Signal: {latest_signal}")

    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])

    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'))

    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']

    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                             mode='markers', marker=dict(color='green', size=10, symbol='triangle-up'),
                             name='Buy Signal'))
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                             mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='Sell Signal'))

    fig.update_layout(title=f'{crypto} Price Chart with SMA & Signals',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)

    st.subheader("Latest News")
    ticker = yf.Ticker(crypto)
    news = ticker.news
    for item in news[:5]:
        st.write(f"- {item['title']}")
else:
    st.error("No data found for the selected crypto.")
