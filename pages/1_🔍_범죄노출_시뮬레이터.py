import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")
load_css()

st.markdown("<h1>🔍 범죄 노출 확률 분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>실제 경찰청 범죄 통계를 연산해 위험을 예측합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────
# 데이터 불러오기
# ─────────────────────────────────────
@st.cache_data
def load_data():
    trend = pd.read_csv("data/1_범죄_피해자_및_범죄피해_추세.csv", encoding="utf-8-sig")
    time = pd.read_csv("data/2_범죄_발생시간_및_장소.csv", encoding="utf-8-sig")
    damage = pd.read_csv("data/4_피해결과.csv", encoding="utf-8-sig")
    return trend, time, damage

try:
    trend_df, time_df, damage_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ 데이터를 불러오지 못했어요: {e}")
    data_loaded = False

# ─────────────────────────────────────
# 시간대 컬럼 정의
# ─────────────────────────────────────
TIME_COLS = ["00:00~02:59", "03:00~05:59", "06:00~08:59", "09:00~11:59",
             "12:00~14:59", "15:00~17:59", "18:00~20:59", "21:00~23:59"]

# 사용자 활동시간대 → 실제 데이터 컬럼 매핑
time_options = {
    "주로 낮에 활동 (09~18시)": ["09:00~11:59", "12:00~14:59", "15:00~17:59"],
    "저녁에 활동 (18~21시)": ["18:00~20:59"],
    "밤늦게 활동 (21~03시)": ["21:00~23:59", "00:00~02:59"],
    "새벽에 활동 (03~06시)": ["03:00~05:59"],
}

# ─────────────────────────────────────
# 연산 함수들 (실제 CSV 숫자로 계산!)
# ─────────────────────────────────────
def get_time_total_ratio(time_df, cols):
    """선택한 시간대들의 전체 범죄 발생 비율(%) 합산"""
    total_row = time_df[time_df["죄종"] == "계"].iloc[0]
    grand_total = total_row["계"]
    selected = sum(total_row[c] for c in cols)
    return round(selected / grand_total * 100, 1)

def get_top_crimes_by_time(time_df, cols, top_n=3):
    """선택한 시간대에 '가장 많이 발생한 범죄 유형' 계산"""
    exclude = ["계", "강력범죄 소계", "절도범죄"]  # 합계성 행 제외
    result = []
    for _, row in time_df.iterrows():
        crime = row["죄종"]
        if crime in exclude:
            continue
        count = sum(row[c] for c in cols)
        if count > 0:
            result.append((crime, int(count)))
    result.sort(key=lambda x: x[1], reverse=True)
    total = sum(c for _, c in result)
    top = []
    for crime, count in result[:top_n]:
        ratio = round(count / total * 100, 1) if total > 0 else 0
        top.append((crime, count, ratio))
    return top

def get_damage_distribution(damage_df, crime_name):
    """특정 범죄의 피해 금액 분포 계산"""
    money_cols = ["피해무", "1만원 이하", "10만원 이하", "100만원 이하",
                  "1000만원 이하", "1억원 이하", "5억원 이하", "50억원 이하", "50억원 초과"]
    row = damage_df[damage_df["죄종"] == crime_name]
    if row.empty:
        return None
    row = row.iloc[0]
    total = row["계"]
    if total == 0:
        return None
    dist = []
    for col in money_cols:
        if col in row.index:
            ratio = round(row[col] / total * 100, 1)
            dist.append((col, ratio))
    dist.sort(key=lambda x: x[1], reverse=True)
    return dist

def get_gender_ratio(trend_df, crime_type, gender):
    """특정 범죄유형의 성별 피해 구성비"""
    row = trend_df[
        (trend_df["범죄유형"] == crime_type) & (trend_df["성별"] == gender)
    ]
    if row.empty:
        return None
    return row.iloc[0]["2024년 구성비"]

# ─────────────────────────────────────
# 사용자 입력
# ─────────────────────────────────────
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
name = st.text_input("🧑 이름(또는 닉네임)", "익명")
gender = st.radio("👤 성별", ["남성", "여성"], horizontal=True)
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

# ─────────────────────────────────────
# 분석 실행
# ─────────────────────────────────────
if st.button("⚡ 확률 분석 시작") and data_loaded:
    cols = time_options[active_time]

    # ── 종합 위험 점수 계산 ──
    score = night_out * 4
    sns_map = {"비공개": 0, "약간 공개": 5, "보통": 10, "많이 공개": 15, "전체 공개": 20}
    score += sns_map[sns_open]
    score += careless * 3
    if risky_area:
        score += 15
    if self_defense:
        score -= 15

    time_ratio = get_time_total_ratio(time_df, cols)
    score += time_ratio * 0.5

    gender_ratio = get_gender_ratio(trend_df, "전체범죄", gender)
    score += gender_ratio * 0.3

    probability = max(0, min(100, round(score)))

    # ── 결과 헤더 ──
    st.markdown("---")
    st.markdown(f"<h2>📊 {name}님의 분석 결과</h2>", unsafe_allow_html=True)
    st.progress(probability / 100)
    st.metric("종합 노출 확률", f"{probability}%")

    if probability < 25:
        color, title = "#00ff9d", "😎 SAFE ENDING"
    elif probability < 50:
        color, title = "#00f0ff", "🙂 NORMAL ENDING"
    elif probability < 75:
        color, title = "#ffb800", "😰 WARNING ENDING"
    else:
        color, title = "#ff2e5e", "💀 DANGER ENDING"

    st.markdown(
        f"<div class='glass-card' style='border-color:{color}; box-shadow:0 0 25px {color}44;'>"
        f"<h3 style='color:{color} !important; text-shadow:0 0 12px {color}88;'>{title}</h3>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 🎯 예측 1: 어떤 범죄에 노출될까?
    # ══════════════════════════════════════
    top_crimes = get_top_crimes_by_time(time_df, cols, top_n=3)
    if top_crimes:
        crime_html = ""
        for i, (crime, count, ratio) in enumerate(top_crimes, 1):
            crime_html += (
                f"<p style='margin:8px 0;'>"
                f"<b style='color:#ff2e9a;'>{i}위. {crime}</b>"
                f"&nbsp;—&nbsp; 이 시간대 발생 {count:,}건 "
                f"(해당 시간 범죄 중 <b style='color:#00f0ff;'>{ratio}%</b>)"
                f"</p>"
            )
        st.markdown(
            f"<div class='glass-card'>"
            f"<h3>🎯 당신이 노출될 가능성이 높은 범죄 TOP3</h3>"
            f"<p style='color:#a0a0d0; font-size:0.9em;'>"
            f"※ {active_time} 시간대 실제 발생 통계 기준</p>"
            f"{crime_html}"
            f"</div>",
            unsafe_allow_html=True
        )
        top1_crime = top_crimes[0][0]
    else:
        top1_crime = None

    # ══════════════════════════════════════
    # 🕐 예측 2: 언제 당할까?
    # ══════════════════════════════════════
    total_row = time_df[time_df["죄종"] == "계"].iloc[0]
    grand_total = total_row["계"]
    time_risks = [(c, round(total_row[c] / grand_total * 100, 1)) for c in TIME_COLS]
    time_risks_sorted = sorted(time_risks, key=lambda x: x[1], reverse=True)
    most_dangerous_time = time_risks_sorted[0]

    st.markdown(
        f"<div class='glass-card'>"
        f"<h3>🕐 가장 위험한 시간대 분석</h3>"
        f"<p>📍 당신의 활동시간(<b>{active_time}</b>)의 범죄 발생 비율: "
        f"<b style='color:#ff2e9a;'>{time_ratio}%</b></p>"
        f"<p>⚠️ 전체 통계상 가장 위험한 시간대: "
        f"<b style='color:#ff2e5e;'>{most_dangerous_time[0]}</b> "
        f"(전체 범죄의 <b>{most_dangerous_time[1]}%</b> 발생)</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 💰 예측 3: 피해 규모는?
    # ══════════════════════════════════════
    damage_map = {
        "절도범죄": "절도", "절도": "절도",
        "강도": "강도", "사기": "사기",
        "손괴": "손괴", "공갈": "공갈"
    }
    target_crime = damage_map.get(top1_crime, "절도") if top1_crime else "절도"
    dist = get_damage_distribution(damage_df, target_crime)

    if dist:
        top_damage = dist[:3]
        dmg_html = ""
        for label, ratio in top_damage:
            display = "피해 없음" if label == "피해무" else label + " 피해"
            dmg_html += (
                f"<p style='margin:6px 0;'>"
                f"💸 <b>{display}</b>: "
                f"<b style='color:#ff2e9a;'>{ratio}%</b></p>"
            )
        st.markdown(
            f"<div class='glass-card'>"
            f"<h3>💰 예상 피해 규모 ({target_crime} 기준)</h3>"
            f"<p style='color:#a0a0d0; font-size:0.9em;'>"
            f"※ 실제 {target_crime} 피해 금액 분포 통계</p>"
            f"{dmg_html}"
            f"</div>",
            unsafe_allow_html=True
        )

    # ══════════════════════════════════════
    # 👤 예측 4: 성별 피해 통계
    # ══════════════════════════════════════
    crime_list = ["전체범죄", "살인범죄", "강도범죄"]
    gender_html = ""
    for ct in crime_list:
        gr = get_gender_ratio(trend_df, ct, gender)
        if gr is not None:
            gender_html += (
                f"<p style='margin:6px 0;'>"
                f"• <b>{ct}</b> 피해자 중 <b>{gender}</b> 비율: "
                f"<b style='color:#00f0ff;'>{gr}%</b></p>"
            )
    st.markdown(
        f"<div class='glass-card'>"
        f"<h3>👤 {gender} 피해자 통계 (2024년)</h3>"
        f"{gender_html}"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 💡 맞춤 안전 팁
    # ══════════════════════════════════════
    tips = []
    if top1_crime:
        tips.append(f"당신의 활동시간엔 '{top1_crime}' 위험이 가장 높아요. 특히 주의하세요.")
    if "밤늦게" in active_time or "새벽" in active_time:
        tips.append("심야·새벽은 위험 시간대입니다. 밝고 사람 많은 길로 다니세요.")
    if sns_open in ["많이 공개", "전체 공개"]:
        tips.append("SNS 공개 범위를 줄이면 표적이 될 확률이 낮아져요.")
    if careless >= 6:
        tips.append("귀중품 관리에 더 신경 쓰세요. 절도 피해가 가장 흔합니다.")
    if risky_area:
        tips.append("위험 지역 방문을 줄이세요.")
    if not self_defense:
        tips.append("기본 안전 교육 이수를 추천합니다.")
    if not tips:
        tips.append("좋은 습관을 유지하고 계세요! 👍")

    tip_html = "".join([f"<li style='margin:6px 0;'>{t}</li>" for t in tips])
    st.markdown(
        f"<div class='glass-card'>"
        f"<h3>💡 맞춤 안전 팁</h3>"
        f"<ul style='color:#c0c0e0;'>{tip_html}</ul>"
        f"</div>",
        unsafe_allow_html=True
    )
