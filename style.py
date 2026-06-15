import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* 전체 배경 - 다크 네온 그라데이션 */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #e0e0ff;
        }

        /* 기본 텍스트 밝게 */
        .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
        .stMarkdown, [data-testid="stWidgetLabel"] p,
        [data-testid="stMarkdownContainer"] p {
            color: #e0e0ff;
        }

        label, .stSlider label, .stSelectSlider label,
        .stTextInput label, .stCheckbox label, .stRadio label,
        .stSelectbox label {
            color: #e0e0ff !important;
        }

        /* ⭐⭐ 텍스트 입력칸 - 어두운 배경 + 흰 글씨 ⭐⭐ */
        .stTextInput input,
        .stTextInput > div > div > input {
            color: #ffffff !important;
            background-color: #1a1735 !important;
            border: 1px solid #ff2e9a88 !important;
            border-radius: 8px !important;
            caret-color: #ff2e9a !important;
        }
        /* 입력칸 placeholder(연한 안내글자) */
        .stTextInput input::placeholder {
            color: #8888bb !important;
        }
        /* 입력칸 클릭(포커스) 했을 때 */
        .stTextInput input:focus {
            border: 1px solid #00f0ff !important;
            box-shadow: 0 0 10px #00f0ff55 !important;
        }

        /* ⭐ 셀렉트박스(드롭다운) - 어두운 배경 + 흰 글씨 */
        .stSelectbox > div > div {
            background-color: #1a1735 !important;
            border: 1px solid #ff2e9a88 !important;
            border-radius: 8px !important;
        }
        .stSelectbox > div > div div {
            color: #ffffff !important;
        }
        /* 드롭다운 펼쳤을 때 나오는 목록 */
        [data-baseweb="popover"] li {
            background-color: #1a1735 !important;
            color: #ffffff !important;
        }
        [data-baseweb="popover"] li:hover {
            background-color: #302b63 !important;
        }

        /* ⭐ 라디오 / 체크박스 글자 */
        .stRadio p, .stCheckbox p {
            color: #e0e0ff !important;
        }

        /* ⭐ 슬라이더 숫자 표시 */
        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"],
        .stSlider [data-baseweb="slider"] div {
            color: #e0e0ff !important;
        }
        /* 슬라이더 현재값 말풍선 */
        .stSlider [data-testid="stThumbValue"] {
            color: #00f0ff !important;
        }

        /* 폰트 */
        html, body, [class*="css"] {
            font-family: 'Pretendard', 'Apple SD Gothic Neo', sans-serif;
        }

        /* 제목 네온 효과 */
        h1 {
            color: #ff2e9a !important;
            text-shadow: 0 0 10px #ff2e9a, 0 0 20px #ff2e9a55;
            letter-spacing: 1px;
        }
        h2, h3 {
            color: #00f0ff !important;
            text-shadow: 0 0 8px #00f0ff66;
        }

        /* 버튼 - 네온 글로우 */
        .stButton > button {
            background: linear-gradient(90deg, #ff2e9a, #7b2ff7);
            color: white !important;
            border: none;
            border-radius: 12px;
            padding: 0.6em 1.4em;
            font-weight: 700;
            box-shadow: 0 0 15px #ff2e9a66;
            transition: all 0.25s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 0 25px #ff2e9a, 0 0 40px #7b2ff766;
        }
        .stButton > button p {
            color: #ffffff !important;
        }

        /* 카드형 컨테이너 (글래스모피즘) */
        .glass-card {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            padding: 24px;
            margin: 12px 0;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }

        /* progress 바 네온 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #00f0ff, #ff2e9a) !important;
        }

        /* metric */
        [data-testid="stMetricValue"] {
            color: #00f0ff !important;
            text-shadow: 0 0 10px #00f0ff88;
        }
        [data-testid="stMetricLabel"] {
            color: #e0e0ff !important;
        }

        /* 데이터프레임(표) 다크 */
        [data-testid="stDataFrame"] {
            background-color: #1a1735 !important;
        }

        /* expander(접기/펼치기) 다크 */
        .streamlit-expanderHeader, [data-testid="stExpander"] summary {
            color: #e0e0ff !important;
            background-color: rgba(255,255,255,0.05) !important;
        }

        /* 구분선 */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #ff2e9a, transparent);
        }

        /* 사이드바 */
        [data-testid="stSidebar"] {
            background: rgba(15, 12, 41, 0.9);
            border-right: 1px solid #ff2e9a33;
        }
        [data-testid="stSidebar"] * {
            color: #e0e0ff !important;
        }
        </style>
    """, unsafe_allow_html=True)
