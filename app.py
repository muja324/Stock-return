import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Stock Return Estimator", layout="centered")
st.title("📈 Weekly Return Estimator")
st.write("Estimate next week's return based on technical analysis.")

# User input
symbol = st.text_input("Enter NSE stock symbol (e.g. AJANTPHARM.NS):", "AJANTPHARM.NS")

if symbol:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)

    try:
        data = yf.download(symbol, start=start_date, end=end_date)

        if not data.empty:
            # Technical Indicators
            data['20_MA'] = data['Close'].rolling(window=20).mean()
            data['50_MA'] = data['Close'].rolling(window=50).mean()
            data['Returns'] = data['Close'].pct_change()

            # RSI Calculation
            mean_gain = data['Returns'].clip(lower=0).rolling(window=14).mean()
            mean_loss = -data['Returns'].clip(upper=0).rolling(window=14).mean()
            rs = mean_gain / (mean_loss + 1e-10)
            data['RSI'] = 100 - (100 / (1 + rs))

            # MACD
            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

            latest = data.iloc[-1]

            # 🧾 Display Technical Metrics
            st.subheader(f"📊 Technical Summary for {symbol}")
            st.metric("Latest Close", f"₹{latest['Close']:.2f}" if pd.notnull(latest['Close']) else "N/A")
            st.metric("RSI (14)", f"{latest['RSI']:.2f}" if pd.notnull(latest['RSI']) else "N/A")
            st.metric("MACD", f"{latest['MACD']:.2f}" if pd.notnull(latest['MACD']) else "N/A")
            st.metric("MACD Signal", f"{latest['Signal']:.2f}" if pd.notnull(latest['Signal']) else "N/A")

            # 🔮 Return Estimation
            rsi = latest['RSI']
            macd_diff = latest['MACD'] - latest['Signal']

            if rsi > 65 and macd_diff > 0:
                outlook = "Bullish"
                expected_return = "+2% to +4%"
            elif rsi < 40 and macd_diff < 0:
                outlook = "Bearish"
                expected_return = "-2% to -4%"
            else:
                outlook = "Sideways/Neutral"
                expected_return = "-1% to +1%"

            st.subheader("📅 5-Day Forecast")
            st.info(f"**Outlook:** {outlook}\n\n**Expected Return Range:** {expected_return}")

            # 📉 Candlestick Chart
            st.subheader("📉 Price Chart (Candlestick)")
            fig = go.Figure(data=[
                go.Candlestick(x=data.index,
                               open=data['Open'],
                               high=data['High'],
                               low=data['Low'],
                               close=data['Close'],
                               name='Candlestick'),
                go.Scatter(x=data.index, y=data['20_MA'], mode='lines', name='20 MA'),
                go.Scatter(x=data.index, y=data['50_MA'], mode='lines', name='50 MA')
            ])
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # 📍 Support and Resistance
            st.subheader("📍 Support & Resistance")
            recent_data = data.tail(30)
            support = recent_data['Low'].min()
            resistance = recent_data['High'].max()
            st.write(f"**Estimated Support:** ₹{support:.2f}")
            st.write(f"**Estimated Resistance:** ₹{resistance:.2f}")

            # 📊 Multi-stock comparison
            st.subheader("📊 Compare with Another Stock")
            comp_symbol = st.text_input("Enter another stock (optional):", "SUNPHARMA.NS")
            if comp_symbol:
                comp_data = yf.download(comp_symbol, start=start_date, end=end_date)['Close']
                compare_df = pd.DataFrame({symbol: data['Close'], comp_symbol: comp_data})
                compare_df.dropna(inplace=True)
                st.line_chart(compare_df)

            # 📤 Export (Placeholder)
            st.subheader("📤 Export Report")
            st.write("🔒 PDF export feature coming soon in hosted version!")

        else:
            st.warning("⚠️ No data found for this symbol.")

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
