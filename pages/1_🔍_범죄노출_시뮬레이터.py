import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")
load_css()

st.markdown("<h1>🔍 범죄 노출 확률 분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>당신의 성별·나이·활동시간을 실제 통계로 종합 분석합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# ═══════════════════════════════════════
# 숫자 변환 함수 (쉼표, 하이픈, 괄호 처리)
# ═══════════════════════════════════════
def to_num(x):
    """'1,187,197' → 1187197 / '-' → 0 / 공백 → 0"""
    if pd.isna(x):
        return 0
    s = str(x).strip().replace(",", "").replace("(", "").replace(")", "")
    if s in ["-", "", "nan"]:
        return 0
    try:
        return float(s)
    except ValueError:
        return 0

# ═══════════════════════════════════════
# 데이터 불러오기
# ═══════════════════════════════════════
@st.cache_data
def load_data():
    male = pd.read_csv("data/crime_statistics_korea.csv", encoding="utf-8-sig")
    female = pd.read_csv("data/table_data.csv", encoding="utf-8-sig")
    time = pd.read_csv("data/crime_occurrence_by_time.csv", encoding="utf-8-sig")
    return male, female, time

try:
    male_df, female_df, time_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ 데이터를 불러오지 못했어요: {e}")
    data_loaded = False

# ═══════════════════════════════════════
# 컬럼/매핑 정의
# ═══════════════════════════════════════
# 시간대 컬럼
TIME_COLS = ["00:00~02:59", "03:00~05:59", "06:00~08:59", "09:00~11:59",
             "12:00~14:59", "15:00~17:59", "18:00~20:59", "21:00~23:59"]

# 사용자 활동시간 → 실제 컬럼
time_options = {
    "주로 낮에 활동 (09~18시)": ["09:00~11:59", "12:00~14:59", "15:00~17:59"],
    "저녁에 활동 (18~21시)": ["18:00~20:59"],
    "밤늦게 활동 (21~03시)": ["21:00~23:59", "00:00~02:59"],
    "새벽에 활동 (03~06시)": ["03:00~05:59"],
}

# 나이대 → 남성/여성 파일의 연령 컬럼명
# 남성 파일: 남_18세이하, 남_20세 ...
# 여성 파일: 18세이하, 20세 ... (헤더가 그냥 나이로 되어있음)
age_options = {
    "10대 이하 (18세 이하)": {"남성": "남_18세이하", "여성": "18세이하"},
    "20대": {"남성": "남_20세", "여성": "20세"},
    "30대": {"남성": "남_30세이하", "여성": "30세이하"},
    "40대": {"남성": "남_40세이하", "여성": "40세이하"},
    "50대": {"남성": "남_50세이하", "여성": "50세이하"},
    "60대": {"남성": "남_60세이하", "여성": "60세이하"},
    "65세 이상": {"남성": "남_65세이상", "여성": "65세이상"},
}

# 합계성 행(개별 범죄 아님) 제외
EXCLUDE = ["계", "소계", "(%)"]

# ═══════════════════════════════════════
# 연산 함수
# ═══════════════════════════════════════
def get_crime_by_profile(gender, age_col_name):
    """선택한 성별·나이대가 많이 당하는 범죄별 건수 {범죄명: 건수}"""
    scores = {}
    if gender == "남성":
        df = male_df
        for _, row in df.iterrows():
            crime = str(row["소분류"]).strip()
            if crime in EXCLUDE:
                continue
            if age_col_name in df.columns:
                val = to_num(row[age_col_name])
                if val > 0:
                    scores[crime] = val
    else:  # 여성: table_data.csv 사용 (행 순서가 male_df와 동일)
        # 여성 파일은 소분류 컬럼이 없으므로, male_df의 소분류를 행 번호로 매칭
        for idx, row in female_df.iterrows():
            if idx >= len(male_df):
                break
            crime = str(male_df.iloc[idx]["소분류"]).strip()
            if crime in EXCLUDE:
                continue
            if age_col_name in female_df.columns:
                val = to_num(row[age_col_name])
                if val > 0:
                    scores[crime] = val
    return scores

def get_crime_by_time(cols):
    """선택한 시간대에 많이 발생하는 범죄별 건수 {범죄명: 건수}"""
    scores = {}
    for _, row in time_df.iterrows():
        crime = str(row["세부죄종"]).strip()
        if crime in EXCLUDE:
            continue
        count = sum(to_num(row[c]) for c in cols)
        if count > 0:
            scores[crime] = count
    return scores

def normalize(d):
    """건수를 0~1 비율로 정규화"""
    total = sum(d.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in d.items()}

def combine_scores(profile_scores, time_scores):
    """프로필 60% + 시간대 40% 종합 → 위험 범죄 순위"""
    p = normalize(profile_scores)
    t = normalize(time_scores)
    combined = {}
    for crime in set(p) | set(t):
        combined[crime] = p.get(crime, 0) * 0.6 + t.get(crime, 0) * 0.4
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)

def get_total_time_ratio(cols):
    """선택 시간대의 전체 범죄 발생 비율(%)"""
    total_row = time_df[(time_df["죄종"] == "계") & (time_df["세부죄종"] == "계")].iloc[0]
    grand = to_num(total_row["계"])
    sel = sum(to_num(total_row[c]) for c in cols)
    return round(sel / grand * 100, 1) if grand else 0

# ═══════════════════════════════════════
# 사용자 입력
# ═══════════════════════════════════════
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
name = st.text_input("🧑 이름(또는 닉네임)", "익명")
gender = st.radio("👤 성별", ["남성", "여성"], horizontal=True)
age_group = st.selectbox("🎂 나이대", list(age_options.keys()))
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

# ═══════════════════════════════════════
# 분석 실행
# ═══════════════════════════════════════
if st.button("⚡ 통합 분석 시작") and data_loaded:
    cols = time_options[active_time]
    age_col = age_options[age_group][gender]

    # ── 종합 노출 확률 점수 ──
    score = night_out * 4
    sns_map = {"비공개": 0, "약간 공개": 5, "보통": 10, "많이 공개": 15, "전체 공개": 20}
    score += sns_map[sns_open]
    score += careless * 3
    if risky_area:
        score += 15
    if self_defense:
        score -= 15

    time_ratio = get_total_time_ratio(cols)
    score += time_ratio * 0.5

    probability = max(0, min(100, round(score)))

    # ── 통합 위험 범죄 순위 ──
    profile_scores = get_crime_by_profile(gender, age_col)
    time_scores = get_crime_by_time(cols)
    ranked = combine_scores(profile_scores, time_scores)

    # ── 결과 헤더 ──
    st.markdown("---")
    st.markdown(f"<h2>📊 {name}님의 통합 분석 결과</h2>", unsafe_allow_html=True)
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
        f"<p style='color:#e0e0ff;'>{gender} · {age_group} · {active_time}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 🎯 당신에게 가장 위험한 범죄 (통합!)
    # ══════════════════════════════════════
    if ranked:
        top1 = ranked[0]
        rank_html = ""
        for i, (crime, sc) in enumerate(ranked[:5], 1):
            pct = round(sc * 100, 1)
            bar_color = "#ff2e5e" if i == 1 else "#ff2e9a" if i == 2 else "#7b2ff7"
            rank_html += (
                f"<div style='margin:10px 0;'>"
                f"<p style='margin:0 0 4px 0;'>"
                f"<b style='color:{bar_color};'>{i}위. {crime}</b> "
                f"<span style='color:#00f0ff;'>위험도 {pct}</span></p>"
                f"<div style='background:rgba(0,0,0,0.4); border-radius:6px; height:14px; overflow:hidden;'>"
                f"<div style='width:{min(100, pct*4)}%; height:100%; "
                f"background:linear-gradient(90deg,{bar_color},#ffffff44); border-radius:6px;'></div>"
                f"</div></div>"
            )
        st.markdown(
            f"<div class='glass-card' style='border-color:#ff2e5e;'>"
            f"<h3 style='color:#ff2e5e !important;'>🎯 당신에게 가장 위험한 범죄</h3>"
            f"<p style='color:#e0e0ff; font-size:1.05em;'>"
            f"<b>{gender} {age_group}</b>이고 <b>{active_time}</b>에 활동하는 당신은<br>"
            f"통계상 <b style='color:#ff2e9a; font-size:1.25em;'>「{top1[0]}」</b>에 "
            f"가장 취약합니다!</p>"
            f"<hr>"
            f"<p style='color:#a0a0d0; font-size:0.85em;'>"
            f"※ 성별·연령별 피해통계(60%) + 시간대 발생통계(40%) 종합 연산</p>"
            f"{rank_html}"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("해당 조건의 데이터를 찾지 못했어요. 입력을 바꿔보세요.")

    # ══════════════════════════════════════
    # 🕐 시간대 분석
    # ══════════════════════════════════════
    total_row = time_df[(time_df["죄종"] == "계") & (time_df["세부죄종"] == "계")].iloc[0]
    grand = to_num(total_row["계"])
    time_risks = [(c, round(to_num(total_row[c]) / grand * 100, 1)) for c in TIME_COLS]
    most_dangerous = sorted(time_risks, key=lambda x: x[1], reverse=True)[0]

    st.markdown(
        f"<div class='glass-card'>"
        f"<h3>🕐 시간대 분석</h3>"
        f"<p>📍 당신의 활동시간(<b>{active_time}</b>) 범죄 발생 비율: "
        f"<b style='color:#ff2e9a;'>{time_ratio}%</b></p>"
        f"<p>⚠️ 전체 통계상 가장 위험한 시간: "
        f"<b style='color:#ff2e5e;'>{most_dangerous[0]}</b> "
        f"(전체 범죄의 {most_dangerous[1]}%)</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 💡 맞춤 안전 팁
    # ══════════════════════════════════════
    tips = []
    if ranked:
        tips.append(f"당신은 '{ranked[0][0]}'에 가장 취약합니다. 특별히 주의하세요.")
    if "밤늦게" in active_time or "새벽" in active_time:
        tips.append("심야·새벽은 위험 시간대입니다. 밝고 사람 많은 길로 다니세요.")
    if sns_open in ["많이 공개", "전체 공개"]:
        tips.append("SNS 공개 범위를 줄이면 표적이 될 확률이 낮아져요.")
    if careless >= 6:
        tips.append("귀중품 관리에 더 신경 쓰세요.")
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
