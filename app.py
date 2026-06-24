import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 保持大器寬版配置
st.set_page_config(page_title="台股AI全鏈監控系統", layout="wide")
st.title("🦅 台股 AI 全產業鏈 100+ 大軍終極永久看板")
st.caption("雲端純淨版：無圖表負擔 × 專注即時動態篩選 × 內建族群與個股雙重資金診斷雷達")

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
    '2449.TW': {'name': '京元電子', 'group': '08. 先裝封測 (CoWoS)'},
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

st.sidebar.header("🎯 AI 供應鏈群組過濾")
all_available_groups = sorted(list(set([v['group'] for v in AI_STOCKS_DICT.values()])))
selected_groups = st.sidebar.multiselect("選擇監控群組：", options=all_available_groups, default=all_available_groups)
FILTERED_STOCKS_DICT = {k: v for k, v in AI_STOCKS_DICT.items() if v['group'] in selected_groups}
FILTERED_TICKERS = list(FILTERED_STOCKS_DICT.keys())

@st.cache_data(ttl=900)
def fetch_all_data(tickers):
    if not tickers: return None, None
    try:
        import requests
        clean_session = requests.Session()
        clean_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        hourly = yf.download(tickers, period="2mo", interval="1h", group_by='ticker', progress=False, threads=False, session=clean_session)
        daily = yf.download(tickers, period="8mo", interval="1d", group_by='ticker', progress=False, threads=False, session=clean_session)
        return hourly, daily
    except:
        return None, None

if FILTERED_TICKERS:
    with st.spinner("⚡ 正在安全抓取 100+ 檔台股大軍數據，並啟動全功能計算..."):
        hourly_data, daily_data = fetch_all_data(FILTERED_TICKERS)
    
    if hourly_data is not None and daily_data is not None and not hourly_data.empty:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔥 60分線 666 戰法", 
            "🛡️ 均線防守 & 低檔反彈選股", 
            "💎 個股智慧狀態診斷", 
            "📊 AI大軍量能與趨勢排行",
            "💰 族群資金輪動監控"
        ])
        
        is_multi = isinstance(hourly_data.columns, pd.MultiIndex)
        
        # ─── Tab 1：60分線篩選 ───
        with tab1:
            st.subheader("🤖 微族群過濾 - 60分鐘線極短線動能篩選")
            matches = []
            for ticker in FILTERED_TICKERS:
                try:
                    df = hourly_data[ticker].dropna() if is_multi else hourly_data.dropna()
                    if len(df) < 65: continue
                    df['MA60'] = df['Close'].rolling(window=60).mean()
                    low_60, high_60 = df['Low'].rolling(window=60).min(), df['High'].rolling(window=60).max()
                    df['RSV'] = (((df['Close'] - low_60) / (high_60 - low_60)) * 100).fillna(50)
                    df['K'] = df['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df['D'] = df['K'].ewm(alpha=1/3, adjust=False).mean()
                    today = df.iloc[-1]
                    if today['Close'] > today['MA60'] and today['K'] > today['D']:
                        df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                        df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                        df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                        p_tod = df_d.iloc[-1]
                        trend_lbl = diagnose_trend_status(p_tod['Close'], p_tod['MA20'], p_tod['MA60'])
                        matches.append({"代號": ticker, "股票名稱": AI_STOCKS_DICT[ticker]['name'], "AI細分族群": AI_STOCKS_DICT[ticker]['group'], "當前價": round(today['Close'], 2), "波段趨勢位階": trend_lbl})
                except: continue
            if matches: 
                st.success(f"🎯 篩選成功！共有 {len(matches)} 檔符合條件。")
                st.dataframe(pd.DataFrame(matches).reset_index(drop=True), use_container_width=True)
            else: st.info("目前範圍內無標的符合條件。")
            
        # ─── Tab 2：均線防守選股 ───
        with tab2:
            st.subheader("🔍 日線級別 - 中長線均線防守診斷")
            correction_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    p_today = df_d.iloc[-1]
                    if p_today['Close'] < p_today['MA20'] or p_today['Close'] < p_today['MA60']:
                        diagnose = diagnose_trend_status(p_today['Close'], p_today['MA20'], p_today['MA60'])
                        correction_list.append({"代號": ticker, "股票名稱": FILTERED_STOCKS_DICT[ticker]['name'], "AI細分族群": FILTERED_STOCKS_DICT[ticker]['group'], "今日收盤": round(p_today['Close'], 2), "趨勢診斷": diagnose})
                except: continue
            if correction_list: 
                st.warning(f"⚠️ 警示：有 {len(correction_list)} 檔標的回檔修正中：")
                st.dataframe(pd.DataFrame(correction_list).reset_index(drop=True), use_container_width=True)
            
            st.markdown("---")
            st.subheader("🌟 智慧自動選股：鎖定安全打底準備反彈區")
            rebound_matches = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_r = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
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

        # ─── Tab 3：個股大字體純數據診斷 ───
        with tab3:
            st.subheader("💎 個股當前技術面核心數據查閱")
            selector_options = {t: f"{t} {FILTERED_STOCKS_DICT[t]['name']} ({FILTERED_STOCKS_DICT[t]['group']})" for t in FILTERED_TICKERS}
            selected_ticker = st.selectbox("請選擇你想查看的 AI 股：", options=FILTERED_TICKERS, format_func=lambda x: selector_options[x])
            
            try:
                df_d = daily_data[selected_ticker].dropna() if is_multi else daily_data.dropna()
                df_h = hourly_data[selected_ticker].dropna() if is_multi else hourly_data.dropna()
                
                df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                df_h['MA60'] = df_h['Close'].rolling(window=60).mean()
                
                tod_d = df_d.iloc[-1]
                yes_d = df_d.iloc[-2]
                tod_h = df_h.iloc[-1]
                
                p_close = tod_h['Close']
                p_change = ((p_close - yes_d['Close']) / yes_d['Close']) * 100
                trend_lbl = diagnose_trend_status(tod_d['Close'], df_d['MA20'].iloc[-1], df_d['MA60'].iloc[-1])
                
                st.metric(label="📊 當前即時股價", value=f"{p_close:.2f} 元", delta=f"{p_change:+.2f}%")
                
                current_ma60_val = df_h['MA60'].iloc[-1]
                if p_close > current_ma60_val:
                    ma_status_text = f"高於 60MA ({current_ma60_val:.1f}) ✅強勢"
                else:
                    ma_status_text = f"低於 60MA ({current_ma60_val:.1f}) ❌弱勢"
                
                with st.container(border=True):
                    st.markdown(f"**🏢 所屬供應鏈族群：** {FILTERED_STOCKS_DICT[selected_ticker]['group']}")
                    st.markdown(f"**🎯 波段中長線趨勢：** {trend_lbl}")
                    st.markdown(f"**⏱️ 60分K戰法位階：** 目前價格 {ma_status_text}")
                    st.markdown(f"**📦 今日概估成交張數：** {int(tod_d['Volume']/1000)} 張")
                    st.markdown(f"**📅 數據最後同步時間：** {tod_h.name.strftime('%Y-%m-%d %H:%M') if hasattr(tod_h.name, 'strftime') else lod_h.name}")
            except:
                st.info("該股數據整合中...")

        # ─── Tab 4：量能與趨勢排行 ───
        with tab4:
            st.subheader("📊 已選 AI 細分供應鏈 - 當日量能與波段趨勢雙料排行 (Top 30)")
            volume_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_v = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    if df_v.empty: continue
                    df_v['MA20'] = df_v['Close'].rolling(window=20).mean(); df_v['MA60'] = df_v['Close'].rolling(window=60).mean()
                    today_v, yesterday_v = df_v.iloc[-1], df_v.iloc[-2]
                    p_change = ((today_v['Close'] - yesterday_v['Close']) / yesterday_v['Close']) * 100
                    volume_list.append({"代號": ticker, "股票名稱": FILTERED_STOCKS_DICT[ticker]['name'], "AI雷射族群": FILTERED_STOCKS_DICT[ticker]['group'], "今日收盤": round(today_v['Close'], 2), "今日漲跌幅": f"{p_change:+.2f}%", "成交量 (張)": int(today_v['Volume'] / 1000), "🌟 當前波段趨勢": diagnose_trend_status(today_v['Close'], today_v['MA20'], today_v['MA60'])})
                except: continue
                
            if volume_list: 
                v_df = pd.DataFrame(volume_list).sort_values(by="成交量 (張)", ascending=False).reset_index(drop=True)
                v_df.index += 1
                top_30_df = v_df.head(30)
                st.dataframe(top_30_df, use_container_width=True)

        # ─── Tab 5：族群資金流向 ＋ 個股自動化雙重白話文診斷 ───
        with tab5:
            st.subheader("💰 🎯 AI 次族群資金流向與輪動警報")
            
            group_flows = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_ticker = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    if len(df_ticker) < 6: continue
                    
                    df_v = df_ticker.copy()
                    df_v['Value'] = df_v['Close'] * df_v['Volume']
                    df_v['Value_MA5'] = df_v['Value'].rolling(window=5).mean()
                    df_v['Vol_MA5'] = df_v['Volume'].rolling(window=5).mean() # 額外加算 5日均量
                    
                    today_v = df_v.iloc[-1]
                    yesterday_v = df_v.iloc[-2]
                    p_change = ((today_v['Close'] - yesterday_v['Close']) / yesterday_v['Close']) * 100
                    
                    # 計算單股今日量能相較 5日均量的放大倍數
                    stock_vol_ratio = today_v['Volume'] / today_v['Vol_MA5'] if today_v['Vol_MA5'] > 0 else 1.0
                    
                    group_flows.append({
                        "ticker": ticker,
                        "name": AI_STOCKS_DICT[ticker]['name'],
                        "group": FILTERED_STOCKS_DICT[ticker]['group'],
                        "value_today": today_v['Value'],
                        "value_ma5": today_v['Value_MA5'],
                        "p_change": p_change,
                        "price": today_v['Close'],
                        "volume": today_v['Volume'],
                        "stock_vol_ratio": stock_vol_ratio # 傳遞單股量能倍數
                    })
                except: continue
                
            if group_flows:
                flow_df = pd.DataFrame(group_flows)
                
                agg_df = flow_df.groupby("group").agg({
                    "value_today": "sum",
                    "value_ma5": "sum",
                    "p_change": "mean"
                }).reset_index()
                
                agg_df["今日成交額 (億元)"] = round(agg_df["value_today"] / 100000000, 2)
                agg_df["量能放大倍數 (較5日)"] = round(agg_df["value_today"] / agg_df["value_ma5"], 2)
                agg_df["族群平均漲跌"] = agg_df["p_change"].map(lambda x: f"{x:+.2f}%")
                
                def judge_flow_status(row):
                    chg = row["p_change"]
                    ratio = row["量能放大倍數 (較5日)"]
                    if chg > 0.4 and ratio >= 1.2: return "🔥 資金大舉點火（價量齊揚）"
                    elif chg > 0 and ratio >= 0.9: return "📈 資金穩定續留（溫和推升）"
                    elif -0.4 <= chg <= 0.4 and ratio < 0.8: return "⏳ 資金休兵觀望（縮量沉悶）"
                    elif chg < -0.4 and ratio >= 1.2: return "🚨 籌碼大舉撤退（放量下跌）"
                    elif chg < 0 and ratio >= 0.9: return "📉 主力拉回調節（震盪修正）"
                    else: return "🌀 橫盤量縮整理"
                    
                agg_df["🔮 資金流向診斷"] = agg_df.apply(judge_flow_status, axis=1)
                
                output_flow = agg_df[["group", "族群平均漲跌", "今日成交額 (億元)", "量能放大倍數 (較5日)", "🔮 資金流向診斷"]].copy()
                output_flow.columns = ["AI 細分次族群", "族群平均漲跌", "今日總成交額 (億元)", "量能放大倍數 (較5日)", "🔮 主力資金流向診斷"]
                
                sort_by = st.radio("排序依據：", ["按成交金額（看誰吸金最多）", "按量能放大倍數（看誰剛被火速點火）"], horizontal=True)
                if "成交金額" in sort_by:
                    output_flow = output_flow.sort_values(by="今日總成交額 (億元)", ascending=False).reset_index(drop=True)
                else:
                    output_flow = output_flow.sort_values(by="量能放大倍數 (較5日)", ascending=False).reset_index(drop=True)
                    
                output_flow.index += 1
                st.dataframe(output_flow, use_container_width=True)
                
                # ─── 下半部：成分股解密 ＋ 🌟完美追加最右側個股白話文講解 ───
                st.markdown("---")
                st.subheader("🔍 族群個股成分明細")
                
                available_groups = sorted(agg_df["group"].tolist())
                selected_flow_group = st.selectbox("📱 點擊選擇想深入查閱成分股的 AI 族群：", options=available_groups)
                
                detail_df = flow_df[flow_df["group"] == selected_flow_group].copy()
                detail_df["今日收盤價"] = detail_df["price"].round(2)
                detail_df["今日漲跌幅"] = detail_df["p_change"].map(lambda x: f"{x:+.2f}%")
                detail_df["成交量 (張)"] = (detail_df["volume"] / 1000).astype(int)
                detail_df["個股成交額 (億元)"] = round(detail_df["value_today"] / 100000000, 2)
                
                # 🌟🌟🌟 核心智慧判定：自動生成單股白話文診斷 🌟🌟🌟
                def judge_single_stock_status(row):
                    chg = row["p_change"]
                    v_ratio = row["stock_vol_ratio"]
                    
                    if chg > 1.0 and v_ratio >= 1.2: return "🔥 主力強勢鎖定（多頭發動）"
                    elif chg > 0 and v_ratio >= 0.9: return "📈 籌碼溫和推升（穩健向上）"
                    elif chg > 0 and v_ratio < 0.9: return "⚠️ 價入量縮拉高（動能略嫌不足）"
                    elif -1.0 <= chg <= 1.0 and v_ratio < 0.8: return "⏳ 縮量橫盤觀望（靜待變盤）"
                    elif chg < -1.0 and v_ratio >= 1.2: return "🚨 籌碼驚慌出貨（主力倒貨）"
                    elif chg < 0 and v_ratio >= 0.9: return "📉 跌勢伴隨量能（破位修正）"
                    else: return "🌀 區間常態波動"
                
                detail_df["🔮 個股籌碼診斷說明"] = detail_df.apply(judge_single_stock_status, axis=1)
                
                output_detail = detail_df[["ticker", "name", "今日收盤價", "今日漲跌幅", "成交量 (張)", "個股成交額 (億元)", "🔮 個股籌碼診斷說明"]]
                output_detail.columns = ["股票代號", "股票名稱", "今日收盤價", "今日漲跌幅", "成交量 (張)", "個股成交額 (億元)", "🔮 個股籌碼診斷說明"]
                
                output_detail = output_detail.sort_values(by="個股成交額 (億元)", ascending=False).reset_index(drop=True)
                output_detail.index += 1
                
                st.success(f"📊 已成功解密【{selected_flow_group}】成分股明細與即時籌碼診斷：")
                st.dataframe(output_detail, use_container_width=True)
            else:
                st.info("暫無足夠歷史數據計算流向。")
    else:
        st.warning("⏳ 雲端伺服器排隊抓取數據中，請稍候重整網頁。")
