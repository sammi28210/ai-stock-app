import streamlit as st
import yfinance as yf
import pandas as pd

# 設置頁面
st.set_page_config(page_title="AI 300大軍監控系統", layout="wide")
st.title("🦅 台股 AI 全產業鏈 300+ 大軍終極雷達")

# 1. 庫存管理
if 'my_portfolio' not in st.session_state:
    st.session_state.my_portfolio = pd.DataFrame([
        {"代號": "2356.TW", "買入成本": 70.57},
        {"代號": "2327.TW", "買入成本": 1010.00},
        {"代號": "2308.TW", "買入成本": 385.50}
    ])

# 2. 核心字典：這裡就是你的軍火庫，之後要新增股票，照著格式在裡面加一行即可
AI_STOCKS_DICT = {
    '2330.TW': {'name': '台積電', 'group': '01. 晶圓代工'},
    '2317.TW': {'name': '鴻海', 'group': '02. AI伺服器代工'},
    '2382.TW': {'name': '廣達', 'group': '02. AI伺服器代工'},
    '3231.TW': {'name': '緯創', 'group': '02. AI伺服器代工'},
    '2356.TW': {'name': '英業達', 'group': '02. AI伺服器代工'},
    '3661.TW': {'name': '世芯-KY', 'group': '03. 矽智財'},
    '3017.TW': {'name': '奇鋐', 'group': '04. 散熱'},
    '3324.TW': {'name': '雙鴻', 'group': '04. 散熱'},
    '1519.TW': {'name': '華城', 'group': '05. 重電'},
    '3029.TW': {'name': '零壹', 'group': '06. 資安'},
    '3008.TW': {'name': '大立光', 'group': '07. 光學'}
}

# 3. 功能：數據下載
@st.cache_data(ttl=600)
def get_data(tickers):
    return yf.download(tickers, period="1mo", interval="1d", group_by='ticker', progress=False)

# 4. 執行畫面佈局
tabs = st.tabs(["🚀 精選買入", "🔄 資金地圖", "📊 數據中心", "📱 持股防守"])

# --- 頁面邏輯 ---

with tabs[0]:
    st.subheader("🚀 今日精選潛力股")
    st.write("系統已啟動，正在過濾強勢股...")
    # 在這裡顯示你的精選篩選結果

with tabs[1]:
    st.subheader("🔄 資金換手地圖")
    code = st.text_input("輸入代號查詢 (例如: 2330.TW)")
    if code:
        st.write(f"正在為你診斷 {code}...")
        # 這裡放置你的診斷邏輯

with tabs[2]:
    st.subheader("📊 300 檔大軍數據中心")
    st.write(f"目前資料庫中共有 {len(AI_STOCKS_DICT)} 檔標的")
    # 顯示字典內容，證明資料已經載入
    st.table(pd.DataFrame(AI_STOCKS_DICT).T)

with tabs[3]:
    st.subheader("📱 持股防守區域")
    edited_df = st.data_editor(st.session_state.my_portfolio, num_rows="dynamic")
    st.session_state.my_portfolio = edited_df
    if st.button("儲存持股變更"):
        st.success("持股已更新！")

# 5. 診斷判斷式 (這段邏輯確保語法正確)
def get_action(price, ma):
    if price > ma and price > 0:
        return "🔥 強勢"
    else:
        return "⏳ 觀望"
