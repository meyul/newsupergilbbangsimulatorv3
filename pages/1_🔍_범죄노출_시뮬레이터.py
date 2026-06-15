import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")
load_css()

st.markdown("<h1>🔍 범죄 노출 확률 분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>실제 범죄 통계 데이터를 기반으로 위험도를 분석합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# ── 데이터 불러오기 (캐시로 빠르게!) ──
@st.cache_data
def load_data():
    trend = pd.read_csv("data/1_범죄_피해자_및_범죄피해_추세.csv")
    time = pd.read_csv("data/2_범죄_발생시간_및_장소.csv")
    return trend, time

try:
    trend_df, time_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ 데이터를 불러오지 못했어요: {e}")
    data_loaded = False

# ── 시간대 → 범죄 비율 계산 함수 ──
def get_time_risk(time_df, time_label):
    """선택한 시간대의 전체 범죄 대비 발생 비율(%)을 반환"""
    total_row = time_df[time_df["죄종"] == "계"].iloc[0]
    total = total_row["계"]
    count = total_row[time_label]
    return round(count / total * 100, 1)

# ── 사용자 입력 ──
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
name = st.text_input("🧑 이름(또는 닉네임)", "익명")
gender = st.radio("👤 성별", ["남성", "여성"], horizontal=True)

time_options = {
    "주로 낮에 활동 (09~18시)": ["09:00~11:59", "12:00~14:59", "15:00~17:59"],
    "저녁에 활동 (18~21시)": ["18:00~20:59"],
    "밤늦게 활동 (21~03시)": ["21:00~23:59", "00:00~02:59"],
    "새벽에 활동 (03~06시)": ["03:00~05:59"],
}
active_time = st.selectbox("🕐 주로 활동하는 시간대", list(time_options.keys()))

night_out = st.slider("🌙 밤늦게 돌아다니는 빈도 (주당 횟수)", 0, 7, 2)
sns_open = st.select_slider(
    "📱 SNS 개인정보 공개 정도",
    options=["비공개", "약간 공개", "보통", "많이 공개", "전체 공개"],
    value="보통"
)
careless = st.slider("💸 귀중품 관리 부주의 정도 (0~10)", 0, 10, 5)
risky_area = st.checkbox("🏙️ 위험 지역에 자주 방문한다")
self_defense = st.checkbox("🛡️ 호신술/안전 교육을 받은 적이 있다")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("⚡ 확률 분석 시작") and data_loaded:
    # ── 기본 위험 점수 ──
    score = night_out * 4
    sns_map = {"비공개": 0, "약간 공개": 5, "보통": 10, "많이 공개": 15, "전체 공개": 20}
    score += sns_map[sns_open]
    score += careless * 3
    if risky_area:
        score += 15
    if self_defense:
        score -= 15

    # ── 통계 반영 1: 활동 시간대 범죄 비율 ──
    time_labels = time_options[active_time]
    time_risk = sum(get_time_risk(time_df, t) for t in time_labels)
    score += time_risk * 0.5  # 시간대 위험 가중

    # ── 통계 반영 2: 성별 전체범죄 구성비 ──
    gender_row = trend_df[
        (trend_df["범죄유형"] == "전체범죄") & (trend_df["성별"] == gender)
    ].iloc[0]
    gender_ratio = gender_row["2024년 구성비"]  # 남44.2 / 여29.9
    score += gender_ratio * 0.3

    probability = max(0, min(100, round(score)))

    # ── 결과 출력 ──
    st.markdown("---")
    st.markdown(f"<h2>📊 {name}님의 분석 결과</h2>", unsafe_allow_html=True)
    st.progress(probability / 100)
    st.metric("종합 노출 확률", f"{probability}%")

    # 통계 근거 표시
    st.markdown(f"""
    <div class='glass-card'>
        <h3>📈 분석 근거 (실제 통계)</h3>
        <p>🕐 <b>{active_time}</b> 시간대 범죄 발생 비율: <b style='color:#ff2e9a;'>{time_risk}%</b></p>
        <p>👤 <b>{gender}</b> 전체범죄 피해 구성비(2024): <b style='color:#ff2e9a;'>{gender_ratio}%</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ── 결말 예측 ──
    if probability < 25:
        color, title, desc = "#00ff9d", "😎 SAFE ENDING", "위험을 잘 피해 평온한 일상을 보냅니다!"
    elif probability < 50:
        color, title, desc = "#00f0ff", "🙂 NORMAL ENDING", "가끔 위험에 노출되지만 큰 사고 없이 지나갑니다."
    elif probability < 75:
        color, title, desc = "#ffb800", "😰 WARNING ENDING", "위험 상황을 자주 마주칩니다. 습관 개선이 필요해요!"
    else:
        color, title, desc = "#ff2e5e", "💀 DANGER ENDING", "범죄 노출 위험이 매우 높습니다! 즉시 대비하세요!"

    st.markdown(f"""
    <div class='glass-card' style='border-color:{color}; box-shadow:0 0 25px {color}44;'>
        <h3 style='color:{color} !important; text-shadow:0 0 12px {color}88;'>{title}</h3>
        <p style='color:#e0e0ff; font-size:1.05em;'>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 안전 팁 ──
    tips = []
    if "밤늦게" in active_time or "새벽" in active_time:
        tips.append("심야·새벽 시간대는 범죄 위험이 높아요. 밝은 길로 다니세요.")
    if night_out >= 4:
        tips.append("밤 외출을 줄여보세요.")
    if sns_open in ["많이 공개", "전체 공개"]:
        tips.append("SNS 개인정보 공개 범위를 줄이세요.")
    if careless >= 6:
        tips.append("귀중품을 항상 몸에 지니고 관리하세요.")
    if risky_area:
        tips.append("위험 지역 방문을 자제하세요.")
    if not self_defense:
        tips.append("기본 안전 교육을 받아보는 것을 추천합니다.")
    if not tips:
        tips.append("지금처럼 안전 습관을 잘 유지하세요! 👍")

    tip_html = "".join([f"<li style='margin:6px 0;'>{t}</li>" for t in tips])
    st.markdown(f"""
    <div class='glass-card'>
        <h3>💡 안전 팁</h3>
        <ul style='color:#c0c0e0;'>{tip_html}</ul>
    </div>
    """, unsafe_allow_html=True)
