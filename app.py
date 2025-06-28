# (Same imports)
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

# Forecast logic functions
def forecast_logic(data, range_type):
    latest = data.iloc[-1]
    rsi = safe_float(latest['RSI'])
    macd = safe_float(latest['MACD'])
    signal = safe_float(latest['Signal'])
    macd_diff = macd - signal

    if range_type == "Weekly":
        if rsi > 65 and macd_diff > 0:
            return "Bullish", "+2% to +4%"
        elif rsi < 40 and macd_diff < 0:
            return "Bearish", "-2% to -4%"
        else:
            return "Sideways/Neutral", "-1% to +1%"

    elif range_type == "Monthly":
        if rsi > 65 and macd_diff > 0:
            return "Bullish", "+4% to +7%"
        elif rsi < 35 and macd_diff < 0:
            return "Bearish", "-4% to -7%"
        else:
            return "Sideways/Neutral", "-2% to +2%"

# Page setup
st.set_page_config(page_title="Stock Return Estimator", layout="centered")
st.title("📈 Stock Return Estimator")
st.write("Estimate weekly/monthly return based on technical indicators.")

main_symbol = st.text_input("Enter NSE stock symbol (e.g. TCS.NS):", "AJANTPHARM.NS")
forecast_range = st.selectbox("Choose Forecast Range:", ["Weekly", "Monthly"])

if main_symbol:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    try:
        data = yf.download(main_symbol, start=start_date, end=end_date, progress=False)

        if data.empty:
            st.warning("No data found for this symbol.")
        else:
            # Technical indicators
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

            # Summary
            st.subheader(f"📊 Technical Summary for {main_symbol}")
            st.metric("Latest Close", f"₹{latest_close:.2f}")
            st.metric("RSI (14)", f"{latest_rsi:.2f}")
            st.metric("MACD", f"{latest_macd:.2f}")
            st.metric("MACD Signal", f"{latest_signal:.2f}")

            # Forecast
            st.subheader(f"📅 {forecast_range} Forecast")
            outlook, expected_return = forecast_logic(data, forecast_range)
            st.info(f"**Outlook:** {outlook}\n\n**Expected Return Range:** {expected_return}")

            # TradingView chart
            st.subheader("📉 Price Chart (TradingView)")
            tv_symbol = f"{main_symbol.replace('.NS', '')}"
            tradingview_full_chart = f"""
            <div class="tradingview-widget-container" style="height:500px;">
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
                new TradingView.widget({{
                  "width": "100%",
                  "height": 500,
                  "symbol": "{tv_symbol}",
                  "interval": "D",
                  "timezone": "Asia/Kolkata",
                  "theme": "dark",
                  "style": "1",
                  "locale": "en",
                  "toolbar_bg": "#f1f3f6",
                  "enable_publishing": false,
                  "allow_symbol_change": true,
                  "container_id": "tradingview_chart"
                }});
              </script>
              <div id="tradingview_chart"></div>
            </div>
            """
            st.components.v1.html(tradingview_full_chart, height=500)

            # Support & Resistance
            st.subheader("📍 Support & Resistance")
            recent_data = data.tail(30)
            support = safe_float(recent_data['Low'].min())
            resistance = safe_float(recent_data['High'].max())
            st.write(f"**Estimated Support:** ₹{support:.2f}")
            st.write(f"**Estimated Resistance:** ₹{resistance:.2f}")

            # Compare with Another Stock
            st.subheader("📊 Compare with Another Stock")
            compare_symbol = st.text_input("Enter another stock (optional):", "SUNPHARMA.NS")

            if compare_symbol.strip() != "":
                try:
                    comp_data = yf.download(compare_symbol, start=start_date, end=end_date, progress=False)

                    if not comp_data.empty and 'Close' in comp_data.columns:
                        comp_close = comp_data['Close'].rename(compare_symbol)
                        main_close = data['Close'].rename(main_symbol)

                        combined = pd.concat([main_close, comp_close], axis=1).dropna()

                        if not combined.empty:
                            st.line_chart(combined)
                        else:
                            st.warning("Not enough overlapping data between the two stocks to compare.")
                    else:
                        st.warning(f"No 'Close' data found for {compare_symbol}.")
                except Exception as e:
                    st.error(f"Error fetching comparison data: {e}")
            else:
                st.info("Enter a stock symbol above to compare.")

            # Export placeholder
            st.subheader("📤 Export Report")
            st.write("🔒 PDF export feature coming soon in hosted version!")

    except Exception as e:
        st.error(f"❌ Error fetching data for {main_symbol}: {e}")
