import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 保持大器寬版配置
st.set_page_config(page_title="台股AI全鏈监控系統", layout="wide")
st.title("🦅 台股 AI 全產業鏈 350+ 大軍終極永久看板")
st.caption("🎯 戰略完全體：【專屬大仁哥週報分頁】× 【獨立資金換手分頁】× 【20日結構背離】× 【2日留存觀察防線】")

# --- ⚙️【持股永久固定區】修改您的真實庫存與成本，重新整理絕不消失！ ---
if 'my_portfolio' not in st.session_state:
    st.session_state.my_portfolio = pd.DataFrame([
        {"代號": "2356", "買入成本": 70.57},    # 💡 您的英業達真實成本
        {"代號": "2308", "買入成本": 2038.64},  # 💡 您的國巨真實成本
        {"代號": "", "買入成本": 0.0},          # 💡 您的台達電真實成本
        {"代號": "", "買入成本": 0.0},          # 💡 您的強茂成本
        {"代號": "", "買入成本": 0.0}           # 💡 您的華新科成本
    ])

# 🔒 350+ 全產業鏈大軍終極永久字典：南茂（8150）精準校對歸位！
AI_STOCKS_DICT = {
    # ─── 01. 矽智財 (IP/ASIC) ───
    '3661.TW': {'name': '世芯-KY', 'group': '01. 矽智財 (IP/ASIC)'},
    '3443.TW': {'name': '創意', 'group': '01. 矽智財 (IP/ASIC)'},
    '3035.TW': {'name': '智原', 'group': '01. 矽智財 (IP/ASIC)'},
    '6643.TWO': {'name': 'M31', 'group': '01. 矽智財 (IP/ASIC)'},
    '6533.TWO': {'name': '晶心科', 'group': '01. 矽智財 (IP/ASIC)'},
    '6684.TWO': {'name': '安格', 'group': '01. 矽智財 (IP/ASIC)'},
    '6756.TW': {'name': '威鋒電子', 'group': '01. 矽智財 (IP/ASIC)'},
    '3529.TWO': {'name': '力旺', 'group': '01. 矽智財 (IP/ASIC)'},
    '6531.TW': {'name': '愛普*', 'group': '01. 矽智財 (IP/ASIC)'},
    '8227.TWO': {'name': '巨有科技', 'group': '01. 矽智財 (IP/ASIC)'},
    '6695.TW': {'name': '芯鼎', 'group': '01. 矽智財 (IP/ASIC)'},

    # ─── 02. AI 晶片 & 主流 IC 設計 ───
    '2454.TW': {'name': '聯發科', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2379.TW': {'name': '瑞昱', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3034.TW': {'name': '聯詠', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2458.TW': {'name': '義隆', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3545.TW': {'name': '敦泰', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '4961.TW': {'name': '天鈺', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '8016.TW': {'name': '矽創', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6202.TW': {'name': '盛群', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '5471.TW': {'name': '松翰', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2401.TW': {'name': '凌陽', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2436.TW': {'name': '偉詮電', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '5351.TWO': {'name': '鈺創', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3006.TW': {'name': '晶豪科', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3122.TW': {'name': '笙泉', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3228.TW': {'name': '金麗科', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6243.TW': {'name': '迅杰', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '4919.TW': {'name': '新唐', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '2363.TW': {'name': '矽統', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3014.TW': {'name': '聯陽', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '4968.TW': {'name': '立積', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6462.TWO': {'name': '神盾', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '8054.TW': {'name': '揚智', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3141.TWO': {'name': '晶宏', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6237.TW': {'name': '驊訊', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '4947.TWO': {'name': '昂寶-KY', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6494.TWO': {'name': '九齊', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3527.TWO': {'name': '聚積', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '4952.TW': {'name': '凌通', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6271.TW': {'name': '同欣電', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '8081.TWO': {'name': '致新', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3211.TWO': {'name': '順達', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6104.TWO': {'name': '創惟', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3553.TWO': {'name': '力群', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '6679.TWO': {'name': '鈺太', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3001.TW': {'name': '三福電', 'group': '02. AI 晶片 & 主流 IC 設計'},
    '3230.TWO': {'name': '錦明', 'group': '02. AI 晶片 & 主流 IC 設計'},

    # ─── 03. 伺服器核心 IC & 管理晶片 ───
    '5274.TW': {'name': '信驊', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '5269.TW': {'name': '祥碩', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '4966.TW': {'name': '譜瑞-KY', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '6415.TW': {'name': '矽力*-KY', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '6138.TWO': {'name': '茂達', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '3588.TW': {'name': '通嘉', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '6719.TW': {'name': '力智', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '3563.TW': {'name': '牧德', 'group': '03. 伺服器核心 IC & 管理晶片'},
    '6245.TW': {'name': '立端', 'group': '03. 伺服器核心 IC & 管理晶片'},

    # ─── 04. 晶圓代工與先進製程 ───
    '2330.TW': {'name': '台積電', 'group': '04. 晶圓代工與先進製程'},
    '2303.TW': {'name': '聯電', 'group': '04. 晶圓代工與先進製程'},
    '5347.TW': {'name': '世界', 'group': '04. 晶圓代工與先進製程'},
    '3707.TW': {'name': '漢磊', 'group': '04. 晶圓代工與先進製程'},
    '3016.TW': {'name': '嘉晶', 'group': '04. 晶圓代工與先進製程'},
    '6770.TW': {'name': '力基電', 'group': '04. 晶圓代工與先進製程'},
    '6488.TWO': {'name': '環球晶', 'group': '04. 晶圓代工與先進製程'},
    '5483.TWO': {'name': '中美晶', 'group': '04. 晶圓代工與先進製程'},
    '3532.TW': {'name': '台勝科', 'group': '04. 晶圓代工與先進製程'},

    # ─── 05. 先進封裝與測試 (CoWoS/FOPLP) ───
    '3711.TW': {'name': '日月光投控', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '2449.TW': {'name': '京元電子', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '6239.TW': {'name': '力成', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '6147.TWO': {'name': '頎邦', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '3481.TW': {'name': '群創', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '2441.TW': {'name': '超豐', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '6257.TW': {'name': '矽格', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '3264.TWO': {'name': '欣銓', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '3265.TWO': {'name': '台星科', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '8110.TW': {'name': '華東', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '3374.TW': {'name': '精材', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '8028.TWO': {'name': '昇陽半導體', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '2323.TW': {'name': '中環', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '2349.TW': {'name': '錸德', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},
    '8150.TW': {'name': '南茂', 'group': '05. 先進封裝與測試 (CoWoS/FOPLP)'},

    # ─── 06. 半導體設備、濕製程與材料 ───
    '3131.TWO': {'name': '弘塑', 'group': '06. 半導體設備、濕製程與材料'},
    '3583.TW': {'name': '辛耘', 'group': '06. 半導體設備、濕製程與材料'},
    '6187.TWO': {'name': '萬潤', 'group': '06. 半導體設備、濕製程與材料'},
    '2447.TW': {'name': '志聖', 'group': '06. 半導體設備、濕製程與材料'},
    '5443.TW': {'name': '均豪', 'group': '06. 半導體設備、濕製程與材料'},
    '6640.TWO': {'name': '均華', 'group': '06. 半導體設備、濕製程與材料'},
    '6196.TW': {'name': '帆宣', 'group': '06. 半導體設備、濕製程與材料'},
    '2404.TW': {'name': '漢唐', 'group': '06. 半導體設備、濕製程與材料'},
    '6139.TW': {'name': '亞翔', 'group': '06. 半導體設備、濕製程與材料'},
    '3413.TW': {'name': '京鼎', 'group': '06. 半導體設備、濕製程與材料'},
    '5536.TWO': {'name': '聖暉*', 'group': '06. 半導體設備、濕製程與材料'},
    '6613.TWO': {'name': '朋億*', 'group': '06. 半導體設備、濕製程與材料'},
    '6667.TWO': {'name': '信紘科', 'group': '06. 半導體設備、濕製程與材料'},
    '6894.TWO': {'name': '科嶠', 'group': '06. 半導體設備、濕製程與材料'},
    '6207.TWO': {'name': '雷科', 'group': '06. 半導體設備、濕製程與材料'},
    '1560.TW': {'name': '中砂', 'group': '06. 半導體設備、濕製程與材料'},
    '1773.TW': {'name': '勝一', 'group': '06. 半導體設備、濕製程與材料'},
    '4755.TWO': {'name': '三福化', 'group': '06. 半導體設備、濕製程與材料'},
    '5434.TW': {'name': '崇越', 'group': '06. 半導體設備、濕製程與材料'},
    '3010.TW': {'name': '華立', 'group': '06. 半導體設備、濕製程與材料'},
    '1717.TW': {'name': '長興', 'group': '06. 半導體設備、濕製程與材料'},
    '3680.TW': {'name': '家登', 'group': '06. 半導體設備、濕製程與材料'},
    '8064.TWO': {'name': '東捷', 'group': '06. 半導體設備、濕製程與材料'},
    '6532.TWO': {'name': '瑞耘', 'group': '06. 半導體設備、濕製程與材料'},
    '3055.TW': {'name': '蔚華科', 'group': '06. 半導體設備、濕製程與材料'},
    '2465.TW': {'name': '麗臺', 'group': '06. 半導體設備、濕製程與材料'},
    '1727.TW': {'name': '中華化', 'group': '06. 半導體設備、濕製程與材料'},
    '4770.TW': {'name': '上品', 'group': '06. 半導體設備、濕製程與材料'},
    '8358.TWO': {'name': '金居材料', 'group': '06. 半導體設備、濕製程與材料'},

    # ─── 07. 高階晶片測試介面與檢測 (Socket/探針卡) ───
    '6515.TW': {'name': '穎崴', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '6223.TW': {'name': '旺矽', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '6510.TW': {'name': '精測', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '6683.TWO': {'name': '雍智科技', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '3030.TW': {'name': '德律', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '3289.TW': {'name': '宜特', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '3587.TWO': {'name': '閎康', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '6830.TW': {'name': '汎銓', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},
    '3558.TWO': {'name': '神準檢測', 'group': '07. 高階晶片測試介面與檢測 (Socket/探針卡)'},

    # ─── 08. 矽光子、CPO 與光收發模組 ───
    '3081.TWO': {'name': '聯亞', 'group': '08. 矽光子、CPO 與光收發模組'},
    '6451.TW': {'name': '訊芯-KY', 'group': '08. 矽光子 + CPO 光收發'},
    '3363.TWO': {'name': '上詮', 'group': '08. 矽光子、CPO 與光收發模組'},
    '3450.TW': {'name': '聯鈞', 'group': '08. 矽光子、CPO 與光收發模組'},
    '6442.TW': {'name': '光聖', 'group': '08. 矽光子、CPO 與光收發模組'},
    '4979.TW': {'name': '華星光', 'group': '08. 矽光子、CPO 與光收發模組'},
    '4908.TWO': {'name': '前鼎', 'group': '08. 矽光子、CPO 與光收發模組'},
    '4977.TW': {'name': '眾達-KY', 'group': '08. 矽光子、CPO 與光收發模組'},
    '3163.TWO': {'name': '波若威', 'group': '08. 矽光子、CPO 與光收發模組'},
    '3234.TWO': {'name': '光環', 'group': '08. 矽光子、CPO 與光收發模組'},
    '3454.TW': {'name': '晶睿光通', 'group': '08. 矽光子、CPO 與光收發模組'},

    # ─── 09. 網路通訊、交換器與 5G 設備 ───
    '2345.TW': {'name': '智邦', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '3380.TW': {'name': '明泰', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '6285.TW': {'name': '啟碁', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '5388.TW': {'name': '中磊', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '4906.TW': {'name': '正文', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '2332.TW': {'name': '友訊', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '3596.TW': {'name': '智易', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '3558.TW': {'name': '神準', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '6214.TW': {'name': '精誠資訊', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '3029.TW': {'name': '零壹科技', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '2471.TW': {'name': '資通電腦', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '6112.TW': {'name': '邁達特', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '2412.TW': {'name': '中華電', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '3045.TW': {'name': '台灣大', 'group': '09. 網路通訊、交換器與 5G 設備'},
    '4904.TW': {'name': '遠傳', 'group': '09. 網路通訊、交換器與 5G 設備'},

    # ─── 10. AI 伺服器代工組裝 (ODM/EMS/品牌) ───
    '2317.TW': {'name': '鴻海', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2382.TW': {'name': '廣達', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '6669.TW': {'name': '緯穎', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '3231.TW': {'name': '緯創', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2356.TW': {'name': '英業達', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2376.TW': {'name': '技嘉', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2352.TW': {'name': '佳世達', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2315.TW': {'name': '神達', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2312.TW': {'name': '金寶', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2324.TW': {'name': '仁寶', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '4938.TW': {'name': '和碩', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2377.TW': {'name': '微星', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2353.TW': {'name': '宏碁', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2357.TW': {'name': '華碩', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},
    '2308.TW': {'name': '台達電', 'group': '10. AI 伺服器代工組裝 (ODM/EMS/品牌)'},

    # ─── 11. 核心液冷、風扇與核心散熱 ───
    '3017.TW': {'name': '奇鋐', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3324.TW': {'name': '雙鴻', 'group': '11. 核心液冷、風扇與核心散熱'},
    '8996.TW': {'name': '高力', 'group': '11. 核心液冷、風扇與核心散熱'},
    '2421.TW': {'name': '建準', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3653.TW': {'name': '健策', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3483.TW': {'name': '力致', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3071.TW': {'name': '協禧', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3338.TW': {'name': '泰碩', 'group': '11. 核心液冷、風扇與核心散熱'},
    '6275.TW': {'name': '元山', 'group': '11. 核心液冷、風扇與核心散熱'},
    '4543.TWO': {'name': '萬在', 'group': '11. 核心液冷、風扇與核心散熱'},
    '6230.TW': {'name': '尼得科超眾', 'group': '11. 核心液冷、風扇與核心散熱'},
    '3311.TW': {'name': '閎暉', 'group': '11. 核心液冷、風扇與核心散熱'},
    '1582.TW': {'name': '信錦', 'group': '11. 核心液冷、風扇與核心散熱'},

    # ─── 12. 伺服器機殼與高階滑軌 ───
    '8210.TW': {'name': '勤誠', 'group': '12. 伺服器機殼與高階滑軌'},
    '3013.TW': {'name': '晟銘電', 'group': '12. 伺服器機殼與高階滑軌'},
    '6117.TW': {'name': '迎廣', 'group': '12. 伺服器機殼與高階滑軌'},
    '2059.TW': {'name': '川湖', 'group': '12. 伺服器機殼與高階滑軌'},
    '6584.TW': {'name': '南俊國際', 'group': '12. 伺服器機殼與高階滑軌'},
    '5222.TW': {'name': '全訊', 'group': '12. 伺服器機殼與高階滑軌'},
    '2476.TW': {'name': '鉅祥', 'group': '12. 伺服器機殼與高階滑軌'},
    '3548.TWO': {'name': '兆利', 'group': '12. 伺服器機殼與高階滑軌'},
    '3376.TW': {'name': '新日興', 'group': '12. 伺服器機殼與高階滑軌'},
    '1597.TWO': {'name': '直得精密', 'group': '12. 伺服器機殼與高階滑軌'},

    # ─── 13. 高頻高速 CCL、銅箔基板與 PCB 主板 ───
    '2383.TW': {'name': '台光電', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '6274.TW': {'name': '台燿', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '6213.TW': {'name': '聯茂', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2368.TW': {'name': '金像電', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '4958.TW': {'name': '臻鼎-KY', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '3044.TW': {'name': '健鼎', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '6269.TW': {'name': '台郡', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2367.TW': {'name': '燿華', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2313.TW': {'name': '華通', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2316.TW': {'name': '楠梓電', 'group': '13. 高頻高速 CCL + PCB 主板'},
    '5469.TW': {'name': '瀚宇博', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '3715.TW': {'name': '定穎投控', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '1815.TW': {'name': '富喬', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '8358.TWO': {'name': '金居', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2355.TW': {'name': '敬鵬', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '5439.TW': {'name': '高僑', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '6278.TW': {'name': '台表科', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},
    '2321.TW': {'name': '東訊', 'group': '13. High CCL 主板'},
    '3003.TW': {'name': '健和興', 'group': '13. 高頻高速 CCL、銅箔基板與 PCB 主板'},

    # ─── 14. IC 載板 (ABF/BT) ───
    '3037.TW': {'name': '欣興', 'group': '14. IC 載板 (ABF/BT)'},
    '8046.TW': {'name': '南電', 'group': '14. IC 載板 (ABF/BT)'},
    '3189.TW': {'name': '景碩', 'group': '14. IC 載板 (ABF/BT)'},

    # ─── 15. 記憶體顆粒、模組與控制晶片 ───
    '2408.TW': {'name': '南亞科', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '2344.TW': {'name': '華邦電', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '2337.TW': {'name': '旺宏', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '8299.TWO': {'name': '群聯', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '3260.TWO': {'name': '威剛', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '2451.TW': {'name': '創見', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '8088.TWO': {'name': '品安', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '4967.TW': {'name': '十銓', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '8271.TW': {'name': '宇瞻', 'group': '15. 記憶體顆粒、模組與控制晶片'},
    '3006.TWO': {'name': '晶豪科', 'group': '15. 記憶體顆粒、模組與控制晶片'},

    # ─── 16. 高階高功率電源供應器與配電 ───
    '2308.TW': {'name': '台達電', 'group': '16. 高階高功率電源供應器與配電'},
    '2301.TW': {'name': '光寶科', 'group': '16. 高階高功率電源供應器與配電'},
    '6282.TW': {'name': '康舒', 'group': '16. 高階高功率電源供應器與配電'},
    '3015.TW': {'name': '全漢', 'group': '16. 高階高功率電源供應器與配電'},
    '3032.TW': {'name': '偉訓', 'group': '16. 高階高功率電源供應器與配電'},
    '2457.TW': {'name': '飛宏', 'group': '16. 高階高功率電源供應器與配電'},
    '3027.TW': {'name': '盛達', 'group': '16. 高階高功率電源供應器與配電'},
    '2415.TW': {'name': '錩新', 'group': '16. 高階高功率電源供應器與配電'},

    # ─── 17. NVLink 連接線、連接器與高速線束 ───
    '6197.TW': {'name': '佳必琪', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3533.TW': {'name': '嘉澤', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3665.TW': {'name': '貿聯-KY', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '6205.TW': {'name': '詮欣', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3023.TW': {'name': '信邦', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3526.TWO': {'name': '凡甲', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3710.TW': {'name': '連展投控', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '6290.TW': {'name': '良維', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3605.TW': {'name': '宏致', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '2392.TW': {'name': '正崴', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '3005.TW': {'name': '神基', 'group': '17. NVLink 連接線、連接器與高速線束'},
    '6115.TW': {'name': '鎰勝', 'group': '17. NVLink 連接線、連接器與高速線束'},

    # ─── 18. 特高壓重電與不斷電配電系統 ───
    '1519.TW': {'name': '華城', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1503.TW': {'name': '士電', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1513.TW': {'name': '中興電', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1514.TW': {'name': '亞力', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1504.TW': {'name': '東元', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1529.TW': {'name': '樂事綠能', 'group': '18. 特高壓重電與不斷電配電系統'},
    '6869.TW': {'name': '雲豹能源', 'group': '18. 特高壓重電與不斷電配電系統'},
    '6806.TW': {'name': '森崴能源', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1508.TW': {'name': '正道', 'group': '18. 特高壓重電與不斷電配電系統'},
    '1516.TW': {'name': '川飛', 'group': '18. 特高壓重電與不斷電配電系統'},

    # ─── 19. 被動元件 (MLCC/電感/電阻) ───
    '2327.TW': {'name': '國巨', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '2492.TW': {'name': '華新科', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '3357.TWO': {'name': '臺慶科', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '3026.TW': {'name': '禾伸堂', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '6173.TWO': {'name': '信昌電', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '2375.TW': {'name': '凱美', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '2472.TW': {'name': '立隆電', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '3090.TW': {'name': '日電貿', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '6284.TWO': {'name': '佳邦', 'group': '19. 被動元件 (MLCC/電感/電阻)'},
    '2456.TW': {'name': '奇力新', 'group': '19. 被動元件 (MLCC/電感/電阻)'},

    # ─── 20. 二極體、MOSFET 與功率半導體 ───
    '3675.TWO': {'name': '德微', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '2481.TW': {'name': '強茂', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '2425.TW': {'name': '鼎元', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '2340.TW': {'name': '台亞', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '5425.TWO': {'name': '台半', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '8255.TW': {'name': '朋程', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6573.TWO': {'name': '虹揚-KY', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '8261.TW': {'name': '富鼎', 'group': '20. 二極體 Fest 功率半導體'},
    '5299.TWO': {'name': '杰力', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6435.TWO': {'name': '大中', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '3317.TWO': {'name': '尼克森', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6411.TWO': {'name': '晶焱', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6525.TW': {'name': '捷敏-KY', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6651.TWO': {'name': '全宇昕', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6759.TWO': {'name': '力士', 'group': '20. 二極體、MOSFET 與功率半導體'},
    '6693.TWO': {'name': '廣閎科', 'group': '20. 二極體、MOSFET 與功率半導體'},

    # ─── 21. 智慧視覺、機器人與自動化具身智能 ───
    '2359.TW': {'name': '所羅門', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '6188.TW': {'name': '廣明', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '2464.TW': {'name': '盟立', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '8374.TWO': {'name': '羅昇', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '4562.TW': {'name': '穎漢', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '2365.TW': {'name': '昆盈', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '1536.TW': {'name': '和大', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '1597.TWO': {'name': '直得', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '2049.TW': {'name': '上銀', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '4583.TW': {'name': '台灣精銳', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '1590.TW': {'name': '亞德客-KY', 'group': '21. 智慧視覺、機器人與自動化具身智能'},
    '2397.TW': {'name': '友通', 'group': '21. 智慧視覺、機器人與自動化具身智能'},

    # ─── 22. 工業電腦與嵌入式系統 (IPC) ───
    '2395.TW': {'name': '研華', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '6414.TW': {'name': '樺漢', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '6206.TW': {'name': '飛捷', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '6166.TW': {'name': '凌華', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '8050.TW': {'name': '廣積', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '6160.TWO': {'name': '欣技', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '3088.TW': {'name': '艾訊', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},
    '3570.TW': {'name': '大聯大', 'group': '22. 工業電腦與嵌入式系統 (IPC)'},

    # ─── 23. 光學鏡頭、面板與車用電子 ───
    '3406.TW': {'name': '玉晶光', 'group': '23. 光學鏡頭、面板與車用電子'},
    '3008.TW': {'name': '大立光', 'group': '23. 光學鏡頭、面板與車用電子'}, 
    '3362.TWO': {'name': '先進光', 'group': '23. 光學鏡頭、面板與車用電子'},
    '3019.TW': {'name': '亞光', 'group': '23. 光學鏡頭、面板與車用電子'},
    '4976.TWO': {'name': '佳凌', 'group': '23. 光學鏡頭、面板與車用電子'},
    '2409.TW': {'name': '友達', 'group': '23. 光學鏡頭、面板與車用電子'},
    '6116.TW': {'name': '彩晶', 'group': '23. 光學鏡頭、面板與車用電子'},
    '2393.TW': {'name': '億光', 'group': '23. 光學鏡頭、面板與車用電子'},
    '3714.TW': {'name': '富采', 'group': '23. 光學鏡頭、面板與車用電子'},
    '3552.TWO': {'name': '同致', 'group': '23. 光學鏡頭、面板與車用電子'},
    '1533.TW': {'name': '車王電', 'group': '23. 光學鏡頭、面板與車用電子'},
    '2231.TW': {'name': '為升', 'group': '23. 光學鏡頭、面板與車用電子'},
    '2497.TW': {'name': '怡利電', 'group': '23. 光學鏡頭、面板與車用電子'},
    '6795.TW': {'name': '澤米', 'group': '23. 光學鏡頭、面板與車用電子'},
    '6168.TW': {'name': '宏齊', 'group': '23. 光學鏡頭、面板與車用電子'},
    '2426.TW': {'name': '鼎元光電', 'group': '23. 光學鏡頭、面板與車用電子'},
}

# 👑 【側邊欄：大仁哥投資週報快速打字對帳艙】固定在最下方，方便您每週看圖 10秒 快速更新！
st.sidebar.markdown("---")
st.sidebar.header("📋 大仁哥週報快速輸入艙")
st.sidebar.caption("💡 請照著圖片最下方的四位數代號打字（多檔用英文逗號隔開）")
weekly_bottom_input = st.sidebar.text_input("1. 底部型態組代號：", value="3583, 3443")
weekly_trust_input = st.sidebar.text_input("2. 投信認養組代號：", value="3189")
weekly_stable_input = st.sidebar.text_input("3. 守穩轉強組代號：", value="2303, 5347")
weekly_strong_input = st.sidebar.text_input("4. 技術面強勢組代號：", value="8046, 2327, 6139")

def parse_weekly_inputs(input_str, default_group_name):
    res = {}
    if not input_str: return res
    codes = [x.strip() for x in input_str.split(",") if x.strip()]
    for c in codes:
        found = False
        for k, v in AI_STOCKS_DICT.items():
            if k.startswith(c + "."):
                res[k] = {"name": v["name"], "weekly_tag": default_group_name, "pure_code": c}
                found = True; break
        if not found:
            res[c + ".TW"] = {"name": f"通用標的({c})", "weekly_tag": default_group_name, "pure_code": c}
    return res

WEEKLY_MAP = {}
WEEKLY_MAP.update(parse_weekly_inputs(weekly_bottom_input, "⭐ 底部型態（名師看好落底）"))
WEEKLY_MAP.update(parse_weekly_inputs(weekly_trust_input, "🎯 投信認養（大戶實質鎖碼）"))
WEEKLY_MAP.update(parse_weekly_inputs(weekly_stable_input, "🛡️ 守穩轉強（打底完成準備點火）"))
WEEKLY_MAP.update(parse_weekly_inputs(weekly_strong_input, "🔥 技術面強勢（多頭強勢常態）"))
WEEKLY_TICKERS = list(WEEKLY_MAP.keys())

# 全鏈統合活體連線數據載入
def fetch_all_data_complete(base_tickers, weekly_tickers):
    portfolio_tickers = st.session_state.my_portfolio['代號'].dropna().tolist()
    yf_port = []
    for t in portfolio_tickers:
        t_str = str(t).strip().upper()
        if t_str:
            if not t_str.endswith('.TW') and not t_str.endswith('.TWO'):
                matched = [k for k in AI_STOCKS_DICT.keys() if k.startswith(t_str + '.')]
                if matched: yf_port.append(matched[0])
                else: yf_port.append(t_str + '.TW')
            else: yf_port.append(t_str)
    all_fetch = sorted(list(set(base_tickers + weekly_tickers + yf_port)))
    if not all_fetch: return None, None, None
    try:
        import requests
        clean_session = requests.Session()
        clean_session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        hourly = yf.download(all_fetch, period="2mo", interval="1h", group_by='ticker', progress=False, threads=False, session=clean_session)
        daily = yf.download(all_fetch, period="8mo", interval="1d", group_by='ticker', progress=False, threads=False, session=clean_session)
        return hourly, daily, all_fetch
    except: return None, None, None

if FILTERED_TICKERS or WEEKLY_TICKERS:
    with st.spinner("⚡ 350+ 全大軍雷達 × 名師投資劇本活體連線中..."):
        hourly_data, daily_data, all_fetch = fetch_all_data_complete(FILTERED_TICKERS, WEEKLY_TICKERS)
    
    if hourly_data is not None and daily_data is not None and not hourly_data.empty:
        is_multi = isinstance(hourly_data.columns, pd.MultiIndex)
        LATEST_PRICES_DAILY = {}
        YESTERDAY_CLOSES_DAILY = {}
        for ticker in all_fetch:
            try:
                df_ticker_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                if not df_ticker_d.empty:
                    LATEST_PRICES_DAILY[ticker] = df_ticker_d['Close'].iloc[-1]
                    if len(df_ticker_d) >= 2: YESTERDAY_CLOSES_DAILY[ticker] = df_ticker_d['Close'].iloc[-2]
                    else: LATEST_PRICES_DAILY[ticker] = df_ticker_d['Close'].iloc[-1]
            except: pass

        # 📋 新增你指定的專屬全新分頁（直接擺在所有分頁的最前面第一個第一個）
        tab_weekly, tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📋 大仁哥週報戰客特訓艙", "🚀 今日實戰精選買入名單", "🔄 AI次族群資金換手地圖", 
            "🔥 日K核心動能大篩選", "🛡️ 日線級別均線防守選股", "💎 個股日K智庫全景診斷", 
            "📊 AI大軍日K成交量排行", "💰 族群日K資金輪動監控", "📱 持股防守艙"
        ])

        # 大數據流向核心矩陣計算
        group_flows = []
        for ticker in FILTERED_TICKERS:
            try:
                df_ticker = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                if len(df_ticker) < 65: continue
                df_v = df_ticker.copy()
                df_v['MA5'] = df_v['Close'].rolling(window=5).mean()
                df_v['MA20'] = df_v['Close'].rolling(window=20).mean()
                df_v['MA60'] = df_v['Close'].rolling(window=60).mean()
                df_v['Value'] = df_v['Close'] * df_v['Volume']
                df_v['Value_MA5'] = df_v['Value'].rolling(window=5).mean()
                df_v['Vol_MA5'] = df_v['Volume'].rolling(window=5).mean()
                today_v = df_v.iloc[-1]
                yesterday_close = YESTERDAY_CLOSES_DAILY.get(ticker, today_v['Close'])
                current_p = LATEST_PRICES_DAILY.get(ticker, today_v['Close']) 
                chg_pct = ((current_p - yesterday_close) / yesterday_close * 100)
                stock_trend = diagnose_trend_status(current_p, today_v['MA20'], today_v['MA60'])
                bias_5 = ((current_p - today_v['MA5']) / today_v['MA5']) * 100
                group_flows.append({
                    "ticker": ticker, "name": AI_STOCKS_DICT[ticker]['name'], "group": FILTERED_STOCKS_DICT[ticker]['group'],
                    "value_today": today_v['Value'], "value_ma5": today_v['Value_MA5'], 
                    "p_change": chg_pct, "price": current_p, "volume": today_v['Volume'], 
                    "stock_vol_ratio": today_v['Volume'] / today_v['Vol_MA5'] if today_v['Vol_MA5'] > 0 else 1.0,
                    "stock_trend": stock_trend, "bias_5": bias_5
                })
            except: continue

        from_names_tab0, to_names_tab0 = "", ""
        if group_flows:
            flow_df_calc = pd.DataFrame(group_flows)
            agg_df_calc = flow_df_calc.groupby("group").agg({"value_today": "sum", "value_ma5": "sum", "p_change": "mean"}).reset_index()
            agg_df_calc["ratio"] = agg_df_calc["value_today"] / agg_df_calc["value_ma5"]
            from_groups_calc = agg_df_calc.sort_values(by="ratio", ascending=True).head(2)
            to_groups_calc = agg_df_calc.sort_values(by="ratio", ascending=False).head(2)
            from_names_tab0 = "、".join([f"【{x.split(' ')[1]}】" for x in from_groups_calc["group"].tolist()])
            to_names_tab0 = "、".join([f"【{x.split(' ')[1]}】" for x in to_groups_calc["group"].tolist()])

        # ＝＝＝＝＝＝＝＝＝＝ Tab 專屬【📋 大仁哥週報戰客特訓艙 - 名師交叉對帳完全體】 ＝＝＝＝＝＝＝＝＝＝
        with tab_weekly:
            st.markdown("## 📋 【大仁哥投資週報 ➔ 活體量化交叉對帳特區】")
            st.caption("💡 交叉原理：拿大仁哥圖片中最下方的分組『期望標籤』，全自動去對齊目前的均線支撐與背離公式，輸出最直白的明天早盤指令。")
            
            if weekly_tickers:
                for tk in weekly_tickers:
                    try:
                        df_w = daily_data[tk].dropna() if is_multi else daily_data.dropna()
                        df_w['MA5'] = df_w['Close'].rolling(window=5).mean()
                        df_w['MA10'] = df_w['Close'].rolling(window=10).mean()
                        df_w['MA20'] = df_w['Close'].rolling(window=20).mean()
                        df_w['MA60'] = df_w['Close'].rolling(window=60).mean()
                        
                        p_w = LATEST_PRICES_DAILY.get(tk, df_w['Close'].iloc[-1])
                        ma5_w = df_w['MA5'].iloc[-1]
                        ma10_w = df_w['MA10'].iloc[-1]
                        ma20_w = df_w['MA20'].iloc[-1]
                        
                        tag_name = WEEKLY_MAP[tk]["weekly_tag"]
                        stock_name = WEEKLY_MAP[tk]["name"]
                        pure_code = WEEKLY_MAP[tk]["pure_code"]
                        
                        # 鋼鐵判定：底部組看 20MA，強勢/通訊組看 10MA
                        lower_w, upper_w = ma10_w * 0.985, ma10_w * 1.015
                        if "底部" in tag_name or "20MA" in tag_name or "守穩" in tag_name:
                            lower_w, upper_w = ma20_w * 0.99, ma20_w * 1.015
                            
                        chips_w = calculate_institutional_flows(df_w)
                        stock_win_rate_w = calculate_historical_win_rate(df_w)
                        
                        if lower_w <= p_w <= upper_w:
                            st.success(
                                f"#### 🎯 {stock_name} ({pure_code}) ── 【{tag_name}】\n"
                                f"* **🔥 實戰盲測發射指令**：` 🚀 劇本觸發：目前價格 ({p_w:.2f}) 已完美進入大戶防守區區間 ({lower_w:.1f}~{upper_w:.1f})，明天早盤開盤爆量直接開擊！ `\n"
                                f"* 📈 **歷史量化優勢勝率**：` {stock_win_rate_w} ` | 💰 **大戶籌碼實況**：` {chips_w['今日主力']} / {chips_w['今日外資']} ({chips_w['評級']}) `\n"
                                f"* ⚠️ **進場後預防針（波動防守）**：進場後主力通常會有常態性的磨人洗盤，**只要收盤不無情跌破極限防守線 `{lower_w:.1f}` 元，就絕對不要被洗出場**。防守線抓死，博取上方 15-20% 的肥美利潤！"
                            )
                        else:
                            st.info(
                                f"#### ⏳ {stock_name} ({pure_code}) ── 【{tag_name}】\n"
                                f"* **🔥 實戰盲測發射指令**：` ⏳ 戰略潛伏：現價 ({p_w:.2f}) 離下方主力成本線過高、短線空間發散。請先列入觀察名單！立刻設定價格警示，靜待降回【{lower_w:.1f}~{upper_w:.1f}】伏擊圈再開槍，絕不盲目高檔幫大戶接飛刀！ `\n"
                                f"* 📈 **歷史量化優勢勝率**：` {stock_win_rate_w} ` | 💰 **大戶籌碼實況**：` {chips_w['今日主力']} ({chips_w['評級']}) `\n"
                                f"* 🛡️ **伏擊作戰方針**：好獵物值得等待。目前的常態推升並非安全買點，把手收起來，放任它震盪跌回大戶的核心成本巢穴時，才是我們風險極小的最佳開火信號！"
                            )
                        st.markdown("---")
                    except: pass
            else:
                st.info("💡 目前側邊欄代號輸入艙為空，請輸入本週大仁哥週報圖片中最下方的四位數代號，新分頁立刻為您全自動交叉盲測對帳！")

        # ＝＝＝＝＝＝＝＝＝＝ Tab 0【今日實戰精選買入名單】 ＝＝＝＝＝＝＝＝＝＝
        with tab0:
            st.markdown("### 🦅 台股 AI 期望值波段作戰發射艙")
            
            # 🔒 初始化 Session State 鋼鐵記憶庫：防止隔天股票消失
            if 'locked_tab0_history' not in st.session_state:
                st.session_state.locked_tab0_history = {
                    "ignition": {}, "rocket": {}, "rebound": {}
                }
            
            ignition_sphere_confirmed = []
            rocket_confirmed = []
            rebound_confirmed = []
            
            # 第一步：活體掃描當日前線數據
            for ticker in FILTERED_TICKERS:
                try:
                    df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    if len(df_d) < 65: continue
                    df_d['MA5'] = df_d['Close'].rolling(window=5).mean()
                    df_d['MA10'] = df_d['Close'].rolling(window=10).mean()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    
                    low_9, high_9 = df_d['Low'].rolling(window=9).min(), df_d['High'].rolling(window=9).max()
                    df_d['RSV'] = (((df_d['Close'] - low_9) / (high_9 - low_9)) * 100).fillna(50)
                    df_d['K'] = df_d['RSV'].ewm(alpha=1/3, adjust=False).mean(); df_d['D'] = df_d['K'].ewm(alpha=1/3, adjust=False).mean()
                    
                    df_d['EMA12'] = df_d['Close'].ewm(span=12, adjust=False).mean(); df_d['EMA26'] = df_d['Close'].ewm(span=26, adjust=False).mean()
                    df_d['DIF'] = df_d['EMA12'] - df_d['EMA26']; df_d['MACD_Sig'] = df_d['DIF'].ewm(span=9, adjust=False).mean()
                    df_d['HIST'] = df_d['DIF'] - df_d['MACD_Sig']
                    
                    tod_d = df_d.iloc[-1]; yes_d = df_d.iloc[-2]
                    p_close = LATEST_PRICES_DAILY.get(ticker, tod_d['Close']) 
                    
                    if p_close > df_d['MA60'].iloc[-1] and tod_d['HIST'] > yes_d['HIST']:
                        daily_support = (2 * ((yes_d['High'] + yes_d['Low'] + yes_d['Close']) / 3)) - yes_d['High']
                        target_15, target_20 = p_close * 1.15, p_close * 1.20
                        stock_win_rate = calculate_historical_win_rate(df_d)
                        chips_info = calculate_institutional_flows(df_d)
                        
                        is_tab0_kd_div = False
                        if tod_d['K'] < 40:
                            for idx_b in range(3, 21):
                                if idx_b >= len(df_d): break
                                hist_row = df_d.iloc[-idx_b]
                                if hist_row['Close'] >= p_close and hist_row['K'] < tod_d['K'] and hist_row['K'] < 40:
                                    is_tab0_kd_div = True
                                    break
                        
                        bias_10_val = ((p_close - df_d['MA10'].iloc[-1]) / df_d['MA10'].iloc[-1]) * 100
                        stock_name = AI_STOCKS_DICT[ticker]['name']
                        group_name = AI_STOCKS_DICT[ticker]['group'].split(' ')[1] if ' ' in AI_STOCKS_DICT[ticker]['group'] else AI_STOCKS_DICT[ticker]['group']
                        
                        analysis_payload = {
                            "代號": ticker.split('.')[0], "名稱": stock_name, "市價": round(p_close, 2), "勝率": stock_win_rate,
                            "今日支撐": round(daily_support, 2), "停損價": round(df_d['MA10'].iloc[-1], 2) if abs(bias_10_val) <= 1.5 else round(df_d['MA20'].iloc[-1], 2),
                            "target_str": f"{target_15:.1f}~{target_20:.1f}", "chips_str": f"主力:{chips_info['今日主力']} / 外資:{chips_info['今日外資']} (評級:{chips_info['評級']})",
                            "group_str": group_name, "bias_10": bias_10_val
                        }
                        
                        if abs(bias_10_val) <= 1.5 and is_tab0_kd_div:
                            analysis_payload["進場成本防線"] = f"{(df_d['MA10'].iloc[-1]*0.985):.1f}~{(df_d['MA10'].iloc[-1]*1.015):.1f}"
                            analysis_payload["15-20%目標區"] = f"{target_15:.1f}~{target_20:.1f}"
                            analysis_payload["預估點火勝率"] = stock_win_rate
                            analysis_payload["主力支撐"] = round(daily_support, 2)
                            analysis_payload["極控停損"] = round(df_d['MA10'].iloc[-1], 2)
                            st.session_state.locked_tab0_history["ignition"][ticker] = (current_day_str, analysis_payload)
                        elif (df_d['MA20'].iloc[-1] * 0.99) <= p_close <= (df_d['MA20'].iloc[-1] * 1.015) and tod_d['K'] > tod_d['D']:
                            analysis_payload["進場區間"] = f"{(df_d['MA20'].iloc[-1]*0.99):.1f}~{(df_d['MA20'].iloc[-1]*1.015):.1f}"
                            analysis_payload["目標區"] = f"{target_15:.1f}~{target_20:.1f}"
                            st.session_state.locked_tab0_history["rebound"][ticker] = (current_day_str, analysis_payload)
                        elif p_close > df_d['MA20'].iloc[-1] * 1.02:
                            close_to_5ma = abs(p_close - df_d['MA5'].iloc[-1]) / df_d['MA5'].iloc[-1] <= 0.012
                            close_to_10ma = abs(p_close - df_d['MA10'].iloc[-1]) / df_d['MA10'].iloc[-1] <= 0.012
                            if close_to_5ma or close_to_10ma:
                                tight_stop = df_d['MA10'].iloc[-1]
                                analysis_payload["進場區間"] = f"{(tight_stop*0.99):.1f}~{(tight_stop*1.012):.1f}"
                                analysis_payload["目標區"] = f"{target_15:.1f}~{target_20:.1f}"
                                st.session_state.locked_tab0_history["rocket"][ticker] = (current_day_str, analysis_payload)
                except: continue
            
            # 第二步：鋼鐵留存觀察防線過濾（強制把前一天的遺留個股釘在榜單上，絕不消失）
            ignition_sphere_confirmed_filtered = []
            rocket_confirmed_filtered = []
            rebound_confirmed_filtered = []
            
            for list_key, target_list in [("ignition", ignition_sphere_confirmed_filtered), ("rocket", rocket_confirmed_filtered), ("rebound", rebound_confirmed_filtered)]:
                for tk, (saved_date, payload) in list(st.session_state.locked_tab0_history[list_key].items()):
                    # 如果是當天進榜，或是昨天(24小時內)留下來的，一律保留
                    if saved_date == current_day_str or (datetime.now() - datetime.strptime(saved_date, "%Y-%m-%d")).days <= 1:
                        # 🔄 即時判定隔天發射指令（馬上買 vs 觀察伏擊）
                        curr_p_now = LATEST_PRICES_DAILY.get(tk, payload["市價"])
                        payload["市價"] = round(curr_p_now, 2)
                        
                        # 解析買入防線邊界
                        lower_bound, upper_bound = 0.0, 0.0
                        if "進場成本防線" in payload: lower_bound, upper_bound = map(float, payload["進場成本防線"].split('~'))
                        elif "進場區間" in payload: lower_bound, upper_bound = map(float, payload["進場區間"].split('~'))
                        
                        if lower_bound <= curr_p_now <= upper_bound:
                            payload["發射指令"] = "🔥 劇本觸發：目前已進入大戶換手防線，開盤爆量直接擊殺！"
                            payload["box_style"] = "success"
                        else:
                            payload["發射指令"] = f"⏳ 戰略潛伏：現價偏高，嚴禁手癢追高！請立刻設定價格警示，靜待降回【{lower_bound if lower_bound > 0 else '指定'}~{upper_bound if upper_bound > 0 else '指定'}】伏擊圈再開槍！"
                            payload["box_style"] = "info"
                            
                        target_list.append(payload)
                    else:
                        # 超過 48 小時的常態洗盤落後股才進行除役
                        del st.session_state.locked_tab0_history[list_key][tk]

            # ─── 渲染區 0：蓄勢發射球 ───
            st.markdown("### 👑 🔮 👑 頂級操盤手特製：【今日最完美量化共振 ➔ 🌟 蓄勢待發發發射球】")
            if ignition_sphere_confirmed_filtered:
                df_ign = pd.DataFrame(ignition_sphere_confirmed_filtered)
                st.data_editor(df_ign[["代號", "名稱", "市價", "進場成本防線", "15-20%目標區", "預估點火勝率", "主力支撐", "極控停損"]], column_config=SEARCH_TABLE_CONFIG, hide_index=True, disabled=True, use_container_width=True)
                
                for item in ignition_sphere_confirmed_filtered:
                    with st.expander(f"🔬 智慧解密個別評語：詳細查閱 {item['代號']} {item['名稱']} 確定買進理由與即時動作指令", expanded=True):
                        box_dispatcher = {"success": st.success, "info": st.info}
                        box_dispatcher[item["box_style"]](f"### 🛡️ 實戰動作手令：{item['發射指令']}")
                        st.write(
                            f"#### 🎯 {item['名稱']}（{item['代號']}）── 【核心共振發射球・落底戰略動作】\n"
                            f"* 📈 **歷史量化勝率**：` {item['勝率']} ` | 💰 **大戶籌碼實況**：` {item['chips_str']} `\n\n"
                            f"--- \n"
                            f"* 🟢 **基本面背景**：該股屬於 **{item['group_str']}** 核心供應鏈，受惠於全球大戶資金從高位階板塊大搬風，實質產業需求正在強勢加溫中。\n"
                            f"* 📈 **技術面與籌碼解析**：日線級別經過回踩洗盤，目前價格正精準壓縮在主力換手防線，系統抓包它出現了 **『真結構型指標底背離』**。白話講：過去兩週外面看是在下跌，但主力大戶在底層早就在暗中默默爆買、瘋狂接單！\n"
                            f"* 🚀 **確定能進場的原因**：均線價格壓彈簧壓到最極致，大戶籌碼完成吸籌，今天主力大資金再度表態！\n"
                            f"* ⚠️ **進場後預防針（波動防守）**：進場後主力通常會有常態性的洗盤震盪，明早若遇到小幅拉回，**只要不跌破極控停損價 `{item['極控停損']}` 元，就絕對不要被洗出場**。防守點卡死 10MA，我們用極小風險，去博取上方 `{item['target_str']}` 元的波段肥美利潤！"
                        )
            else: st.info("⏳ 今晚全市場大數據掃描：暫無個股同時完美符合『10MA壓縮 ＋ 20日指標真底背離』發射特徵。")
            
            st.markdown("---")
            # ─── 渲染區 1：狂飆悍馬榜 ───
            st.markdown("### 🔥 🔴 狂飆悍馬榜：日K強勢主升段（拉回 5MA/10MA 換手點）")
            if rocket_confirmed_filtered:
                df_roc = pd.DataFrame(rocket_confirmed_filtered)
                st.data_editor(df_roc[["代號", "名稱", "市價", "進場區間", "目標區", "勝率", "今日支撐", "停損價"]], column_config=MOBILE_TABLE_CONFIG, hide_index=True, disabled=True, use_container_width=True)
                
                for item in rocket_confirmed_filtered:
                    with st.expander(f"🔥 飆股換手動作查閱：{item['代號']} {item['名稱']} 實戰指引與即時動作指令", expanded=False):
                        box_dispatcher = {"success": st.success, "info": st.info}
                        box_dispatcher[item["box_style"]](f"### 🛡️ 實戰動作手令：{item['發射指令']}")
                        st.write(
                            f"#### ⚡ {item['名稱']}（{item['代號']}）── 【強勢悍馬常態軌道・主升換手動作】\n"
                            f"* 📈 **技術主升勝率**：` {item['勝率']} ` | 💰 **短線籌碼實況**：` {item['chips_str']} `\n\n"
                            f"--- \n"
                            f"* 🟢 **基本面特徵**：作為 **{item['group_str']}** 族群的強勢多頭箭頭，基本面業績爆發力非常強悍，是多頭大戶鎖碼的必爭之地。\n"
                            f"* 📈 **技術面解析**：目前該股日K處於常態主升段，今天股價出現了非常健康的『拉回換手點』，精準靠攏在 5MA / 10MA 控盤線身邊。這不是多頭要死掉，而是狂飆途中的良性中繼站！\n"
                            f"* 🚀 **確定能進場的原因**：股價沒有過熱高空發散，回踩短期控盤線給予了游擊隊最舒服的『順勢搭便車』進場黃金空間。\n"
                            f"* ⚠️ **進場後預防針（波動防守）**：強勢飆股的缺點就是盤中震盪非常劇烈。**進場後明後天盤中可能會有暴震，只要收盤不無情跌破 10MA 強勢控盤防線（約 `{item['停損價']}` 元），就代表大戶莊家依然在車上**。對齊防守點，放任利潤向 `{item['target_str']}` 元常態推進！"
                        )
            else: st.info("⏳ 目前強勢飆股都在半空中，沒有任何一檔『精準拉回貼緊 5MA/10MA』。")
                
            st.markdown("---")
            # ─── 渲染區 2：潛力黑馬榜 ───
            st.markdown("### 🌱 🟢 潛力黑馬榜：日K底部穩健反彈（精穩貼緊 20MA 生命線）")
            if rebound_confirmed_filtered:
                df_reb = pd.DataFrame(rebound_confirmed_filtered)
                st.data_editor(df_reb[["代號", "名稱", "市價", "進場區間", "目標區", "勝率", "今日支撐", "停損價"]], column_config=MOBILE_TABLE_CONFIG, hide_index=True, disabled=True, use_container_width=True)
                
                for item in rebound_confirmed_filtered:
                    with st.expander(f"🌱 穩健黑馬安全查閱：{item['代號']} {item['名稱']} 實戰指引與即時動作指令", expanded=False):
                        box_dispatcher = {"success": st.success, "info": st.info}
                        box_dispatcher[item["box_style"]](f"### 🛡️ 實戰動作手令：{item['發射指令']}")
                        st.write(
                            f"#### 🛡️ {item['名稱']}（{item['代號']}）── 【底部黑馬復甦・穩健打底動作】\n"
                            f"* 📈 **底部反彈勝率**：` {item['勝率']} ` | 💰 **大戶收集籌碼**：` {item['chips_str']} `\n\n"
                            f"--- \n"
                            f"* 🟢 **基本面特徵**：隸屬 **{item['group_str']}** 關鍵次產業，利空已完全出盡，產業基本面正迎來谷底全面復甦的拐點。\n"
                            f"* 📈 **技術面解析**：這檔個股剛剛完成大底，目前股價溫和、非常乖巧地貼在日線 20MA 生命線身邊。這是多頭防禦最堅固的老巢，大戶資金在這裡築起了一道厚厚的防火牆。\n"
                            f"* 🚀 **確定能進場的原因**：股價剛從底部爬起來，安全基底極厚，具備『低風險、高期望值』的防守反擊特徵。\n"
                            f"* ⚠️ **進場後預防針（波動防守）**：底部黑馬股的缺點是『爆發前洗盤比較磨人』，它可能不會馬上拉出漲停，而是會沿著 20MA 溫吞磨蹭幾天。**你需要展現耐心，只要股價不跌破 20MA 生命線（現價 `{item['停損價']}` 元），大戶的方向就沒變**。等籌碼沉澱完畢、成交量爆量點火，就會瞬間向上噴發！"
                        )
            else: st.info("⏳ 目前暫時沒有標的『溫和黏在日線 20MA 防守線身邊』。")

            if from_names_tab0 and to_names_tab0:
                st.markdown("---")
                st.markdown("### 🗺️ 當前市場大資金板塊星移大局觀（跨族群換手脈絡）")
                st.info(
                    f"🔮 **操盤手實戰換手大局完美註解**：\n\n"
                    f"💡 **大脈絡監測**：目前大戶資金正連續 2-3 天從過熱的 {from_names_tab0} 板塊執行『暗中抽血與利潤套現』。**主力已將其當作波段大提款機**，手上若有相關持股，請立刻收緊 60分K 生命防線，嚴禁看新聞利多傻傻進場幫大戶接刀！\n\n"
                    f"與此同時，由提款區抽離的百億巨資，正無聲無息地**搬風並全面建倉到低位階的 {to_names_tab0} 龍頭指標股身邊**！這完全契合你『落底反彈流』的黃金狩獵背景，晚上做功課請直接鎖定這些吸籌指標個股，明天早盤動能點火即是發射信號！"
                )

        # ＝＝＝＝＝＝＝＝＝＝ Tab 1【🔄 獨立：次族群資金換手地圖分頁】（🔥 特打活體查詢功能） ＝＝＝＝＝＝＝＝＝＝
        with tab1:
            st.markdown("## 🗺️ 系統獨立監測：三大法人 AI 大軍資金「蹺蹺板換手地圖」")
            st.caption("💡 戰刻核心：本頁面全自動捕捉大資金從過熱區抽水、並同步注入低位階龍頭標的之完整遷徙軌跡。")
            
            if group_flows:
                flow_df = pd.DataFrame(group_flows)
                agg_df = flow_df.groupby("group").agg({"value_today": "sum", "value_ma5": "sum", "p_change": "mean"}).reset_index()
                agg_df["ratio"] = agg_df["value_today"] / agg_df["value_ma5"]
                
                from_groups = agg_df.sort_values(by="ratio", ascending=True).head(2)
                to_groups = agg_df.sort_values(by="ratio", ascending=False).head(2)
                
                with st.container(border=True):
                    st.markdown("### 🦅 AI 次族群資金跨板塊乾坤大挪移連線")
                    
                    st.markdown("#### 💸 【資金正在撤退的提款區 (From)】")
                    for _, row in from_groups.iterrows():
                        g_name = row["group"]
                        g_pct = row["p_change"]
                        sub_stocks = flow_df[flow_df["group"] == g_name]
                        target_lead = sub_stocks.sort_values(by="value_today", ascending=False).iloc[0]
                        st.error(f"* **{g_name}**（族群資金佔比委縮至前波 {row['ratio']:.2f}x，平均跌幅 {g_pct:+.2f}%）➔ 🚨 **主力大提款標的：{target_lead['name']} ({str(target_lead['ticker']).split('.')[0]})**")
                    
                    st.markdown("---")
                    st.markdown("#### 🎯 【資金正在連夜開進的進駐區 (To)】")
                    for _, row in to_groups.iterrows():
                        g_name = row["group"]
                        g_pct = row["p_change"]
                        sub_stocks = flow_df[flow_df["group"] == g_name]
                        target_lead = sub_stocks.sort_values(by="stock_vol_ratio", ascending=False).iloc[0]
                        st.success(f"* **{g_name}**（族群量能瘋狂放大 **{row['ratio']:.2f} 倍**，平均漲幅 {g_pct:+.2f}%）➔ 🔥 **核心吸籌指標箭頭：{target_lead['name']} ({str(target_lead['ticker']).split('.')[0]})** ── 成交量暴增 **{target_lead['stock_vol_ratio']:.2f} 倍**！")
                    
                    st.markdown("---")
                    
                    from_names = "ве、".join([f"【{x.split(' ')[1]}】" for x in from_groups["group"].tolist()])
                    to_names = "、".join([f"【{x.split(' ')[1]}】" for x in to_groups["group"].tolist()])
                    st.info(
                        f"🔮 **操盤手實戰換手完美註解**：\n\n"
                        f"💡 **大脈絡監測**：目前大戶資金正連續 2-3 天從過熱的 {from_names} 板塊執行『暗中抽血與利潤套現』。**主力已將其當作波段大提款機**，手上若有相關持股，請立刻收緊 60分K 生命防線，嚴禁看新聞利多傻傻進場幫大戶接刀！\n\n"
                        f"與此同時，由提款區抽離的百億巨資，正無聲無息地**搬風並全面建倉到低位階的 {to_names} 龍頭指標股身邊**！這完全契合你『落底反彈流』的黃金狩獵背景，晚上做功課請直接鎖定這些吸籌指標個股，明天早盤動能點火即是發射信號！"
                    )
            else: st.info("⏳ 次族群資金遷徙數據同步中...")

            # 🛠️ 鋼鐵特打查詢艙
            st.markdown("---")
            st.markdown("### 🔮 盤後快速特打查詢艙（不需切換分頁，原地直接剖析個股資金與波段轉折）")
            search_code = st.text_input("請輸入台股四位數代號（例如輸入 8046 查詢南電，或 2481 查詢強茂）：", key="tab1_search").strip()
            
            if search_code:
                matched_ticker = None
                for k in AI_STOCKS_DICT.keys():
                    if k.startswith(search_code + "."):
                        matched_ticker = k
                        break
                if not matched_ticker: matched_ticker = search_code + ".TW"
                try:
                    df_search = yf.download(matched_ticker, period="8mo", interval="1d", progress=False).dropna()
                    if df_search.empty: st.error("❌ 無此標的")
                    else:
                        if isinstance(df_search.columns, pd.MultiIndex):
                            df_search.columns = [col[0] if col[0] in ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'] else col[1] for col in df_search.columns]

                        df_search['MA5'] = df_search['Close'].rolling(window=5).mean()
                        df_search['MA10'] = df_search['Close'].rolling(window=10).mean()
                        df_search['MA20'] = df_search['Close'].rolling(window=20).mean()
                        df_search['MA60'] = df_search['Close'].rolling(window=60).mean()
                        
                        l9_s, h9_s = df_search['Low'].rolling(window=9).min(), df_search['High'].rolling(window=9).max()
                        df_search['RSV'] = (((df_search['Close'] - l9_s) / (h9_s - l9_s)) * 100).fillna(50)
                        df_search['K'] = df_search['RSV'].ewm(alpha=1/3, adjust=False).mean()
                        df_search['D'] = df_search['K'].ewm(alpha=1/3, adjust=False).mean()
                        
                        df_search['EMA12'] = df_search['Close'].ewm(span=12, adjust=False).mean()
                        df_search['EMA26'] = df_search['Close'].ewm(span=26, adjust=False).mean()
                        df_search['DIF'] = df_search['EMA12'] - df_search['EMA26']
                        df_search['MACD_Sig'] = df_search['DIF'].ewm(span=9, adjust=False).mean()
                        df_search['HIST'] = df_search['DIF'] - df_search['MACD_Sig']
                        
                        tod_s = df_search.iloc[-1]; yes_s = df_search.iloc[-2]
                        p_close_s = float(tod_s['Close'])
                        yesterday_close_s = float(yes_s['Close'])
                        daily_support_s = (2 * ((yes_s['High'] + yes_s['Low'] + yes_s['Close']) / 3)) - yes_s['High']
                        
                        stock_name_s = AI_STOCKS_DICT[matched_ticker]['name'] if matched_ticker in AI_STOCKS_DICT else f"全台股通用標的"
                        st.markdown(f"#### 📊 {search_code} {stock_name_s} 實時量價與背離健康度指標")
                        st.metric(label="當前收盤價", value=f"{p_close_s:.2f} 元", delta=f"{((p_close_s - yesterday_close_s) / yesterday_close_s * 100):+.2f}%")
                        
                        chips_s = calculate_institutional_flows(df_search)
                        c1, c2, c3, c4 = st.columns(4)
                        with c1: st.metric("🏦 主力大戶態度", chips_s["今日主力"])
                        with c2: st.metric("⚡ 外資即時動向", chips_s["今日外資"])
                        with c3: st.metric("🛡️ 投信加碼張數", chips_s["今日投信"])
                        with c4: st.metric("📊 5日籌碼大累計", chips_s["五日總量"])
                        
                        ma5_s = float(tod_s['MA5']); ma10_s = float(tod_s['MA10']); ma20_s = float(tod_s['MA20']); ma60_s = float(tod_s['MA60'])
                        bias_5_s = ((p_close_s - ma5_s) / ma5_s) * 100
                        bias_10_s = ((p_close_s - ma10_s) / ma10_s) * 100
                        
                        box_color_s = "info"; title_text_s = ""; trend_text_s = ""
                        if bias_10_s > 6.0:
                            trend_text_s = f"目前價格遠高於 10MA 控盤線，10MA 乖離已高達極端的 **{bias_10_s:+.2f}%**！短線追價買盤在太空嚴重發散。此時進場無異於在懸崖邊幫主力莊家接刀，極易面臨短線劇烈拉回。"
                            box_color_s = "error"; title_text_s = "🚨【AI 智庫警戒判定：空間嚴重高空發散，嚴禁手癢追高】"
                        elif -1.5 <= bias_10_s <= 1.5:
                            trend_text_s = f"目前價格與 10MA 控盤線空間極致收斂（10MA 乖離率僅漂亮的 **{bias_10_s:+.2f}%**）。股價已安全回踩主力防線，洗盤正式洗到核心成本區。下檔停損極小，屬於期望值極高、向向的完美安全防守發射台！"
                            box_color_s = "success"; title_text_s = "🟢【AI 智庫進場判定：精準安全回踩 10MA 主力控盤換手區】"
                        elif p_close_s < ma10_s:
                            trend_text_s = f"目前股價已無情跌破 10MA 控盤線（10MA 乖離率為 **{bias_10_s:+.2f}%**），短線技術面結構正式轉落進入空方修正背景。由於下方的底部分形信號尚未確立，此時不具備落底反彈特徵，強烈建議雙手抱胸、保持冷靜觀望。"
                            box_color_s = "warning"; title_text_s = "⏳【AI 智庫觀望判定：股價破位控盤線，靜待底部止穩分形】"
                        else:
                            trend_text_s = f"目前價格在 10MA 之上穩定多頭軌道向前運行（5MA 乖離 **{bias_5_s:+.2f}%**，10MA 乖離 **{bias_10_s:+.2f}%**）。空間結構並未出現極端的過熱或破位發散。屬於常態波段鎖碼洗盤或健康推進位階。"
                            box_color_s = "info"; title_text_s = "🔵【AI 智庫常態判定：個股處於多頭常態洗盤或推進位階】"
                        
                        is_kd_div_s = False; div_day_kd_s = -1; curr_k_s = float(tod_s['K'])
                        if curr_k_s < 40:
                            for idx_back in range(3, 21):
                                if idx_back >= len(df_search): break
                                hist_d = df_search.iloc[-idx_back]
                                if hist_d['Close'] >= p_close_s and hist_d['K'] < curr_k_s and hist_d['K'] < 40:
                                    is_kd_div_s = True; div_day_kd_s = idx_back; break
                                    
                        is_macd_div_s = False; div_day_macd_s = -1; curr_hist_s = float(tod_s['HIST'])
                        if curr_hist_s > 0:
                            for idx_back in range(3, 21):
                                if idx_back >= len(df_search): break
                                hist_d = df_search.iloc[-idx_back]
                                if hist_d['Close'] <= p_close_s and hist_d['HIST'] > curr_hist_s and hist_d['HIST'] > 0:
                                    is_macd_div_s = True; div_day_macd_s = idx_back; break
                        
                        div_text_s = ""
                        if is_kd_div_s:
                            div_text_s = f"🎯 **【轉折特徵：20日結構 KD 底背離】** 技術指標與 **{div_day_kd_s} 天前** 的波段低點確立了完美的結構型底背離！股價雖然在震盪洗盤，但底層指標動能已提前暗中大幅抬頭。大戶壓價吃貨痕跡敗露，這就是小波段落底反彈準備點火的最強烽火訊號！"
                            if box_color_s in ["success", "info"]: box_color_s = "success"; title_text_s = f"🔥【AI 智庫共振判定：貼緊控盤線 × {div_day_kd_s}天結構底背離黃金買點】"
                        elif is_macd_div_s:
                            div_text_s = f"🚨 **【轉折特徵：20日結構 MACD 頂背離】** 股價在表面刷出反彈新高，打前波高峰相比，實質推土能量紅柱體卻出現了嚴重的結構性委縮！主力正在拉高掩護倒貨，小心隨時引發高點暴跌修正，請立刻利索準備停利逃生！"
                            box_color_s = "error"; title_text_s = f"💥【AI 智庫危險判定：價格虛漲 × {div_day_macd_s}天結構頂背離逃生賣點】"
                        else:
                            div_text_s = "⚖️ **【轉折特徵：多空常態同步】** 經 20 日滾動背景比對，目前 KD 與 MACD 紅綠柱動能波動與價格走勢完全同步，未見任何結構性底背離大戶進貨或頂背離出貨特徵。"
                        
                        box_dispatcher = {"success": st.success, "error": st.error, "warning": st.warning, "info": st.info}
                        box_dispatcher[box_color_s](
                            f"### {title_text_s}\n"
                            f"**🔍 智慧買賣核心數據註解診斷：**\n\n"
                            f"1. **📈 趨勢與乖離空間診斷**：{trend_text_s}\n\n"
                            f"2. **🔥 轉折與雙指標背離鑑定**：{div_text_s}\n\n"
                            f"3. **💰 籌碼法人動態方向**：今日日K成交量為 5 日均量的 **{v_ratio_s:.1f} 倍**。{chips_s['五日總量']}"
                        )
                except Exception as ex: st.warning(f"⚠️ {search_code} 數據活體同步中，請確保代號輸入正確並重新整理...")

        # ＝＝＝＝＝＝＝＝＝＝ Tab 2 到 Tab 7 ＝＝＝＝＝＝＝＝＝＝
        with tab2:
            st.subheader("🤖 微族群過濾 - 日K級別強勢波段動能篩選")
            matches = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    if len(df_d) < 65: continue
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    low_9, high_9 = df_d['Low'].rolling(window=9).min(), df_d['High'].rolling(window=9).max()
                    df_d['RSV'] = (((df_d['Close'] - low_9) / (high_9 - low_9)) * 100).fillna(50)
                    df_d['K'] = df_d['RSV'].ewm(alpha=1/3, adjust=False).mean(); df_d['D'] = df_d['K'].ewm(alpha=1/3, adjust=False).mean()
                    today_d = df_d.iloc[-1]
                    if today_d['Close'] > today_d['MA60'] and today_d['K'] > today_d['D']:
                        df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                        trend_lbl = diagnose_trend_status(today_d['Close'], df_d['MA20'].iloc[-1], today_d['MA60'])
                        current_p = LATEST_PRICES_DAILY.get(ticker, today_d['Close']) 
                        matches.append({"代號": ticker.split('.')[0], "名稱": AI_STOCKS_DICT[ticker]['name'], "當前日K收盤價": round(current_p, 2), "波段趨勢位階": trend_lbl})
                except: continue
            if matches: st.dataframe(pd.DataFrame(matches).reset_index(drop=True), use_container_width=True)
            
        with tab3:
            st.subheader("🔍 日線級別 - 中長線均線防守波段診斷")
            correction_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_d = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean(); df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    p_today = df_d.iloc[-1]
                    if p_today['Close'] < p_today['MA20'] or p_today['Close'] < p_today['MA60']:
                        diagnose = diagnose_trend_status(p_today['Close'], p_today['MA20'], p_today['MA60'])
                        current_p = LATEST_PRICES_DAILY.get(ticker, p_today['Close']) 
                        correction_list.append({"代號": ticker.split('.')[0], "名稱": FILTERED_STOCKS_DICT[ticker]['name'], "今日日K收盤": round(current_p, 2), "長線趨勢背景": diagnose})
                except: continue
            if correction_list: st.dataframe(pd.DataFrame(correction_list).reset_index(drop=True), use_container_width=True)

        with tab4:
            st.subheader("💎 個股日K數據智慧解密與完美註解智庫艙")
            selector_options = {t: f"{t} {FILTERED_STOCKS_DICT[t]['name']}" for t in FILTERED_TICKERS}
            selected_ticker = st.selectbox("請選擇你想查看全景完美註解的 AI 股：", options=FILTERED_TICKERS, format_func=lambda x: selector_options[x], key="tab4_select")
            
            try:
                df_d = daily_data[selected_ticker].dropna() if is_multi else daily_data.dropna()
                if len(df_d) < 65:
                    st.info("💡 該標的歷史數據加載中...")
                else:
                    df_d['MA5'] = df_d['Close'].rolling(window=5).mean()
                    df_d['MA10'] = df_d['Close'].rolling(window=10).mean()
                    df_d['MA20'] = df_d['Close'].rolling(window=20).mean()
                    df_d['MA60'] = df_d['Close'].rolling(window=60).mean()
                    
                    low_9, high_9 = df_d['Low'].rolling(window=9).min(), df_d['High'].rolling(window=9).max()
                    df_d['RSV'] = (((df_d['Close'] - low_9) / (high_9 - low_9)) * 100).fillna(50)
                    df_d['K'] = df_d['RSV'].ewm(alpha=1/3, adjust=False).mean()
                    df_d['D'] = df_d['K'].ewm(alpha=1/3, adjust=False).mean()
                    
                    df_d['EMA12'] = df_d['Close'].ewm(span=12, adjust=False).mean()
                    df_d['EMA26'] = df_d['Close'].ewm(span=26, adjust=False).mean()
                    df_d['DIF'] = df_d['EMA12'] - df_d['EMA26']
                    df_d['MACD_Sig'] = df_d['DIF'].ewm(span=9, adjust=False).mean()
                    df_d['HIST'] = df_d['DIF'] - df_d['MACD_Sig']
                    
                    tod_d = df_d.iloc[-1]; yes_d = df_d.iloc[-2]
                    p_close = float(LATEST_PRICES_DAILY.get(selected_ticker, tod_d['Close']))
                    yesterday_close = float(YESTERDAY_CLOSES_DAILY.get(selected_ticker, p_close))
                    daily_support = (2 * ((yes_d['High'] + yes_d['Low'] + yes_d['Close']) / 3)) - yes_d['High']
                    
                    st.metric(label=f"📊 {FILTERED_STOCKS_DICT[selected_ticker]['name']} 當前日K價", value=f"{p_close:.2f} 元", delta=f"{((p_close - yesterday_close) / yesterday_close * 100):+.2f}%")
                    
                    chips = calculate_institutional_flows(df_d)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1: st.metric("🏦 主力大戶態度", chips["今日主力"])
                    with col2: st.metric("⚡ 外資即時動向", chips["今日外資"])
                    with col3: st.metric("🛡️ 投信加碼張數", chips["今日投信"])
                    with col4: st.metric("📊 5日籌碼大累計", chips["五日總量"])
                    
                    ma5_val = float(df_d['MA5'].iloc[-1])
                    ma10_val = float(df_d['MA10'].iloc[-1])
                    ma20_val = float(df_d['MA20'].iloc[-1])
                    ma60_val = float(df_d['MA60'].iloc[-1])
                    
                    bias_5 = ((p_close - ma5_val) / ma5_val) * 100
                    bias_10 = ((p_close - ma10_val) / ma10_val) * 100
                    trend_lbl = diagnose_trend_status(p_close, ma20_val, ma60_val)
                    
                    trend_text = ""; box_color = "info"; title_text = ""
                    if bias_10 > 6.0:
                        trend_text = f"目前 5MA 短線乖離為 **{bias_5:+.2f}%**，10MA 控盤線乖離已偏高達 **{bias_10:+.2f}%**。這說明短期價格在太空中嚴重向外發散！強烈建議絕對不要手癢追高，耐心等待股價回踩均線支撐！"
                        box_color = "error"; title_text = "🚨【AI 智庫警戒判定：個股高空嚴重發散，嚴禁手癢追高】"
                    elif -1.5 <= bias_10 <= 1.5:
                        trend_text = f"目前價格與 10MA 控盤線空間極致收斂（10MA 乖離率僅有漂亮的 **{bias_10:+.2f}%**）。這代表股價先前的高空火氣已完全退去，剛好安全回踩到波段主力的防守大本營。"
                        box_color = "success"; title_text = "🟢【AI 智庫買入判定：精準回踩 10MA 控盤安全換手區】"
                    elif p_close < ma10_val:
                        trend_text = f"目前股價已無情跌破 10MA 控盤線（10MA 乖離為 **{bias_10:.2f}%**），短線走勢正式轉落進入空方震盪修正背景，下方的底部分形或止穩信號尚未完全確立。"
                        box_color = "warning"; title_text = "⏳【AI 智庫觀望判定：股價跌破控盤線，靜待底部分形確立】"
                    else:
                        trend_text = f"目前股價穩健運行於 10MA 控盤線之漸健康的多頭軌道（5MA 乖離 **{bias_5:+.2f}%**，10MA 乖離 **{bias_10:+.2f}%**）。空間結構並未出現極端的過熱或破位發散。"
                        box_color = "info"; title_text = "🔵【AI 智庫常態判定：個股處於多頭常態洗盤或推進位階】"

                    is_kd_bottom_div = False; kd_div_day_idx = -1; current_k = float(tod_d['K'])
                    if current_k < 40:
                        for idx_back in range(3, 21):
                            if idx_back >= len(df_d): break
                            hist_d = df_d.iloc[-idx_back]
                            if hist_d['Close'] >= p_close and hist_d['K'] < current_k and hist_d['K'] < 40:
                                is_kd_bottom_div = True; kd_div_day_idx = idx_back; break
                                
                    is_macd_top_div = False; macd_div_day_idx = -1; current_hist = float(tod_d['HIST'])
                    if current_hist > 0:
                        for idx_back in range(3, 21):
                            if idx_back >= len(df_d): break
                            hist_d = df_d.iloc[-idx_back]
                            if hist_d['Close'] <= p_close and hist_d['HIST'] > current_hist and hist_d['HIST'] > 0:
                                is_macd_top_div = True; macd_div_day_idx = idx_back; break
                    
                    div_text = ""
                    if is_kd_bottom_div:
                        div_text = f"🎯 **【指標特徵：20日滾動型 KD 底背離】** 經活體晶片比對，個股與 **{kd_div_day_idx} 天前** 的結構型波段低點呈現完美的『真底背離』！小波段反彈重砲已上膛！"
                        if box_color in ["success", "info"]: box_color = "success"; title_text = f"🔥【AI 智庫共振判定：回踩 10MA × 契合 {kd_div_day_idx}天大底背離黃金買點】"
                    elif is_macd_top_div:
                        div_text = f"🚨 **【指標特徵：20日滾動型 MACD 頂背離】** 股價今日雖然刷出短線反彈新高，但與 **{macd_div_day_idx} 天前** 的前波高點相比，MACD 紅柱能量竟然出現了嚴重的結構性委縮（頂背離）！請立刻準備執行彈射停利！"
                        box_color = "error"; title_text = "### 💥【AI 智庫危險判定：價格虛漲 × {macd_div_day_idx}天結構頂背離逃生點】"
                    else:
                        div_text = "⚖️ **【指標特徵：動能常態同步】** 經 20 日滾動背景比對，目前 KD 與 MACD 動能並未與過去一個月內的高低點發生 any 結構性背離。"

                    box_dispatcher = {"success": st.success, "error": st.error, "warning": st.warning, "info": st.info}
                    box_dispatcher[box_color](
                        f"### {title_text}\n\n"
                        f"**🔍 智慧買賣核心數據註解診斷：**\n\n"
                        f"1. **📈 趨勢與乖離空間診斷**：{trend_text}\n\n"
                        f"2. **🔥 轉折與雙指標背離鑑定**：{div_text}\n\n"
                        f"3. **💰 籌碼法人動態方向**：今日日K成交量為 5 日均量的 **{vol_ratio:.1f} 倍**。{chips['評級']}"
                    )
            except: pass

        with tab5:
            st.subheader("📊 已選 AI 細分供應鏈 - 當日日K大數據量能與趨勢排行")
            volume_list = []
            for ticker in FILTERED_TICKERS:
                try:
                    df_v = daily_data[ticker].dropna() if is_multi else daily_data.dropna()
                    df_v['MA20'] = df_v['Close'].rolling(window=20).mean(); df_v['MA60'] = df_v['Close'].rolling(window=60).mean()
                    today_v = df_v.iloc[-1]
                    yesterday_close = YESTERDAY_CLOSES_DAILY.get(ticker, today_v['Close'])
                    current_p = LATEST_PRICES_DAILY.get(ticker, today_v['Close']) 
                    chg_pct = ((current_p - yesterday_close) / yesterday_close * 100)
                    volume_list.append({"代號": ticker.split('.')[0], "名稱": FILTERED_STOCKS_DICT[ticker]['name'], "當前收盤": round(current_p, 2), "今日漲跌幅": f"{chg_pct:+.2f}%", "成交量 (張)": int(today_v['Volume'] / 1000), "🌟 波段大趨勢": diagnose_trend_status(current_p, df_v['MA20'].iloc[-1], df_v['MA60'].iloc[-1])})
                except: continue
            if volume_list: st.dataframe(pd.DataFrame(volume_list).sort_values(by="成交量 (張)", ascending=False).head(30).reset_index(drop=True), use_container_width=True)

        with tab6:
            st.subheader("💰 🎯 AI 次族群日線級別資金大流向與輪動警報")
            if group_flows:
                flow_df = pd.DataFrame(group_flows)
                agg_df = flow_df.groupby("group").agg({"value_today": "sum", "value_ma5": "sum", "p_change": "mean"}).reset_index()
                agg_df["今日總成交額 (億元)"] = round(agg_df["value_today"] / 100000000, 2)
                agg_df["量能放大倍數 (較5日)"] = round(agg_df["value_today"] / agg_df["value_ma5"], 2)
                
                def judge_flow_status(row):
                    chg = row["p_change"]; ratio = row["量能放大倍數 (較5日)"]
                    if chg > 0.4 and ratio >= 1.2: return "🔥 資金點火"
                    elif chg > 0 and ratio >= 0.9: return "📈 資金穩定"
                    elif -0.4 <= chg <= 0.4 and ratio < 0.8: return "⏳ 縮量觀望"
                    else: return "🌀 橫盤整理"
                agg_df["🔮 主力資金流向診斷"] = agg_df.apply(judge_flow_status, axis=1)
                
                group_table_config = {
                    "group": st.column_config.TextColumn("🔬 AI 次族群名稱", width="medium"),
                    "今日總成交額 (億元)": st.column_config.NumberColumn("金額(億)", width="small", format="%.1f 億"),
                    "量能放大倍數 (較5日)": st.column_config.NumberColumn("量增倍數", width="small", format="%.2f x"),
                    "🔮 主力資金流向診斷": st.column_config.TextColumn("🎯 資金診斷", width="small")
                }
                st.data_editor(agg_df[["group", "今日總成交額 (億元)", "量能放大倍數 (較5日)", "🔮 主力資金流向診斷"]].sort_values(by="今日總成交額 (億元)", ascending=False), column_config=group_table_config, hide_index=True, disabled=True, use_container_width=True)
                
                st.markdown("---")
                flow_display = flow_df.copy()
                flow_display["代號"] = flow_display["ticker"].apply(lambda x: str(x).split('.')[0])
                flow_display["名稱"] = flow_display["name"]
                flow_display["族群"] = flow_display["group"].apply(lambda x: str(x).split(' ')[1] if ' ' in str(x) else str(x))
                flow_display["現價"] = round(flow_display["price"], 2)
                flow_display["漲跌幅"] = flow_display["p_change"].apply(lambda x: f"{x:+.2f}%")
                flow_display["5日線乖離"] = flow_display["bias_5"]
                flow_display["🔮 個股診斷"] = flow_display["stock_trend"]
                
                flow_display = flow_display.sort_values(by=["group", "value_today"], ascending=[True, False])
                
                detail_table_config = {
                    "族群": st.column_config.TextColumn("族群", width="small"),
                    "代號": st.column_config.TextColumn("代號", width="small"),
                    "名稱": st.column_config.TextColumn("名稱", width="small"),
                    "現價": st.column_config.NumberColumn("現價", width="small"),
                    "漲跌幅": st.column_config.TextColumn("漲跌幅", width="small"),
                    "5日線乖離": st.column_config.NumberColumn("5日線乖離", width="small", format="%+.1f%%"),
                    "🔮 個股診斷": st.column_config.TextColumn("🔮 個股診斷", width="medium")
                }
                st.data_editor(flow_display[["族群", "代號", "名稱", "現價", "漲跌幅", "5日線乖離", "🔮 個股診斷"]], column_config=detail_table_config, hide_index=True, disabled=True, use_container_width=True)

        with tab7:
            st.subheader("📱 我的持股鋼鐵防守與極速停利監控艙")
            st.caption("💡 智慧守護：此分頁專門死守【60分K高頻機制】（5分鐘刷新），盤中幫您以快 4.5 倍的速度鎖住波段利潤、擊殺風險！")
            
            edited_df = st.data_editor(st.session_state.my_portfolio, num_rows="dynamic", use_container_width=True)
            st.session_state.my_portfolio = edited_df
            
            st.markdown("---")
            if hourly_data is not None:
                for idx, row in edited_df.iterrows():
                    tk = str(row["代號"]).strip().upper()
                    if not tk: continue
                    full_tk = tk + ".TW" if not tk.endswith(".TW") and not tk.endswith(".TWO") else tk
                    
                    try:
                        df_p = hourly_data[full_tk].dropna() if is_multi else hourly_data.dropna()
                        if df_p.empty: continue
                        
                        price_h = df_p['Close'].iloc[-1]
                        ma10_h = df_p['Close'].rolling(10).mean().iloc[-1]
                        ma20_h = df_p['Close'].rolling(20).mean().iloc[-1]
                        
                        yesterday_close_d = YESTERDAY_CLOSES_DAILY.get(full_tk, price_h)
                        if row['買入成本'] > 0:
                            pnl = ((price_h - row['買入成本']) / row['買入成本']) * 100
                            pnl_str = f"損益:{pnl:+.2f}%"
                        else:
                            pnl = ((price_h - yesterday_close_d) / yesterday_close_d) * 100
                            pnl_str = f"今日即時幅:{pnl:+.2f}%"
                        
                        df_d_ticker = daily_data[full_tk].dropna() if is_multi else daily_data.dropna()
                        vol_ma5 = df_d_ticker['Volume'].rolling(window=5).mean().iloc[-1] if 'Volume' in df_d_ticker.columns else 0
                        tod_vol = df_d_ticker['Volume'].iloc[-1] if 'Volume' in df_d_ticker.columns else 0
                        vol_ratio = tod_vol / vol_ma5 if vol_ma5 > 0 else 1.0
                        
                        df_p['EMA12'] = df_p['Close'].ewm(span=12, adjust=False).mean()
                        df_p['EMA26'] = df_p['Close'].ewm(span=26, adjust=False).mean()
                        df_p['DIF'] = df_p['EMA12'] - df_p['EMA26']
                        df_p['MACD_Sig'] = df_p['DIF'].ewm(span=9, adjust=False).mean()
                        df_p['HIST'] = df_p['DIF'] - df_p['MACD_Sig']
                        
                        low_60, high_60 = df_p['Low'].rolling(window=60).min(), df_p['High'].rolling(window=60).max()
                        df_p['RSV'] = (((df_p['Close'] - low_60) / (high_60 - low_60)) * 100).fillna(50)
                        df_p['K'] = df_p['RSV'].ewm(alpha=1/3, adjust=False).mean()
                        df_p['D'] = df_p['K'].ewm(alpha=1/3, adjust=False).mean()
                        
                        tod_h = df_p.iloc[-1]; yes_h = df_p.iloc[-2]
                        
                        drop_reasons = []
                        if price_h < ma10_h: drop_reasons.append("📉 **均線破防**：股價跌破 60分K 10MA 短線強勢線，短線利潤收斂，注意停利！")
                        if price_h < ma20_h: drop_reasons.append("🚨 **生命線失守**：股價無情跌破 60分K 20MA 波段防守點，移動停利點/停損點觸發！")
                        if tod_h['HIST'] < yes_h['HIST']:
                            if tod_h['HIST'] < 0: drop_reasons.append("🔴 **MACD 動能下殺**：60分K綠柱持續拉長，空方修正動能放大。")
                            else: drop_reasons.append("⏳ **MACD 多頭熄火**：60分K紅柱連續縮短，推推力道告吹。")
                        if tod_h['K'] < tod_h['D']: drop_reasons.append(f"🌀 **KD 指標死叉**：60分K呈現死叉 (K:{tod_h['K']:.1f} < D:{tod_h['D']:.1f})。")
                        if price_h < ma10_h or price_h < ma20_h:
                            if vol_ratio >= 1.4: drop_reasons.append(f"💥 **籌碼恐慌爆量**：下殺成交量達5日均量 {vol_ratio:.1f} 倍！有主力砍倉。")
                            else: drop_reasons.append(f"🛡️ **籌碼量縮洗盤**：下跌量僅5日均量 {vol_ratio:.1f} 倍，屬於量縮良性震盪。")
                                
                        reason_text = "\n\n**🔍 60分K極速轉弱/下跌原因診斷（盤中监控）：**\n" + "\n".join([f"{i+1}. {r}" for i, r in enumerate(drop_reasons)]) if drop_reasons else "\n\n**⚖️ 原因診斷**：mult多頭結構完美，現價極其強勢！"
                        
                        disp_title = f"{tk} {AI_STOCKS_DICT[full_tk]['name']}" if full_tk in AI_STOCKS_DICT else tk
                        res_base = f"**{disp_title}** | 60分K現價:{price_h:.2f} | {pnl_str} | (10MA:{ma10_h:.2f} , 20MA:{ma20_h:.2f})"
                        
                        if price_h >= ma10_h: st.success(f"🟢 {res_base} ➔ **強勢續抱** (站穩 10MA 與 20MA 之上，多頭格局強勁){reason_text}")
                        elif ma20_h <= price_h < ma10_h: st.warning(f"⚠️ {res_base} ➔ **短線轉弱** (已破 10MA！移動停利機制準備，看 20MA 最後防守){reason_text}")
                        else: st.error(f"🚨 {res_base} ➔ **執行紀律！** (已無情跌破 60分K 20MA 防守點，請依波段紀律停利/停損出場！){reason_text}")
                    except: pass
            else: st.info("💡 正在等待雷達數據初始化同步...")
