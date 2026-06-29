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
        st.error("❌ 系統嚴重錯誤：找不到 stocks.json。請確認該檔案已上傳至 GitHub 根目錄。")
        st.stop()

AI_STOCKS_DICT = load_stocks()

# ==========================================
# 2. 側邊欄 (Sidebar) - 族群過濾系統
# ==========================================
st.sidebar.title("⚙️ 監控條件設定")

all_groups = sorted(list(set([info['group'] for info in AI_STOCKS_DICT.values()])))

selected_groups = st.sidebar.multiselect(
    "1️⃣ 選擇要監控的 AI 供應鏈族群：",
    options=all_groups,
    default=all_groups
)

FILTERED_STOCKS = {k: v for k, v in AI_STOCKS_DICT.items() if v['group'] in selected_groups}

st.sidebar.markdown("---")
st.sidebar.success(f"✅ 資料庫總檔數：{len(AI_STOCKS_DICT)} 檔")
st.sidebar.info(f"🔍 目前篩選顯示：{len(FILTERED_STOCKS)} 檔")

if not FILTERED_STOCKS:
    st.warning("⚠️ 請從左側選單至少選擇一個族群來進行監控！")
    st.stop()

# ==========================================
# 3. 核心大腦：AI 綜合診斷演算法
# ==========================================
@st.cache_data(ttl=300) 
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
    """計算技術指標並生成極度白話的診斷與防守線"""
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
        
        recent_high = float(df['High'].tail(20).max())
        recent_low = float(df['Low'].tail(10).min())
        
        bias_20 = ((current_price - ma20) / ma20) * 100 if ma20 != 0 else 0
        
        score = 40 
        if current_price > ma5: score += 15
        if current_price > ma20: score += 20
        if current_price > ma60: score += 15
        if vol_today > vol_5ma: score += 10
        
        if score >= 80:
            action = "🔥 【強勢抱牢 / 順勢操作】"
            summary = "多頭格局確立，主力資金進駐明顯。不預設高點，只要不跌破 5 日均線就死抱不放，讓利潤奔跑。"
        elif score >= 60:
            action = "📈 【伺機買進 / 逢低佈局】"
            summary = "中長線趨勢偏多，短線可能處於震盪或量縮整理。若有拉回靠近 20 日線 (月線) 附近，是不錯的切入防守點。"
        elif score >= 40:
            action = "👀 【觀望勿動 / 等待表態】"
            summary = "股價處於上有壓、下有撐的盤整泥淖中。在沒有出現「帶量突破」的明確訊號前，請管好手不要輕易摸底進場。"
        else:
            action = "⚠️ 【嚴格停損 / 避開弱勢】"
            summary = "技術面全面轉弱，可能伴隨主力出貨或棄守。若已跌破防守線，請無條件斷尾求生，保留資金。"

        if vol_today > vol_5ma * 1.5 and current_price > ma5:
            volume_status = "主力進場特徵：出現【價漲量增】的攻擊訊號，籌碼換手積極，動能強勁。"
        elif vol_today < vol_5ma * 0.7 and current_price > ma20:
            volume_status = "籌碼沉澱特徵：出現【量縮價穩】，顯示主力洗盤惜售，賣壓減輕，正在醞釀下一波攻勢。"
        elif vol_today > vol_5ma * 1.5 and current_price < df['Open'].iloc[-1]:
            volume_status = "警戒特徵：高檔出現【爆量收黑】(避雷針)，可能有大戶或短線客正在獲利了結倒貨，請高度警戒。"
        else:
            volume_status = "量能平穩，無明顯異常洗盤或倒貨跡象，順勢觀察即可。"

        return {
            "score": score, "action": action, "summary": summary,
            "support": recent_low, "resistance": recent_high,
            "bias": bias_20, "volume_status": volume_status, "ma20": ma20
        }
    except Exception:
        return None

# ==========================================
# 4. UI 渲染模組：統一規格展開面板
# ==========================================
def render_stock_card(ticker, info):
    df = fetch_stock_data(ticker)
    
    if df is None:
        st.error(f"❌ 暫時無法獲取 {info['name']} ({ticker}) 的報價資料。")
        return
        
    current_price = float(df['Close'].iloc[-1])
    prev_price = float(df['Close'].iloc[-2])
    change_pct = ((current_price - prev_price) / prev_price) * 100
    
    diag = generate_ai_diagnosis(df, current_price)
    if diag is None: return

    color = "red" if change_pct > 0 else "green" if change_pct < 0 else "gray"
    sign = "+" if change_pct > 0 else ""
    
    with st.expander(f"📊 點擊查看【{info['name']} ({ticker})】綜合 AI 診斷 ｜ 現價: {current_price:.2f} ({sign}{change_pct:.2f}%) ｜ 狀態: {diag['action']}"):
        
        st.markdown(f"#### 🏷️ AI 綜合判定與行動指南")
        st.markdown(f"**健康度分數：** `{diag['score']} / 100`")
        st.markdown(f"**AI 戰略總結：** {diag['summary']}")
        
        st.markdown("---")
        st.markdown(f"#### 🛡️ 預防退路與關鍵價位")
        st.markdown(f"🚨 **最後防守線 (嚴格停損點)：** **`{diag['support']:.2f}` 元** *(近10日低點，一旦跌破請立即執行出場紀律)*")
        dist_to_res = ((diag['resistance'] - current_price) / current_price) * 100 if current_price != 0 else 0
        st.markdown(f"🎯 **近期壓力區 (短期停利點)：** **`{diag['resistance']:.2f}` 元** *(距離目前價格約向上 {dist_to_res:.1f}%)*")
        
        st.markdown("---")
        st.markdown(f"#### 📈 技術面與主力籌碼推測")
        if diag['bias'] > 12: bias_str = "🔥 短線嚴重過熱，隨時有獲利了結賣壓 (拉回風險極高)"
        elif diag['bias'] > 6: bias_str = "⚠️ 短線偏熱，不建議空手追高"
        elif diag['bias'] < -10: bias_str = "❄️ 超跌區間，隨時醞釀技術性反彈"
        else: bias_str = "✅ 乖離率於安全健康範圍"
            
        st.markdown(f"- **乖離風險：** 目前距離月線乖離率 `{diag['bias']:.2f}%` ➜ **{bias_str}**")
        st.markdown(f"- **趨勢狀態：** 股價目前 **{'大於' if current_price > diag['ma20'] else '小於'}** 月線防守基準 ({diag['ma20']:.2f})")
        st.markdown(f"- **動能解析：** {diag['volume_status']}")
        
        st.markdown("---")
        st.markdown(f"#### 💡 族群連動狀態")
        st.info(f"所屬供應鏈板塊：**{info['group']}**")

# ==========================================
# 5. 前端介面：維持原本的 9 個分頁架構
# ==========================================
st.title("🦅 AI 供應鏈戰術指揮中心")

tabs = st.tabs([
    "首頁", 
    "分頁二", 
    "分頁三", 
    "分頁四", 
    "分頁五", 
    "分頁六", 
    "分頁七", 
    "分頁八", 
    "最後一頁"
])

# ----------------- 分頁一 (首頁)：單檔速查 -----------------
with tabs[0]:
    st.markdown("### 🎯 首頁：單檔標的深度診斷")
    search_query = st.text_input("請輸入台股四位數代號 (例如: 2330) 或公司名稱：")
    
    if search_query:
        found = False
        for ticker, info in FILTERED_STOCKS.items():
            if search_query in ticker or search_query in info['name']:
                render_stock_card(ticker, info)
                found = True
        if not found:
            st.warning("⚠️ 查無此標的。請確認代碼或左側邊欄勾選狀態。")

# ----------------- 分頁二：族群資金輪動 -----------------
with tabs[1]:
    st.markdown("### 🗂️ 分頁二：次產業族群輪動")
    if selected_groups:
        target_group = st.selectbox("1. 選擇要檢視的次產業族群：", selected_groups)
        group_stocks = {k: v for k, v in FILTERED_STOCKS.items() if v['group'] == target_group}
        stock_options = [""] + [f"{v['name']} ({k})" for k, v in group_stocks.items()]
        
        selected_stock_str = st.selectbox("2. 選擇要展開診斷的標的：", stock_options)
        
        if selected_stock_str != "":
            ticker_to_show = selected_stock_str.split("(")[1].replace(")", "")
            render_stock_card(ticker_to_show, group_stocks[ticker_to_show])

# ----------------- 分頁三：強勢突破監控 -----------------
with tabs[2]:
    st.markdown("### 🔥 分頁三：盤中強勢異動掃描")
    st.write("自動篩選：今天股價站上月線之上，且成交量大於 5日均量的轉強標的。")
    
    if st.button("🚀 啟動強勢股掃描"):
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

# ----------------- 分頁四：(保留區) -----------------
with tabs[3]:
    st.markdown("### 📉 分頁四：弱勢跌破警示")
    st.write("系統架構已為您保留。這裡未來可以放置跌破季線或均線空頭排列的預警邏輯。")

# ----------------- 分頁五：(保留區) -----------------
with tabs[4]:
    st.markdown("### 📊 分頁五：成交量異常偵測")
    st.write("系統架構已為您保留。這裡未來可以放置爆量收黑或爆量長紅的專屬篩選器。")

# ----------------- 分頁六：(保留區) -----------------
with tabs[5]:
    st.markdown("### 📈 分頁六：乖離率過高預警")
    st.write("系統架構已為您保留。這裡未來可以專門列出正乖離大於 15% 的風險標的。")

# ----------------- 分頁七：(保留區) -----------------
with tabs[6]:
    st.markdown("### ❄️ 分頁七：乖離率過低尋寶")
    st.write("系統架構已為您保留。這裡未來可以放置負乖離極大，醞釀反彈的標的。")

# ----------------- 分頁八：(保留區) -----------------
with tabs[7]:
    st.markdown("### 💡 分頁八：AI 綜合給分排行")
    st.write("系統架構已為您保留。這裡未來可以製作全市場健康度分數排行榜。")

# ----------------- 最終頁 (分頁九)：核心觀測站 -----------------
with tabs[8]:
    st.markdown("### 🏆 最後一頁：核心自選觀測站")
    st.write("以下是你預設重點監控的標的，一鍵展開所有狀態：")
    
    default_watch_list = ["2330.TW", "2317.TW", "2454.TW", "2382.TW", "3231.TW", "3017.TW"]
    
    for ticker in default_watch_list:
        if ticker in FILTERED_STOCKS:
            render_stock_card(ticker, FILTERED_STOCKS[ticker])

