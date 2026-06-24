import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# 🌟 手機優化：強制使用窄版面（不使用 wide 模式），讓所有元件乖乖排在手機寬度內
st.set_page_config(page_title="AI看盤大軍", layout="centered")

st.title("🦅 AI 看盤大軍手機版")
st.caption("專為手機調校：大字體、免左右滑動、個股大卡片設計")

AI_STOCKS_DICT = {
    # ─── 核心算力與代工 ───
    '2330.TW': {'name': '台積電', 'group': '先進製程'},
    '2317.TW': {'name': '鴻海', 'group': 'AI 伺服器 ODM'},
    '2382.TW': {'name': '廣達', 'group': 'AI 伺服器 ODM'},
    '3231.TW': {'name': '緯創', 'group': '伺服器主機板'},
    '2454.TW': {'name': '聯發科', 'group': 'AI 晶片設計'},
    # ─── 關鍵關鍵散熱與機殼 ───
    '3017.TW': {'name': '奇鋐', 'group': '核心水冷散熱'},
    '3324.TW': {'name': '雙鴻', 'group': '核心水冷散熱'},
    '8210.TW': {'name': '勤誠', 'group': '伺服器機殼'},
    '3013.TW': {'name': '晟銘電', 'group': '伺服器機殼'},
    # ─── 矽光子與通訊 ───
    '3081.TWO': {'name': '聯亞', 'group': '矽光子雷射'},
    '3450.TW': {'name': '聯鈞', 'group': '矽光子封裝'},
    '4979.TW': {'name': '華星光', 'group': '光收發模組'},
    # ─── 電力重電 ───
    '1519.TW': {'name': '華城', 'group': '特高壓重電'},
    '1503.TW': {'name': '士電', 'group': '特高壓重電'},
    '1513.TW': {'name': '中興電', 'group': '配電盤/UPS'}
}

def diagnose_trend_status(p_close, ma20, ma60):
    if p_close > ma20 and ma20 > ma60: return "🔥 多頭強攻中"
    elif ma20 > ma60 and p_close <= ma20 and p_close > ma60: return "🛡️ 多頭良性拉回"
    elif p_close < ma60 and ma20 < ma60: return "⏳ 弱勢整理中"
    else: return "🌀 均線糾結盤整"

st.sidebar.header("🎯 群組過濾")
all_available_groups = sorted(list(set([v['group'] for v in AI_STOCKS_DICT.values()])))
selected_groups = st.sidebar.multiselect("選擇監控群組：", options=all_available_groups, default=all_available_groups)
FILTERED_STOCKS_DICT = {k: v for k, v in AI_STOCKS_DICT.items() if v['group'] in selected_groups}
FILTERED_TICKERS = list(FILTERED_STOCKS_DICT.keys())

@st.cache_data(ttl=600)
def fetch_all_data(tickers):
    if not tickers: return None, None
    try:
        import requests
        clean_session = requests.Session()
        clean_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
        })
        hourly = yf.download(tickers, period="1mo", interval="1h", group_by='ticker', progress=False, threads=False, session=clean_session)
        daily = yf.download(tickers, period="6mo", interval="1d", group_by='ticker', progress=False, threads=False, session=clean_session)
        return hourly, daily
    except:
        return None, None

if FILTERED_TICKERS:
    hourly_data, daily_data = fetch_all_data(FILTERED_TICKERS)
    
    if hourly_data is not None and daily_data is not None and not hourly_data.empty:
        is_multi = isinstance(hourly_data.columns, pd.MultiIndex)
        
        # 🌟 介面改成最適合手機的「上方切換大按鈕」
        view_mode = st.radio("請選擇看盤模式：", ["🎯 今日短線篩選", "💎 個股大字體K線"], horizontal=True)
        
        if view_mode == "🎯 今日短線篩選":
            st.markdown("### 📱 個股動態卡片 (直式滑動)")
            
            for ticker in FILTERED_TICKERS:
                try:
                    df_h = hourly_data[ticker].dropna() if is_multi else hourly_data.dropna()
                    if len(df_h) < 65: continue
                    df_h['MA60'] = df_h['Close'].rolling(window=60).mean()
                    
                    df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    
                    today_h = df_h.iloc[-1]
                    yesterday_d = df_d.iloc[-2]
                    today_d = df_d.iloc[-1]
                    
                    p_close = today_h['Close']
                    p_change = ((p_close - yesterday_d['Close']) / yesterday_d['Close']) * 100
                    trend_lbl = diagnose_trend_status(today_d['Close'], df_d['MA20'].iloc[-1], df_d['MA60'].iloc[-1])
                    
                    # 60分K戰法檢查：價格大於60MA
                    is_bull_60h = p_close > today_h['MA60']
                    signal_str = "✅ 符合60分K強勢" if is_bull_60h else "⚪ 區間整理"
                    
                    # 🌟 用方塊卡片（Container）把每檔股票包起來，手機上看一目了然
                    with st.container(border=True):
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            st.markdown(f"### **{FILTERED_STOCKS_DICT[ticker]['name']}**")
                            st.caption(f"{ticker} | {FILTERED_STOCKS_DICT[ticker]['group']}")
                        with col2:
                            color_prefix = "+" if p_change >= 0 else ""
                            text_color = "red" if p_change >= 0 else "green"
                            st.markdown(f"<h2 style='text-align: right; color: {text_color}; margin:0;'>{p_close:.1f}</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: right; color: {text_color}; margin:0;'>{color_prefix}{p_change:.2f}%</p>", unsafe_allow_html=True)
                        
                        st.markdown(f"**趨勢背景：** {trend_lbl}")
                        st.markdown(f"**短線訊號：** {signal_str}")
                except:
                    continue
                    
        else:
            st.markdown("### 🔍 個股智慧大 K 線")
            selector_options = {t: f"{FILTERED_STOCKS_DICT[t]['name']} ({t})" for t in FILTERED_TICKERS}
            selected_ticker = st.selectbox("請選擇股票：", options=FILTERED_TICKERS, format_func=lambda x: selector_options[x])
            
            chart_type = st.radio("選擇 K 線規格：", ["📈 60分鐘戰法線", "📊 日線長線圖"], horizontal=True)
            
            if "60分鐘" in chart_type:
                df_plot = hourly_data[selected_ticker].dropna() if is_multi else hourly_data.dropna()
                df_plot['MA60'] = df_plot['Close'].rolling(window=60).mean()
                df_plot = df_plot.tail(40)
                
                fig = make_subplots(rows=1, cols=1)
                fig.add_trace(go.Candlestick(x=df_plot.index, open=df_plot['Open'], high=df_plot['High'], low=df_plot['Low'], close=df_plot['Close'], name="60分K"))
                fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['MA60'], name="60MA", line=dict(color='cyan', width=2)))
            else:
                df_plot = daily_data[selected_ticker].dropna() if is_multi else daily_data.dropna()
                df_plot['MA20'] = df_plot['Close'].rolling(window=20).mean()
                df_plot['MA60'] = df_plot['Close'].rolling(window=60).mean()
                df_plot = df_plot.tail(40)
                
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_width=[0.3, 0.7])
                fig.add_trace(go.Candlestick(x=df_plot.index, open=df_plot['Open'], high=df_plot['High'], low=df_plot['Low'], close=df_plot['Close'], name="日K"), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['MA20'], name="20MA", line=dict(color='orange', width=1.5)), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot['MA60'], name="60MA", line=dict(color='limegreen', width=2)), row=1, col=1)
                fig.add_trace(go.Bar(x=df_plot.index, y=df_plot['Volume'], name="成交量", marker_color='#1f77b4'), row=2, col=1)
            
            # 🌟 手機圖表優化：縮小邊距、隱藏下方的滑動條，讓圖表在手機上完美呈現
            fig.update_layout(xaxis_rangeslider_visible=False, height=450, margin=dict(l=5, r=5, t=5, b=5), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True)
