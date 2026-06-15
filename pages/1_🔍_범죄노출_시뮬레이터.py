import streamlit as st
from style import load_css

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")
load_css()

st.markdown("<h1>🔍 범죄 노출 확률 분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>당신의 데이터를 입력하면 AI가 위험도를 분석합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# 입력 카드
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
name = st.text_input("🧑 이름(또는 닉네임)", "익명")
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

if st.button("⚡ 확률 분석 시작"):
    # 위험 점수 계산
    score = night_out * 5
    sns_map = {"비공개": 0, "약간 공개": 5, "보통": 10, "많이 공개": 15, "전체 공개": 20}
    score += sns_map[sns_open]
    score += careless * 3
    if risky_area:
        score += 15
    if self_defense:
        score -= 15

    probability = max(0, min(100, score))

    st.markdown("---")
    st.markdown(f"<h2>📊 {name}님의 분석 결과</h2>", unsafe_allow_html=True)
    st.progress(probability / 100)
    st.metric("노출 확률", f"{probability}%")

    # 결말 예측 카드
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

    # 안전 팁
    tips = []
    if night_out >= 4:
        tips.append("밤 외출을 줄이고, 밝은 길로 다니세요.")
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
