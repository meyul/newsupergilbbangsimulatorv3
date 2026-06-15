import streamlit as st

def load_css():
    st.markdown("""
        <style>
        /* 전체 배경 - 다크 네온 그라데이션 */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #e0e0ff;
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
            color: white;
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
            color: #fff;
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

        /* 입력 위젯 */
        .stTextInput input, .stSlider, .stSelectSlider {
            color: #e0e0ff;
        }

        /* progress 바 네온 */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #00f0ff, #ff2e9a) !important;
        }

        /* metric */
        [data-testid="stMetricValue"] {
            color: #00f0ff;
            text-shadow: 0 0 10px #00f0ff88;
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
        </style>
    """, unsafe_allow_html=True)
