import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objects as go
import google.generativeai as genai

st.set_page_config(layout="wide", page_title="AI Crypto Live Analysis Dashboard")

st.title("💡 AI Crypto Live Analysis Dashboard")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-3.8-flash')
else:
    st.warning("Please enter your Gemini API Key in the sidebar.")

crypto_options = ['BTC-USD', 'ETH-USD', 'SOL-USD']
crypto = st.selectbox('Select Crypto', crypto_options)

@st.cache_data(ttl=300)
def fetch_data(crypto_symbol):
    data = yf.download(crypto_symbol, period='1mo', interval='5m')
    return data

if api_key:
    data = fetch_data(crypto)

    if not data.empty:
        data_summary = data[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).to_string()
        
        prompt = f"""
        You are an expert crypto trading assistant.
        Analyze the recent price action of {crypto} based on the last 10 periods:
        {data_summary}
        Provide a concise trading signal: 'Buy', 'Sell', or 'Hold'.
        Give a brief reason for your decision.
        """
        
        try:
            response = model.generate_content(prompt)
            ai_analysis = response.text
        except Exception as e:
            ai_analysis = f"Error generating analysis: {e}"

        st.subheader("🤖 AI Agent Analysis")
        st.write(ai_analysis)

        st.subheader("📈 Technical Indicators")
        data[('SMA_20', '')] = data['Close'].iloc[:, 0].rolling(window=20).mean()
        st.write(data.head())
        
data['SMA_50'] = data['Close'].iloc[:, 0].rolling(window=50).mean()
data.dropna(inplace=True)
data['Signal'] = 0
data['Signal'] = np.where(data['SMA_20'] > data['SMA_50'], 1, 0)
data['Position'] = data['Signal'].diff()
latest_position = data['Position'].iloc[-1]
if latest_position == 1:
    st.write("Buy Signal")
elif latest_position == -1:
    st.write("Sell Signal")
else:
    st.write("No Signal")


data.dropna(subset=[('SMA_20', '')], inplace=True)

st.subheader("📊 Plotting Data")
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                            open=data['Open'],
                                            high=data['High'],
                                            low=data['Low'],
                                            close=data['Close'],
                                            name='Market Data')])
        
        fig.add_trace(go.Scatter(x=data.index, y=data[('SMA_20', '')], line=dict(color='orange', width=2), name='SMA_20'))
        
        fig.update_layout(title=f'{crypto} Live Price Chart with SMA_20',
                          xaxis_title='Time',
                          yaxis_title='Price (USD)',
                          height=600)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Data not found.")
else:
    st.error("No data available.")
        
