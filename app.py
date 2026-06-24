import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from FinMind.data import DataLoader
from datetime import datetime, timedelta

st.set_page_config(page_title="台股AI全鏈監控系統", layout="wide")
st.title("🤖 台股 AI 全產業鏈 100+ 大軍終極永久看板")
st.caption("正式雲端穩定版：技術面趨勢 × 雙週期K線智慧交互 × 籌碼時間軸完全對齊")

AI_STOCKS_DICT = {
    # ─── 基礎算力層 ───
    '3661.TW': {'name': '世芯-KY', 'group': '01. 矽智財 (IP/ASIC)'},
    '3443.TW': {'name': '創意', 'group': '01. 矽智財 (IP/ASIC)'},
    '3035.TW': {'name': '智原', 'group': '01. 矽智財 (IP/ASIC)'},
    '6643.TWO': {'name': 'M31', 'group': '01. 矽智財 (IP/ASIC)'},
    '6533.TWO': {'name': '晶心科', 'group': '01. 矽智財 (IP/ASIC)'},
    '2454.TW': {'name': '聯發科', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2379.TW': {'name': '瑞昱', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3034.TW': {'name': '聯詠', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '5274.TW': {'name': '信驊', 'group': '03. 伺服器 BMC/遠端控制 IC'},
    '5269.TW': {'name': '祥碩', 'group': '04. 高速傳輸控制 IC (PCIe 5)'},
    '4966.TW': {'name': '譜瑞-KY', 'group': '04. 高速傳輸控制 IC (PCIe 5)'},
    '6415.TW': {'name': '矽力*-KY', 'group': '05. 伺服器電源管理 IC (PMIC)'},
    '2330.TW': {'name': '台積電', 'group': '06. 晶圓代工 (先進製程)'},
    '2303.TW': {'name': '聯電', 'group': '07. 晶圓代工 (成熟製程)'},
    '5347.TW': {'name': '世界', 'group': '07. 晶圓代工 (成熟製程)'},
    # ─── 先進封裝與半導體設備 ───
    '3711.TW': {'name': '日月光投控', 'group': '08. 先進封裝封測 (CoWoS)'},
    '2449.TW': {'name': '京元電子', 'group': '08. 先進封裝封測 (CoWoS)'},
    '6239.TW': {'name': '力成', 'group': '08. 先進封裝封測 (CoWoS)'},
    '6147.TWO': {'name': '頎邦', 'group': '09. 面板級先進封裝 (FOPLP)'},
    '3481.TW': {'name': '群創', 'group': '09. 面板級先進封裝 (FOPLP)'},
    '3131.TWO': {'name': '弘塑', 'group': '10. 先進封裝濕製程設備'},
    '3583.TW': {'name': '辛耘', 'group': '10. 先進封裝濕製程設備'},
    '6187.TWO': {'name': '萬潤', 'group': '11. 先進封裝點膠/自動化設備'},
    '2467.TW': {'name': '志聖', 'group': '11. 先進封裝點膠/自動化設備'},
    '5443.TW': {'name': '均豪', 'group': '11. 先進封裝點膠/自動化設備'},
    '6515.TW': {'name': '穎崴', 'group': '12. 高階晶片測試座 (Socket)'},
    '6223.TW': {'name': '旺矽', 'group': '13. 晶圓前段探針卡/測試介面'},
    '6510.TW': {'name': '精測', 'group': '13. 晶圓前段探針卡/測試介面'},
    '3680.TW': {'name': '家登', 'group': '14. EUV 光罩傳送盒/半導體材料'},
    '3289.TW': {'name': '宜特', 'group': '15. 半導體驗證/材料分析 (MA/RA)'},
    '3587.TWO': {'name': '閎康', 'group': '15. 半導體驗證/材料分析 (MA/RA)'},
    '6830.TW': {'name': '汎銓', 'group': '15. 半導體驗證/材料分析 (MA/RA)'},
    # ─── 數據網路與通訊 ───
    '3081.TWO': {'name': '聯亞', 'group': '16. 矽光子雷射晶片/磊晶 (DFB)'},
    '6451.TW': {'name': '訊芯-KY', 'group': '17. 矽光子/CPO 模組封裝'},
    '3363.TWO': {'name': '上詮', 'group': '17. 矽光子/CPO 模組封裝'},
    '3450.TW': {'name': '聯鈞', 'group': '17. 矽光子/CPO 模組封裝'},
    '6442.TW': {'name': '光聖', 'group': '18. 高階光收發模組 (800G+)'},
    '4979.TW': {'name': '華星光', 'group': '18. 高階光收發模組 (800G+)'},
    '2345.TW': {'name': '智邦', 'group': '19. 高階資料中心交換器'},
    # ─── 伺服器中游硬體 ───
    '2317.TW': {'name': '鴻海', 'group': '20. AI 伺服器代工 (ODM整機櫃)'},
    '2382.TW': {'name': '廣達', 'group': '20. AI 伺服器代工 (ODM整機櫃)'},
    '6669.TW': {'name': '緯穎', 'group': '20. AI 伺服器代工 (ODM整機櫃)'},
    '3231.TW': {'name': '緯創', 'group': '21. 伺服器主機板 & GPU加速卡基板'},
    '2356.TW': {'name': '英業達', 'group': '21. 伺服器主機板 & GPU加速卡基板'},
    '2376.TW': {'name': '技嘉', 'group': '21. 伺服器主機板 & GPU加速卡基板'},
    '3017.TW': {'name': '奇鋐', 'group': '22. 核心液冷散熱 (CDU/水冷板)'},
    '3324.TW': {'name': '雙鴻', 'group': '22. 核心液冷散熱 (CDU/水冷板)'},
    '8996.TW': {'name': '高力', 'group': '22. 核心液冷散熱 (CDU/水冷板)'},
    '2421.TW': {'name': '建準', 'group': '23. 高階散熱風扇 & 均熱片'},
    '3653.TW': {'name': '健策', 'group': '23. 高階散熱風扇 & 均熱片'},
    '3483.TW': {'name': '力致', 'group': '23. 高階散熱風扇 & 均熱片'},
    '8210.TW': {'name': '勤誠', 'group': '24. AI 伺服器專用機殼/水冷櫃'},
    '3013.TW': {'name': '晟銘電', 'group': '24. AI 伺服器專用機殼/水冷櫃'},
    '6117.TW': {'name': '迎廣', 'group': '24. AI 伺服器專用機殼/水冷櫃'},
    '2059.TW': {'name': '川湖', 'group': '25. 高階伺服器滑軌/導軌'},
    '6584.TW': {'name': '南俊國際', 'group': '25. 高階伺服器滑軌/導軌'},
    '2383.TW': {'name': '台光電', 'group': '26. 高頻高速 CCL 銅箔基板'},
    '6274.TW': {'name': '台燿', 'group': '26. 高頻高速 CCL 銅箔基板'},
    '6213.TW': {'name': '聯茂', 'group': '26. 高頻高速 CCL 銅箔基板'},
    '2368.TW': {'name': '金像電', 'group': '27. 高層數伺服器 PCB 主板'},
    '4958.TW': {'name': '臻鼎-KY', 'group': '27. 高層數伺服器 PCB 主板'},
    '3044.TW': {'name': '健鼎', 'group': '27. 高層數伺服器 PCB 主板'},
    '3037.TW': {'name': '欣興', 'group': '28. ABF 晶片載板'},
    '8046.TW': {'name': '南電', 'group': '28. ABF 晶片載板'},
    # ─── 周邊與延伸支援 ───
    '2408.TW': {'name': '南亞科', 'group': '29. HBM / 高頻寬記憶體顆粒'},
    '8299.TWO': {'name': '群聯', 'group': '29. HBM / 高頻寬記憶體顆粒'},
    '3260.TWO': {'name': '威剛', 'group': '29. HBM / 高頻寬記憶體顆粒'},
    '2308.TW': {'name': '台達電', 'group': '30. 伺服器高階高功率電源 (5.5kW+)'},
    '2301.TW': {'name': '光寶科', 'group': '30. 伺服器高階高功率電源 (5.5kW+)'},
    '6197.TW': {'name': '佳必琪', 'group': '31. NVLink 高速線束 & 連接器'},
    '3533.TW': {'name': '嘉澤', 'group': '31. NVLink 高速線束 & 連接器'},
    '3665.TW': {'name': '貿聯-KY', 'group': '31. NVLink 高速線束 & 連接器'},
    '1519.TW': {'name': '華城', 'group': '32. 機房電力大變壓器 (特高壓重電)'},
    '1503.TW': {'name': '士電', 'group': '32. 機房電力大變壓器 (特高壓重電)'},
    '1513.TW': {'name': '中興電', 'group': '33. 機房配電盤 & 不斷電系統 (UPS)'},
    '1514.TW': {'name': '亞力', 'group': '33. 機房配電盤 & 不斷電系統 (UPS)'},
    '2327.TW': {'name': '國巨', 'group': '34. 被動元件 (高階 MLCC)'},
    '3675.TWO': {'name': '德微', 'group': '35. 分離元件 & 功率半導體 (MOSFET)'},
    '2481.TW': {'name': '強茂', 'group': '35. 分離元件 & 功率半導體 (MOSFET)'},
    '2359.TW': {'name': '所羅門', 'group': '36. AI 智慧視覺 & 具身智慧機器人'},
    '6188.TW': {'name': '廣明', 'group': '36. AI 智慧視覺 & 具身智慧機器人'},
    '2353.TW': {'name': '宏碁', 'group': '37. AI PC 品牌與終端'},
    '2357.TW': {'name': '華碩', 'group': '37. AI PC 品牌與終端'}
}

def diagnose_trend_status(p_close, ma20, ma60):
    if p_close > ma20 and ma20 > ma60: return "🔥 多頭強攻中"
    elif ma20 > ma60 and p_close <= ma20 and p_close > ma60: return "🛡️ 多頭良性拉回"
    elif p_close < ma60 and ma20 < ma60: return "⏳ 趨勢空頭/弱勢整理"
    else: return "🌀 均線糾結盤整"

st.sidebar.header("🎯 AI 供應鏈精密群組過濾")
all_available_groups = sorted(list(set([v['group'] for v in AI_STOCKS_DICT.values()])))
selected_groups = st.sidebar.multiselect("選擇監控群組：", options=all_available_groups, default=all_available_groups)
FILTERED_STOCKS_DICT = {k: v for k, v in AI_STOCKS_DICT.items() if v['group'] in selected_groups}
FILTERED_TICKERS = list(FILTERED_STOCKS_DICT.keys())

@st.cache_data(ttl=900)
def fetch_all_data(tickers):
    if not tickers: return None, None
    try:
        # 🛡️ 終極防禦：單次批量打包下載，並強制關閉 threads，徹底免疫機房保安系統的弱引用死鎖！
        hourly = yf.download(tickers, period="2mo", interval="1h", group_by='ticker', progress=False, threads=False)
        daily = yf.download(tickers, period="8mo", interval="1d", group_by='ticker', progress=False, threads=False)
        return hourly, daily
    except Exception as e:
        st.error(f"數據加載同步中，請稍候重整：{e}")
        return None, None

if FILTERED_TICKERS:
    hourly_data, daily_data = fetch_all_data(FILTERED_TICKERS)
    
    if hourly_data is not None and daily_data is not None:
        tab1, tab2, tab3, tab4 = st.tabs(["🔥 60分線 666 戰法", "🛡️ 均線防守 & 低檔反彈選股", "💎 全能智慧 K 線查閱畫布", "📊 AI大軍量能與趨勢排行"])
        
        # ─── 分頁一 ───
        with tab1:
            st.subheader("🤖 微族群過濾 - 60分鐘線極短線動能篩選")
            matches = []
            for ticker in FILTERED_TICKERS:
                try:
                    df = hourly_data[ticker].dropna() if len(FILTERED_TICKERS) > 1 else hourly_data.dropna()
                    if len(df) < 65: continue
                    df['MA60'] = df['Close'].rolling(window=60).mean()
                    low_60, high_60 = df['Low'].rolling(window=60).min(), df['High'].rolling(window=60).max()
                    df['RSV'] = (((df['Close'] - low_60) / (high_60 - low_60)) * 100).fillna(50)
                    df['K'] = df['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df['D'] = df['K'].ewm(alpha=1/3, adjust=False).mean()
                    today = df.iloc[-1]
                    if today['Close'] > today['MA60'] and today['K'] > today['D']:
                        df_d = daily_data[ticker].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                        df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                        df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                        p_tod = df_d.iloc[-1]
                        trend_lbl = diagnose_trend_status(p_tod['Close'], p_tod['MA20'], p_tod['MA60'])
                        matches.append({"代號": ticker, "股票名稱": AI_STOCKS_DICT[ticker]['name'], "AI細分族群": AI_STOCKS_DICT[ticker]['group'], "當前價": round(today['Close'], 2), "波段趨勢位階": trend_lbl})
                except: continue
            if matches: 
                st.success(f"🎯 篩選成功！共有 {len(matches)} 檔符合條件。")
                st.dataframe(pd.DataFrame(matches).reset_index(drop=True), use_container_width=True)
                st.markdown("---")
                selected_t1 = st.selectbox("📊 點擊個股，下方立刻同步看 60分K 戰法線型圖：", options=[m["代號"] for m in matches], format_func=lambda x: f"{x} {AI_STOCKS_DICT[x]['name']}", key="t1_select")
                df_t1 = hourly_data[selected_t1].dropna() if len(FILTERED_TICKERS) > 1 else hourly_data.dropna()
                df_t1['MA60'] = df_t1['Close'].rolling(window=60).mean()
                l_60, h_60 = df_t1['Low'].rolling(window=60).min(), df_t1['High'].rolling(window=60).max()
                df_t1['RSV'] = (((df_t1['Close'] - l_60) / (h_60 - l_60)) * 100).fillna(50)
                df_t1['K'] = df_t1['RSV'].ewm(alpha=1/3, adjust=False).mean()
                df_t1['D'] = df_t1['K'].ewm(alpha=1/3, adjust=False).mean()
                df_plot_t1 = df_t1.tail(60)
                fig_t1 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                fig_t1.add_trace(go.Candlestick(x=df_plot_t1.index, open=df_plot_t1['Open'], high=df_plot_t1['High'], low=df_plot_t1['Low'], close=df_plot_t1['Close'], name="60分K"), row=1, col=1)
                fig_t1.add_trace(go.Scatter(x=df_plot_t1.index, y=df_plot_t1['MA60'], name="60MA", line=dict(color='cyan', width=2.5)), row=1, col=1)
                fig_t1.add_trace(go.Scatter(x=df_plot_t1.index, y=df_plot_t1['K'], name="K", line=dict(color='red', width=1.5)), row=2, col=1)
                fig_t1.add_trace(go.Scatter(x=df_plot_t1.index, y=df_plot_t1['D'], name="D", line=dict(color='green', width=1.5)), row=2, col=1)
                fig_t1.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_t1, use_container_width=True)
            else: st.info("目前範圍內無標的符合條件。")
            
        # ─── 分頁二 ───
        with tab2:
            st.subheader("🔍 日線級別 - 中長線均線防守診斷")
            correction_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_d = daily_data[ticker].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    p_today = df_d.iloc[-1]
                    if p_today['Close'] < p_today['MA20'] or p_today['Close'] < p_today['MA60']:
                        diagnose = diagnose_trend_status(p_today['Close'], p_today['MA20'], p_today['MA60'])
                        correction_list.append({"代號": ticker, "股票名稱": AI_STOCKS_DICT[ticker]['name'], "AI細分族群": AI_STOCKS_DICT[ticker]['group'], "今日收盤": round(p_today['Close'], 2), "趨勢診斷": diagnose})
                except: continue
            if correction_list: 
                st.warning(f"⚠️ 警示：有 {len(correction_list)} 檔標的回檔修正中：")
                st.dataframe(pd.DataFrame(correction_list).reset_index(drop=True), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🌟 智慧自動選股：鎖定安全打底準備反彈區")
            rebound_matches = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_r = daily_data[ticker].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                    df_r['MA20'] = df_r['Close'].rolling(window=20).mean(); df_r['MA60'] = df_r['Close'].rolling(window=60).mean()
                    low_9, high_9 = df_r['Low'].rolling(window=9).min(), df_r['High'].rolling(window=9).max()
                    df_r['RSV'] = (((df_r['Close'] - low_9) / (high_9 - low_9)) * 100).fillna(50)
                    df_r['K'] = df_r['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df_r['D'] = df_r['K'].ewm(alpha=1/3, adjust=False).mean()
                    today_r, yesterday_r = df_r.iloc[-1], df_r.iloc[-2]
                    if yesterday_r['K'] < 30 and yesterday_r['K'] <= yesterday_r['D'] and today_r['K'] > today_r['D']:
                        trend_lbl = diagnose_trend_status(today_r['Close'], today_r['MA20'], today_r['MA60'])
                        rebound_matches.append({"代號": ticker, "股票名稱": FILTERED_STOCKS_DICT[ticker]['name'], "AI細分族群": FILTERED_STOCKS_DICT[ticker]['group'], "目前價格": round(today_r['Close'], 2), "長線趨勢背景": trend_lbl})
                except: continue
            if rebound_matches: 
                st.success(f"🚀 打底完成！目前有 {len(rebound_matches)} 檔符合【低檔準備反彈】訊號！")
                st.dataframe(pd.DataFrame(rebound_matches).reset_index(drop=True), use_container_width=True)
                
            all_t2_targets = list(set([c["代號"] for c in correction_list] + [r["代號"] for r in rebound_matches]))
            if all_t2_targets:
                st.markdown("---")
                selected_t2 = st.selectbox("📊 選擇上方標的，直接看日K線與日線KD打底圖：", options=all_t2_targets, format_func=lambda x: f"{x} {AI_STOCKS_DICT[x]['name']}", key="t2_select")
                df_t2 = daily_data[selected_t2].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                df_t2['MA20'] = df_t2['Close'].rolling(window=20).mean()
                df_t2['MA60'] = df_t2['Close'].rolling(window=60).mean()
                l_9, h_9 = df_t2['Low'].rolling(window=9).min(), df_t2['High'].rolling(window=9).max()
                df_t2['RSV'] = (((df_t2['Close'] - l_9) / (h_9 - l_9)) * 100).fillna(50)
                df_t2['K'] = df_t2['RSV'].ewm(alpha=1/3, adjust=False).mean()
                df_t2['D'] = df_t2['K'].ewm(alpha=1/3, adjust=False).mean()
                df_plot_t2 = df_t2.tail(50)
                fig_t2 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                fig_t2.add_trace(go.Candlestick(x=df_plot_t2.index, open=df_plot_t2['Open'], high=df_plot_t2['High'], low=df_plot_t2['Low'], close=df_plot_t2['Close'], name="日K"), row=1, col=1)
                fig_t2.add_trace(go.Scatter(x=df_plot_t2.index, y=df_plot_t2['MA20'], name="20MA月線", line=dict(color='orange', width=2)), row=1, col=1)
                fig_t2.add_trace(go.Scatter(x=df_plot_t2.index, y=df_plot_t2['MA60'], name="60MA季線", line=dict(color='limegreen', width=2.5)), row=1, col=1)
                fig_t2.add_trace(go.Scatter(x=df_plot_t2.index, y=df_plot_t2['K'], name="日K值", line=dict(color='red', width=1.5)), row=2, col=1)
                fig_t2.add_trace(go.Scatter(x=df_plot_t2.index, y=df_plot_t2['D'], name="日D值", line=dict(color='green', width=1.5)), row=2, col=1)
                fig_t2.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_t2, use_container_width=True)

        # ─── 分頁三 ───
        with tab3:
            st.subheader("💎 AI 個股波段趨勢 & 雙規格智慧 K 線看板")
            selector_options = {t: f"{t} {FILTERED_STOCKS_DICT[t]['name']} ({FILTERED_STOCKS_DICT[t]['group']})" for t in FILTERED_TICKERS}
            selected_ticker = st.selectbox("請選擇你想查看 K 線圖的 AI 股：", options=FILTERED_TICKERS, format_func=lambda x: selector_options[x])
            stock_id = selected_ticker.split('.')[0]
            chart_type = st.radio("請選擇 K 線圖查閱規格：", ["📈 60分鐘線 K線圖", "📊 日線級別 K線圖 × 三大法人籌碼"])
            
            if "60分鐘線" in chart_type:
                df_selected_h = hourly_data[selected_ticker].dropna() if len(FILTERED_TICKERS) > 1 else hourly_data.dropna()
                if len(df_selected_h) >= 65:
                    df_selected_h['MA60'] = df_selected_h['Close'].rolling(window=60).mean()
                    low_60, high_60 = df_selected_h['Low'].rolling(window=60).min(), df_selected_h['High'].rolling(window=60).max()
                    df_selected_h['RSV'] = (((df_selected_h['Close'] - low_60) / (high_60 - low_60)) * 100).fillna(50)
                    df_selected_h['K'] = df_selected_h['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df_selected_h['D'] = df_selected_h['K'].ewm(alpha=1/3, adjust=False).mean()
                    df_plot_h = df_selected_h.tail(60)
                    fig_h = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                    fig_h.add_trace(go.Candlestick(x=df_plot_h.index, open=df_plot_h['Open'], high=df_plot_h['High'], low=df_plot_h['Low'], close=df_plot_h['Close'], name="60分K"), row=1, col=1)
                    fig_h.add_trace(go.Scatter(x=df_plot_h.index, y=df_plot_h['MA60'], name="60MA", line=dict(color='cyan', width=2.5)), row=1, col=1)
                    fig_h.add_trace(go.Scatter(x=df_plot_h.index, y=df_plot_h['K'], name="K", line=dict(color='red', width=1.5)), row=2, col=1)
                    fig_h.add_trace(go.Scatter(x=df_plot_h.index, y=df_plot_h['D'], name="D", line=dict(color='green', width=1.5)), row=2, col=1)
                    fig_h.update_layout(xaxis_rangeslider_visible=False, height=600, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_h, use_container_width=True)
            else:
                df_selected_d = daily_data[selected_ticker].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                df_selected_d['MA20'] = df_selected_d['Close'].rolling(window=20).mean()
                df_selected_d['MA60'] = df_selected_d['Close'].rolling(window=60).mean()
                df_selected_d = df_selected_d.tail(40)
                @st.cache_data(ttl=1800)
                def fetch_chip_data(sid):
                    fm_api = DataLoader()
                    start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
                    return fm_api.taiwan_stock_institutional_investors(stock_id=sid, start_date=start_date)
                try:
                    chip_df = fetch_chip_data(stock_id)
                    if not chip_df.empty:
                        chip_df['Net_Shares'] = (chip_df['buy'] - chip_df['sell']) / 1000
                        pivot_df = chip_df.pivot_table(index='date', columns='name', values='Net_Shares', aggfunc='sum').fillna(0)
                        pivot_df = pivot_df.rename(columns={'Foreign_Investor': '外資', 'Investment_Trust': '投信', 'Dealer_Self': '自營商'})
                        pivot_df.index = pd.to_datetime(pivot_df.index)
                        merged_df = df_selected_d.join(pivot_df, how='inner')
                        fig_canvas = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                        fig_canvas.add_trace(go.Candlestick(x=merged_df.index, open=merged_df['Open'], high=merged_df['High'], low=merged_df['Low'], close=merged_df['Close'], name="日K線"), row=1, col=1)
                        fig_canvas.add_trace(go.Scatter(x=merged_df.index, y=merged_df['MA20'], name="20MA", line=dict(color='orange', width=2)), row=1, col=1)
                        fig_canvas.add_trace(go.Scatter(x=merged_df.index, y=merged_df['MA60'], name="60MA", line=dict(color='limegreen', width=2.5)), row=1, col=1)
                        color_map = {'外資': '#1f77b4', '投信': '#ff7f0e', '自營商': '#2ca02c'}
                        for investor in ['外資', '投信', '自營商']:
                            if investor in merged_df.columns: fig_canvas.add_trace(go.Bar(x=merged_df.index, y=merged_df[investor], name=investor, marker_color=color_map[investor]), row=2, col=1)
                        fig_canvas.update_layout(xaxis_rangeslider_visible=False, barmode='group', height=600, margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified")
                        st.plotly_chart(fig_canvas, use_container_width=True)
                except Exception as e: st.error(f"籌碼加載中... {e}")

        # ─── 分頁四 ───
        with tab4:
            st.subheader("📊 已選 AI 細分供應鏈 - 當日量能與波段趨勢雙料排行 (Top 30)")
            volume_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_v = daily_data[ticker].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                    if df_v.empty: continue
                    df_v['MA20'] = df_v['Close'].rolling(window=20).mean(); df_v['MA60'] = df_v['Close'].rolling(window=60).mean()
                    today_v, yesterday_v = df_v.iloc[-1], df_v.iloc[-2]
                    p_change = ((today_v['Close'] - yesterday_v['Close']) / yesterday_v['Close']) * 100
                    volume_list.append({"代號": ticker, "股票名稱": FILTERED_STOCKS_DICT[ticker]['name'], "AI雷射族群": FILTERED_STOCKS_DICT[ticker]['group'], "今日收盤價": round(today_v['Close'], 2), "今日漲跌幅": f"{p_change:+.2f}%", "成交張數 (張)": int(today_v['Volume'] / 1000), "🌟 當前波段趨勢位階": diagnose_trend_status(today_v['Close'], today_v['MA20'], today_v['MA60'])})
                except: continue
                
            if volume_list: 
                v_df = pd.DataFrame(volume_list).sort_values(by="成交張數 (張)", ascending=False).reset_index(drop=True)
                v_df.index += 1
                top_30_df = v_df.head(30)
                st.dataframe(top_30_df, use_container_width=True)
                
                st.markdown("---")
                selected_t4 = st.selectbox("📊 選擇排行榜中的任意股票，直接看圖：", options=top_30_df["代號"].tolist(), format_func=lambda x: f"{x} {AI_STOCKS_DICT[x]['name']}", key="t4_select")
                t4_type = st.radio("選擇看圖規格：", ["📈 查看 60分鐘線 K線", "📊 查看 日線 × 法人籌碼圖"], key="t4_radio")
                
                if "60分鐘" in t4_type:
                    df_t4_h = hourly_data[selected_t4].dropna() if len(FILTERED_TICKERS) > 1 else hourly_data.dropna()
                    df_t4_h['MA60'] = df_t4_h['Close'].rolling(window=60).mean()
                    l_60, h_60 = df_t4_h['Low'].rolling(window=60).min(), df_t4_h['High'].rolling(window=60).max()
                    df_t4_h['RSV'] = (((df_t4_h['Close'] - l_60) / (h_60 - l_60)) * 100).fillna(50)
                    df_t4_h['K'] = df_t4_h['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df_t4_h['D'] = df_t4_h['K'].ewm(alpha=1/3, adjust=False).mean()
                    df_p_t4h = df_t4_h.tail(60)
                    fig_t4h = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                    fig_t4h.add_trace(go.Candlestick(x=df_p_t4h.index, open=df_p_t4h['Open'], high=df_p_t4h['High'], low=df_p_t4h['Low'], close=df_p_t4h['Close'], name="60分K"), row=1, col=1)
                    fig_t4h.add_trace(go.Scatter(x=df_p_t4h.index, y=df_p_t4h['MA60'], name="60MA", line=dict(color='cyan', width=2.5)), row=1, col=1)
                    fig_t4h.add_trace(go.Scatter(x=df_p_t4h.index, y=df_p_t4h['K'], name="K", line=dict(color='red', width=1.5)), row=2, col=1)
                    fig_t4h.add_trace(go.Scatter(x=df_p_t4h.index, y=df_p_t4h['D'], name="D", line=dict(color='green', width=1.5)), row=2, col=1)
                    fig_t4h.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_t4h, use_container_width=True)
                else:
                    df_t4_d = daily_data[selected_t4].dropna() if len(FILTERED_TICKERS) > 1 else daily_data.dropna()
                    df_t4_d['MA20'] = df_t4_d['Close'].rolling(window=20).mean()
                    df_t4_d['MA60'] = df_t4_d['Close'].rolling(window=60).mean()
                    df_p_t4d = df_t4_d.tail(40)
                    try:
                        fm_api = DataLoader()
                        c_df = fm_api.taiwan_stock_institutional_investors(stock_id=selected_t4.split('.')[0], start_date=(datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"))
                        if not c_df.empty:
                            c_df['Net_Shares'] = (c_df['buy'] - c_df['sell']) / 1000
                            p_df = c_df.pivot_table(index='date', columns='name', values='Net_Shares', aggfunc='sum').fillna(0).rename(columns={'Foreign_Investor':'外資','Investment_Trust':'投信','Dealer_Self':'自營商'})
                            p_df.index = pd.to_datetime(p_df.index)
                            m_df = df_p_t4d.join(p_df, how='inner')
                            fig_t4d = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_width=[0.35, 0.65])
                            fig_t4d.add_trace(go.Candlestick(x=m_df.index, open=m_df['Open'], high=m_df['High'], low=m_df['Low'], close=m_df['Close'], name="日K"), row=1, col=1)
                            fig_t4d.add_trace(go.Scatter(x=m_df.index, y=m_df['MA20'], name="20MA", line=dict(color='orange', width=2)), row=1, col=1)
                            fig_t4d.add_trace(go.Scatter(x=m_df.index, y=m_df['MA60'], name="60MA", line=dict(color='limegreen', width=2.5)), row=1, col=1)
                            for inv, clr in [('外資','#1f77b4'),('投信','#ff7f0e'),('自營商','#2ca02c')]:
                                if inv in m_df.columns: fig_t4d.add_trace(go.Bar(x=m_df.index, y=m_df[inv], name=inv, marker_color=clr), row=2, col=1)
                            fig_t4d.update_layout(xaxis_rangeslider_visible=False, barmode='group', height=500, margin=dict(l=10, r=10, t=10, b=10))
                            st.plotly_chart(fig_t4d, use_container_width=True)
                    except: st.error("籌碼維護中。")
