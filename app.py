import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def safe_float(val):
    if isinstance(val, pd.Series):
        return float(val.iloc[0])
    return float(val)

st.set_page_config(page_title="Stock Return Estimator", layout="centered")
st.title("📈 Weekly Return Estimator")
st.write("Estimate next week's return based on technical analysis.")

symbol = st.text_input("Enter NSE stock symbol (e.g. AJANTPHARM.NS):", "AJANTPHARM.NS")

if symbol:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            st.warning("No data found for this symbol.")
        else:
            data['Returns'] = data['Close'].pct_change()
            gain = data['Returns'].clip(lower=0)
            loss = -data['Returns'].clip(upper=0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / (avg_loss + 1e-10)
            data['RSI'] = 100 - (100 / (1 + rs))

            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

            data['20_MA'] = data['Close'].rolling(window=20).mean()
            data['50_MA'] = data['Close'].rolling(window=50).mean()

            latest = data.iloc[-1]

            latest_close = safe_float(latest['Close'])
            latest_rsi = safe_float(latest['RSI'])
            latest_macd = safe_float(latest['MACD'])
            latest_signal = safe_float(latest['Signal'])
            macd_diff = latest_macd - latest_signal

            st.subheader(f"📊 Technical Summary for {symbol}")
            st.metric("Latest Close", f"₹{latest_close:.2f}")
            st.metric("RSI (14)", f"{latest_rsi:.2f}")
            st.metric("MACD", f"{latest_macd:.2f}")
            st.metric("MACD Signal", f"{latest_signal:.2f}")

            if latest_rsi > 65 and macd_diff > 0:
                outlook = "Bullish"
                expected_return = "+2% to +4%"
            elif latest_rsi < 40 and macd_diff < 0:
                outlook = "Bearish"
                expected_return = "-2% to -4%"
            else:
                outlook = "Sideways/Neutral"
                expected_return = "-1% to +1%"

            st.subheader("📅 5-Day Forecast")
            st.info(f"**Outlook:** {outlook}\n\n**Expected Return Range:** {expected_return}")

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

            st.subheader("📍 Support & Resistance")
            recent_data = data.tail(30)
            support = safe_float(recent_data['Low'].min())
            resistance = safe_float(recent_data['High'].max())
            st.write(f"**Estimated Support:** ₹{support:.2f}")
            st.write(f"**Estimated Resistance:** ₹{resistance:.2f}")

            st.subheader("📊 Compare with Another Stock")

comp_symbol = st.text_input("Enter another stock (optional):", "SUNPHARMA.NS")

if comp_symbol.strip() != "":
    try:
        comp_data = yf.download(comp_symbol, start=start_date, end=end_date, progress=False)
        
        if not comp_data.empty and 'Close' in comp_data.columns:
            comp_close import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def safe_float(val):
    if isinstance(val, pd.Series):
        return float(val.iloc[0])
    return float(val)

st.set_page_config(page_title="Stock Return Estimator", layout="centered")
st.title("📈 Weekly Return Estimator")
st.write("Estimate next week's return based on technical analysis.")

symbol = st.text_input("Enter NSE stock symbol (e.g. AJANTPHARM.NS):", "AJANTPHARM.NS")

if symbol:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        if data.empty:
            st.warning("No data found for this symbol.")
        else:
            data['Returns'] = data['Close'].pct_change()
            gain = data['Returns'].clip(lower=0)
            loss = -data['Returns'].clip(upper=0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / (avg_loss + 1e-10)
            data['RSI'] = 100 - (100 / (1 + rs))

            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

            data['20_MA'] = data['Close'].rolling(window=20).mean()
            data['50_MA'] = data['Close'].rolling(window=50).mean()

            latest = data.iloc[-1]

            latest_close = safe_float(latest['Close'])
            latest_rsi = safe_float(latest['RSI'])
            latest_macd = safe_float(latest['MACD'])
            latest_signal = safe_float(latest['Signal'])
            macd_diff = latest_macd - latest_signal

            st.subheader(f"📊 Technical Summary for {symbol}")
            st.metric("Latest Close", f"₹{latest_close:.2f}")
            st.metric("RSI (14)", f"{latest_rsi:.2f}")
            st.metric("MACD", f"{latest_macd:.2f}")
            st.metric("MACD Signal", f"{latest_signal:.2f}")

            if latest_rsi > 65 and macd_diff > 0:
                outlook = "Bullish"
                expected_return = "+2% to +4%"
            elif latest_rsi < 40 and macd_diff < 0:
                outlook = "Bearish"
                expected_return = "-2% to -4%"
            else:
                outlook = "Sideways/Neutral"
                expected_return = "-1% to +1%"

            st.subheader("📅 5-Day Forecast")
            st.info(f"**Outlook:** {outlook}\n\n**Expected Return Range:** {expected_return}")

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

            st.subheader("📍 Support & Resistance")
            recent_data = data.tail(30)
            support = safe_float(recent_data['Low'].min())
            resistance = safe_float(recent_data['High'].max())
            st.write(f"**Estimated Support:** ₹{support:.2f}")
            st.write(f"**Estimated Resistance:** ₹{resistance:.2f}")

            st.subheader("📊 Compare with Another Stock")

comp_symbol = st.text_input("Enter another stock (optional):", "SUNPHARMA.NS")

if comp_symbol.strip() != "":
    try:
        comp_data = yf.download(comp_symbol, start=start_date, end=end_date, progress=False)
        
        if not comp_data.empty and 'Close' in comp_data.columns:
            comp_close = comp_data['Close'].rename(comp_symbol)
            primary_close = data['Close'].rename(symbol)

            combined = pd.concat([primary_close, comp_close], axis=1).dropna()

            if not combined.empty:
                st.line_chart(combined)
            else:
                st.warning("Not enough overlapping data between the two stocks to plot a comparison.")
        else:
            st.warning(f"No 'Close' data found for {comp_symbol}. Please verify the symbol.")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
else:
    st.info("Enter a stock symbol above to compare.")
        else:
            st.warning("Not enough overlapping data to compare.")
    else:
        st.warning("No data found for comparison symbol.")
                    else:
                        st.warning("Not enough overlapping data to compare.")
                else:
                    st.warning("No data found for comparison symbol.")

            st.subheader("📤 Export Report")
            st.write("🔒 PDF export feature coming soon in hosted version!")

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
= comp_data['Close'].rename(comp_symbol)
            primary_close = data['Close'].rename(symbol)

            combined = pd.concat([primary_close, comp_close], axis=1).dropna()

            if not combined.empty:
                st.line_chart(combined)
            else:
                st.warning("Not enough overlapping data between the two stocks to plot a comparison.")
        else:
            st.warning(f"No 'Close' data found for {comp_symbol}. Please verify the symbol.")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
else:
    st.info("Enter a stock symbol above to compare.")
        else:
            st.warning("Not enough overlapping data to compare.")
    else:
        st.warning("No data found for comparison symbol.")
                    else:
                        st.warning("Not enough overlapping data to compare.")
                else:
                    st.warning("No data found for comparison symbol.")

            st.subheader("📤 Export Report")
            st.write("🔒 PDF export feature coming soon in hosted version!")

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
