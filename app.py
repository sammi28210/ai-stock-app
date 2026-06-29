import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os

# ==========================================
# 1. 系統設定與資料庫載入
# ==========================================
st.set_page_config(page_title="AI 股市供應鏈監控系統", layout="wide", page_icon="🦅")

@st.cache_data
def load_stocks():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "stocks.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ 找不到 stocks.json，請確認檔案已上傳至 GitHub 根目錄。")
        st.stop()

AI_STOCKS_DICT = load_stocks()

# ==========================================
# 2. 側邊欄 (Sidebar) - 族群過濾系統
# ==========================================
st.sidebar.title("⚙️ 監控條件設定")

# 萃取所有不重複的群組名稱並排序
all_groups = sorted(list(set([info['group'] for info in AI_STOCKS_DICT.values()])))

# 側邊欄：選擇要監控的群組
selected_groups = st.sidebar.multiselect(
    "1️⃣ 選擇要監控的 AI 供應鏈族群：",
    options=all_groups,
    default=all_groups  # 預設全選
)

# 根據選擇過濾股票字典
FILTERED_STOCKS = {k: v for k, v in AI_STOCKS_DICT.items() if v['group'] in selected_groups}

st.sidebar.markdown("---")
st.sidebar.success(f"✅ 系統總檔數：{len(AI_STOCKS_DICT)} 檔")
st.sidebar.info(f"🔍 目前篩選顯示：{len(FILTERED_STOCKS)} 檔")

if not FILTERED_STOCKS:
    st.warning("請至少選擇一個族群來進行監控！")
    st.stop()

# ==========================================
# 3. 核心大腦：資料抓取與 AI 綜合診斷
# ==========================================
@st.cache_data(ttl=300) # 快取 5 分鐘，避免被 Yahoo 封鎖
def fetch_stock_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        return df
    except Exception:
        return None

def generate_ai_diagnosis(df, current_price):
    """計算技術指標並生成極度白話的診斷評語與防守線"""
    try:
        df['5MA'] = df['Close'].rolling(window=5).mean()
        df['20MA'] = df['Close'].rolling(window=20).mean()
        df['60MA'] = df['Close'].rolling(window=60).mean()
        df['Vol_5MA'] = df['Volume'].rolling(window=5).mean()
        
        ma5 = float(df['5MA'].iloc[-1]) if not pd.isna(df['5MA'].iloc[-1]) else current_price
        ma20 = float(df['20MA'].iloc[-1]) if not pd.isna(df['20MA'].iloc[-1]) else current_price
        ma60 = float(df['60MA'].iloc[-1]) if not pd.isna(df['60MA'].iloc[-1]) else current_price
        vol_today = float(df['Volume'].iloc[-1])
        vol_5ma = float(df['Vol_5MA'].iloc[-1]) if not pd.isna(df['Vol_5MA'].iloc[-1]) else vol_today
        
        # 關鍵價位：防守(近10日低)與壓力(近20日高)
        recent_high = float(df['High'].tail(20).max())
        recent_low = float(df['Low'].tail(10).min())
        
        # 乖離率
        bias_20 = ((current_price - ma20) / ma20) * 100 if ma20 != 0 else 0
        
        # 健康度計分
        score = 40
        if current_price > ma5: score += 15
        if current_price > ma20: score += 20
        if current_price > ma60: score += 15
        if vol_today > vol_5ma: score += 10
        
        # 白話文戰略判定
        if score >= 80:
            action = "🔥 【強勢抱牢 / 順勢操作】"
            summary = "多頭格局確立，主力資金進駐明顯。不預設高點，只要不跌破 5 日線就死抱不放。"
        elif score >= 60:
            action = "📈 【伺機買進 / 逢低佈局】"
            summary = "中長線趨勢偏多，短線可能處於震盪或量縮整理。若有拉回靠近 20 日線 (月線) 是不錯的切入防守點。"
        elif score >= 40:
            action = "👀 【觀望勿動 / 等待表態】"
            summary = "股價處於上有壓、下有撐的盤整泥淖中。沒有帶量突破前，請管好手不要輕易摸底進場。"
        else:
            action = "⚠️ 【嚴格停損 / 避開弱勢】"
            summary = "技術面全面轉弱，可能伴隨主力出貨。若已跌破防守線，請無條件斷尾求生，保留資金。"

        # 量價與主力推測
        if vol_today > vol_5ma * 1.5 and current_price > ma5:
            volume_status = "主力進場特徵：出現【價漲量增】攻擊訊號，籌碼換手積極。"
        elif vol_today < vol_5ma * 0.7 and current_price > ma20:
            volume_status = "籌碼沉澱特徵：出現【量縮價穩】，主力洗盤惜售，醞釀下一波。"
        elif vol_today > vol_5ma * 1.5 and current_price < df['Open'].iloc[-1]:
            volume_status = "警戒特徵：高檔【爆量收黑】，可能有主力或短線客倒貨，請小心。"
        else:
            volume_status = "量能平穩，無明顯異常主力洗盤跡象。"

        return {
            "score": score,
            "action": action,
            "summary": summary,
            "support": recent_low,
            "resistance": recent_high,
            "bias": bias_20,
            "volume_status": volume_status,
            "ma20": ma20
        }
    except Exception:
        return None

# ==========================================
# 4. 畫布渲染：統一規格的展開面板
# ==========================================
def render_stock_card(ticker, info):
    """將單一股票的報價與展開式診斷面板整合在一起"""
    df = fetch_stock_data(ticker)
    
    if df is None:
        st.error(f"⚠️ 無法獲取 {info['name']} ({ticker}) 的報價資料。")
        return
        
    current_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    diag = generate_ai_diagnosis(df, current_price)
    
    if diag is None:
        st.warning(f"資料不足以對 {info['name']} 進行深度診斷。")
        return

    color = "red" if change_pct > 0 else "green" if change_pct < 0 else "gray"
    sign = "+" if change_pct > 0 else ""
    
    # === 大標題：股名與即時報價 ===
    st.markdown(f"### 🟩 {info['name']} ({ticker}) : <span style='color:{color}'>{current_price:.2f} ({sign}{change_pct:.2f}%)</span>", unsafe_allow_html=True)
    
    # === 點擊展開的統一診斷規格 ===
    with st.expander(f"📊 點擊查看綜合 AI 診斷報告 ｜ 狀態: {diag['action']}"):
        st.markdown(f"#### 🏷️ 綜合評估")
        st.markdown(f"**健康分數：** `{diag['score']} / 100`")
        st.markdown(f"**AI 結論：** {diag['summary']}")
        
        st.markdown("---")
        st.markdown(f"#### 🛡️ 預防退路與關鍵價位")
        st.markdown(f"🚨 **最後防守線 (停損點)：** **`{diag['support']:.2f}` 元** *(近10日低點，跌破請嚴格執行出場)*")
        dist_to_res = ((diag['resistance'] - current_price) / current_price) * 100 if current_price != 0 else 0
        st.markdown(f"🎯 **近期壓力區 (停利點)：** **`{diag['resistance']:.2f}` 元** *(距離目前約向上 {dist_to_res:.1f}%)*")
        
        st.markdown("---")
        st.markdown(f"#### 📈 技術面與主力推測")
        bias_str = "✅ 正常範圍"
        if diag['bias'] > 10: bias_str = "🔥 短線過熱 (隨時拉回)"
        elif diag['bias'] < -10: bias_str = "❄️ 超跌區 (有反彈契機)"
            
        st.markdown(f"- **乖離風險：** 目前距月線乖離率 `{diag['bias']:.2f}%` ➜ **{bias_str}**")
        st.markdown(f"- **趨勢狀態：** 股價目前 {'大於' if current_price > diag['ma20'] else '小於'} 月線 ({diag['ma20']:.2f})")
        st.markdown(f"- **主力動能：** {diag['volume_status']}")
        
        st.markdown("---")
        st.markdown(f"#### 💡 族群連動")
        st.info(f"所屬板塊：**{info['group']}**")

# ==========================================
# 5. 前端介面：維持原本的四個分頁架構
# ==========================================
st.title("🦅 AI 供應鏈戰術儀表板")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 單檔速查 (首頁)", 
    "🗂️ 族群資金輪動 (分頁二)", 
    "🔥 強勢突破監控 (分頁三)", 
    "🏆 AI 綜合觀測站 (最後一頁)"
])

# ----------------- 分頁一：單檔速查 -----------------
with tab1:
    st.markdown("### 🎯 精準查詢")
    search_query = st.text_input("請輸入台股四位數代號 (例如: 2330) 或名稱：")
    
    if search_query:
        found = False
        for ticker, info in FILTERED_STOCKS.items():
            if search_query in ticker or search_query in info['name']:
                render_stock_card(ticker, info)
                found = True
        if not found:
            st.warning("⚠️ 找不到相符的標的，請確認代號，或檢查側邊欄是否未勾選該族群。")

# ----------------- 分頁二：族群資金輪動 -----------------
with tab2:
    st.markdown("### 🗂️ 檢視單一供應鏈族群")
    if selected_groups:
        target_group = st.selectbox("1. 選擇要檢視的次產業：", selected_groups)
        
        # 將該族群內的所有標的列為下拉選單 (避免一次載入太多 API 當機)
        group_stocks = {k: v for k, v in FILTERED_STOCKS.items() if v['group'] == target_group}
        stock_options = [""] + [f"{v['name']} ({k})" for k, v in group_stocks.items()]
        
        selected_stock_str = st.selectbox("2. 選擇要深入診斷的個股：", stock_options)
        
        if selected_stock_str != "":
            ticker_to_show = selected_stock_str.split("(")[1].replace(")", "")
            render_stock_card(ticker_to_show, group_stocks[ticker_to_show])

# ----------------- 分頁三：強勢突破監控 -----------------
with tab3:
    st.markdown("### 🔥 盤中強勢異動掃描")
    st.write("自動篩選：今天股價在月線之上，且成交量大於 5日均量的轉強標的。")
    
    if st.button("🚀 啟動掃描 (可能需要1-2分鐘)"):
        with st.spinner("正在逐檔過濾籌碼與量價..."):
            hit_count = 0
            for ticker, info in list(FILTERED_STOCKS.items()):
                df = fetch_stock_data(ticker)
                if df is not None and len(df) > 20:
                    cp = float(df['Close'].iloc[-1])
                    ma20 = float(df['Close'].rolling(20).mean().iloc[-1])
                    vol_today = float(df['Volume'].iloc[-1])
                    vol_5ma = float(df['Volume'].rolling(5).mean().iloc[-1])
                    
                    if cp > ma20 and vol_today > (vol_5ma * 1.2):
                        render_stock_card(ticker, info)
                        hit_count += 1
            
            if hit_count == 0:
                st.info("目前無符合強勢突破條件的標的。")

# ----------------- 最終頁：核心觀測站 -----------------
with tab4:
    st.markdown("### 🏆 每日自選觀察清單")
    st.write("你的重點權值股與核心戰力總覽：")
    
    # 自訂核心觀察名單
    default_watch_list = ["2330.TW", "2317.TW", "2382.TW", "3231.TW", "3017.TW", "2454.TW"]
    
    for ticker in default_watch_list:
        if ticker in FILTERED_STOCKS:
            render_stock_card(ticker, FILTERED_STOCKS[ticker])

