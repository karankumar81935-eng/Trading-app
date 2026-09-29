
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.title("Crypto Live Analysis Dashboard")

crypto = st.selectbox('Select Crypto', ['BTC-USD', 'ETH-USD', 'SOL-USD'])

# Fetching Data
data = yf.download(crypto, period='1mo', interval='5m')

if not data.empty:
    # Technical Analysis: 20-period Simple Moving Average
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data.dropna(subset=['SMA_20'], inplace=True)

    # Signal Generation
    data['Signal'] = 'Hold'
    data.loc[data['Close'] > data['SMA_20'], 'Signal'] = 'Buy'
    data.loc[data['Close'] < data['SMA_20'], 'Signal'] = 'Sell'

    latest_signal = data['Signal'].iloc[-1]
    st.write(f"Latest Signal: {latest_signal}")

    # Plotting Data
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])

    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'))

    # Buy/Sell Markers
    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Signal'] = 'Sell'

    latest_signal = data['Signal'].iloc[-1]
    st.write(f"Latest Signal: {latest_signal}")

    # Plotting Data
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'])])

    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'))

    # Buy/Sell Markers
    buy_signals = data[data['Signal'] == 'Buy']
    sell_signals = data[data['Signal'] == 'Sell']

    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                             mode='markers', marker=dict(color='green', size=8, symbol='triangle-up'),
                             name='Buy Signal'))

    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                             mode='markers', marker=dict(color='red', size=8, symbol='triangle-down'),
                             name='Sell Signal'))

    fig.update_layout(title=f'{crypto} Analysis with Buy/Sell Signals', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)
else:
    st.error("No data available.")
