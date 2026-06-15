import streamlit as st

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")

st.title("🔍 나의 범죄 노출 확률 시뮬레이터")
st.markdown("아래 항목을 입력하면 노출 확률과 예상 결말을 예측해드려요!")
st.markdown("---")

# 사용자 입력
name = st.text_input("이름(또는 닉네임)", "익명")

night_out = st.slider("🌙 밤늦게 돌아다니는 빈도 (주당 횟수)", 0, 7, 2)
sns_open = st.select_slider(
    "📱 SNS 개인정보 공개 정도",
    options=["비공개", "약간 공개", "보통", "많이 공개", "전체 공개"],
    value="보통"
)
careless = st.slider("💸 귀중품 관리 부주의 정도 (0~10)", 0, 10, 5)
risky_area = st.checkbox("🏙️ 위험 지역에 자주 방문한다")
self_defense = st.checkbox("🛡️ 호신술/안전 교육을 받은 적이 있다")

st.markdown("---")

if st.button("확률 예측하기 🎯"):
    # 위험 점수 계산
    score = 0
    score += night_out * 5  # 최대 35

    sns_map = {"비공개": 0, "약간 공개": 5, "보통": 10, "많이 공개": 15, "전체 공개": 20}
    score += sns_map[sns_open]

    score += careless * 3  # 최대 30

    if risky_area:
        score += 15
    if self_defense:
        score -= 15

    # 0~100 범위로 보정
    probability = max(0, min(100, score))

    st.subheader(f"📊 {name}님의 범죄 노출 확률")
    st.progress(probability / 100)
    st.metric("노출 확률", f"{probability}%")

    # 결말 예측
    st.markdown("### 🔮 예상 결말")
    if probability < 25:
        st.success("😎 **안전 결말** : 당신은 위험을 잘 피해 평온한 일상을 보냅니다!")
    elif probability < 50:
        st.info("🙂 **무난 결말** : 가끔 위험에 노출되지만 큰 사고 없이 지나갑니다.")
    elif probability < 75:
        st.warning("😰 **주의 결말** : 위험 상황을 자주 마주칩니다. 습관 개선이 필요해요!")
    else:
        st.error("💀 **위험 결말** : 범죄에 노출될 위험이 매우 높습니다! 즉시 대비하세요!")

    # 조언
    st.markdown("### 💡 안전 팁")
    tips = []
    if night_out >= 4:
        tips.append("밤 외출을 줄이고, 외출 시 밝은 길로 다니세요.")
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

    for t in tips:
        st.write(f"- {t}")
