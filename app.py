import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import google.generativeai as genai

# स्ट्रीमलिट पेज कॉन्फिगरेशन
st.set_page_config(layout="wide", page_title="AI Crypto Agent")

st.title("🚀 AI Crypto Live Analysis Dashboard")

# जेमिनी API की कॉन्फ़िगरेशन
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel( 'models/gemini-1.5-flash')
                                 
else:
    st.warning("कृपया साइडबार में अपनी Gemini API Key दर्ज करें।")

crypto_options = ['BTC-USD', 'ETH-USD', 'SOL-USD']
crypto = st.selectbox('Select Crypto', crypto_options)

# डेटा फेचिंग फंक्शन
@st.cache_data(ttl=300)
def fetch_data(crypto_symbol):
    data = yf.download(crypto_symbol, period='1mo', interval='5m')
    return data

if api_key:
    data = fetch_data(crypto)

    if not data.empty:
        # डेटा को टेक्स्ट में बदलना ताकि AI समझ सके
        data_summary = data[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10).to_string()

        # AI एनालिसिस
        prompt = f"""
        You are an expert crypto trading assistant. 
        Analyze the recent price action of {crypto} based on the following 5-minute interval data:
        
        {data_summary}
        
        Provide a concise trading signal: 'Buy', 'Sell', or 'Hold'.
        Give a brief reason for your decision.
        """
        
        try:
            response = model.generate_content(prompt)
            ai_analysis = response.text
        except Exception as e:
            ai_analysis = f"Error generating analysis: {e}"

        # सिग्नल डिस्प्ले
        st.subheader("🤖 AI Agent Analysis")
        st.write(ai_analysis)

        # टेक्निकल इंडिकेटर्स
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data.dropna(subset=['SMA_20'], inplace=True)

        # प्लॉटिंग डेटा
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name='Market Data')])

        fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='orange', width=1.5), name='SMA 20'))

        fig.update_layout(title=f'{crypto} Live Price Chart with SMA',
                          xaxis_title='Time',
                          yaxis_title='Price (USD)',
                          height=600)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error
        
