import streamlit as st
import pandas as pd
from style import load_css

st.set_page_config(page_title="범죄 노출 시뮬레이터", page_icon="🔍")
load_css()

st.markdown("<h1>🔍 범죄 노출 확률 분석</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>성별·나이·시간·지역을 실제 통계로 종합 분석합니다.</p>", unsafe_allow_html=True)
st.markdown("---")

# ═══════════════════════════════════════
# 숫자 변환
# ═══════════════════════════════════════
def to_num(x):
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
    region1 = pd.read_csv("data/seoul_crime_statistics.csv", encoding="utf-8-sig")
    region2 = pd.read_csv("data/seoul_district_data.csv", encoding="utf-8-sig")
    busan = pd.read_csv("data/busan_district_data.csv", encoding="utf-8-sig")
    return male, female, time, region1, region2, busan

try:
    male_df, female_df, time_df, region1_df, region2_df, busan_df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"⚠️ 데이터를 불러오지 못했어요: {e}")
    data_loaded = False

# ═══════════════════════════════════════
# 컬럼/매핑 정의
# ═══════════════════════════════════════
TIME_COLS = ["00:00~02:59", "03:00~05:59", "06:00~08:59", "09:00~11:59",
             "12:00~14:59", "15:00~17:59", "18:00~20:59", "21:00~23:59"]

time_options = {
    "주로 낮에 활동 (09~18시)": ["09:00~11:59", "12:00~14:59", "15:00~17:59"],
    "저녁에 활동 (18~21시)": ["18:00~20:59"],
    "밤늦게 활동 (21~03시)": ["21:00~23:59", "00:00~02:59"],
    "새벽에 활동 (03~06시)": ["03:00~05:59"],
}

age_options = {
    "10대 이하 (18세 이하)": {"남성": "남_18세이하", "여성": "18세이하"},
    "20대": {"남성": "남_20세", "여성": "20세"},
    "30대": {"남성": "남_30세이하", "여성": "30세이하"},
    "40대": {"남성": "남_40세이하", "여성": "40세이하"},
    "50대": {"남성": "남_50세이하", "여성": "50세이하"},
    "60대": {"남성": "남_60세이하", "여성": "60세이하"},
    "65세 이상": {"남성": "남_65세이상", "여성": "65세이상"},
}

# 지역별 자치구 (어느 파일에 있는지 구분)
SEOUL_REGION1 = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구"]
SEOUL_REGION2 = ["성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구",
                 "마포구", "양천구", "강서구", "구로구", "금천구", "영등포구"]
BUSAN_DISTRICTS = ["영도구", "부산진구", "동래구", "남구", "북구", "강서구",
                   "해운대구", "사하구", "금정구", "연제구", "수영구", "사상구", "기장군"]

# 사용자에게 보여줄 지역 선택지 (도시 구분)
city_options = {
    "서울특별시": SEOUL_REGION1 + SEOUL_REGION2,
    "부산광역시": BUSAN_DISTRICTS,
}

EXCLUDE = ["계", "소계", "(%)"]

# ═══════════════════════════════════════
# 연산 함수
# ═══════════════════════════════════════
def get_crime_by_profile(gender, age_col_name):
    scores = {}
    if gender == "남성":
        for _, row in male_df.iterrows():
            crime = str(row["소분류"]).strip()
            if crime in EXCLUDE:
                continue
            if age_col_name in male_df.columns:
                val = to_num(row[age_col_name])
                if val > 0:
                    scores[crime] = val
    else:
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
    scores = {}
    for _, row in time_df.iterrows():
        crime = str(row["세부죄종"]).strip()
        if crime in EXCLUDE:
            continue
        count = sum(to_num(row[c]) for c in cols)
        if count > 0:
            scores[crime] = count
    return scores

def get_crime_by_region(city, district):
    """선택한 도시·자치구의 범죄별 건수"""
    scores = {}
    if city == "서울특별시" and district in SEOUL_REGION1:
        # region1: 소분류 컬럼이 직접 있음
        for _, row in region1_df.iterrows():
            crime = str(row["소분류"]).strip()
            if crime in EXCLUDE:
                continue
            if district in region1_df.columns:
                val = to_num(row[district])
                if val > 0:
                    scores[crime] = val
    else:
        # region2(서울 뒤) 또는 busan: 행 순서로 region1의 소분류 매칭
        df = region2_df if city == "서울특별시" else busan_df
        for idx, row in df.iterrows():
            if idx >= len(region1_df):
                break
            crime = str(region1_df.iloc[idx]["소분류"]).strip()
            if crime in EXCLUDE:
                continue
            if district in df.columns:
                val = to_num(row[district])
                if val > 0:
                    scores[crime] = val
    return scores

def get_region_total(city, district):
    """선택한 구의 전체 범죄 건수 (계 행 = 첫 데이터 행)"""
    if city == "서울특별시" and district in SEOUL_REGION1:
        row = region1_df[(region1_df["대분류"] == "계") &
                         (region1_df["소분류"] == "계")].iloc[0]
        return to_num(row[district])
    else:
        df = region2_df if city == "서울특별시" else busan_df
        return to_num(df.iloc[0][district])  # 첫 행이 '계'

def normalize(d):
    total = sum(d.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in d.items()}

def combine_scores(profile, time, region):
    p, t, r = normalize(profile), normalize(time), normalize(region)
    combined = {}
    for crime in set(p) | set(t) | set(r):
        combined[crime] = (p.get(crime, 0) * 0.45 +
                           t.get(crime, 0) * 0.30 +
                           r.get(crime, 0) * 0.25)
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)

def get_total_time_ratio(cols):
    total_row = time_df[(time_df["죄종"] == "계") & (time_df["세부죄종"] == "계")].iloc[0]
    grand = to_num(total_row["계"])
    sel = sum(to_num(total_row[c]) for c in cols)
    return round(sel / grand * 100, 1) if grand else 0

def get_city_avg(city):
    """도시의 자치구 평균 범죄 건수"""
    districts = city_options[city]
    totals = [get_region_total(city, d) for d in districts]
    return sum(totals) / len(totals) if totals else 0

# ═══════════════════════════════════════
# 사용자 입력
# ═══════════════════════════════════════
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
name = st.text_input("🧑 이름(또는 닉네임)", "익명")
gender = st.radio("👤 성별", ["남성", "여성"], horizontal=True)
age_group = st.selectbox("🎂 나이대", list(age_options.keys()))
city = st.selectbox("🏙️ 도시", list(city_options.keys()))
district = st.selectbox("🗺️ 자치구", city_options[city])
active_time = st.selectbox("🕐 주로 활동하는 시간대", list(time_options.keys()))
night_out = st.slider("🌙 밤늦게 돌아다니는 빈도 (주당 횟수)", 0, 7, 2)
sns_open = st.select_slider(
    "📱 SNS 개인정보 공개 정도",
    options=["비공개", "약간 공개", "보통", "많이 공개", "전체 공개"],
    value="보통"
)
careless = st.slider("💸 귀중품 관리 부주의 정도 (0~10)", 0, 10, 5)
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
    if self_defense:
        score -= 15

    time_ratio = get_total_time_ratio(cols)
    score += time_ratio * 0.5

    # 지역 위험도 (그 도시 평균 대비)
    region_total = get_region_total(city, district)
    city_avg = get_city_avg(city)
    if city_avg > 0:
        region_factor = region_total / city_avg
        score += (region_factor - 1) * 15
    else:
        region_factor = 1

    probability = max(0, min(100, round(score)))

    # ── 통합 위험 범죄 순위 ──
    profile_scores = get_crime_by_profile(gender, age_col)
    time_scores = get_crime_by_time(cols)
    region_scores = get_crime_by_region(city, district)
    ranked = combine_scores(profile_scores, time_scores, region_scores)

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
        f"<p style='color:#e0e0ff;'>{gender} · {age_group} · {city} {district} · {active_time}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 🎯 가장 위험한 범죄
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
            f"<b>{gender} {age_group}</b>이고 <b>{city} {district}</b>의 "
            f"<b>{active_time}</b>에 활동하는 당신은<br>통계상 "
            f"<b style='color:#ff2e9a; font-size:1.25em;'>「{top1[0]}」</b>에 "
            f"가장 취약합니다!</p>"
            f"<hr>"
            f"<p style='color:#a0a0d0; font-size:0.85em;'>"
            f"※ 성별·연령(45%) + 시간대(30%) + 지역(25%) 종합 연산</p>"
            f"{rank_html}"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("해당 조건의 데이터를 찾지 못했어요.")

    # ══════════════════════════════════════
    # 🗺️ 지역 분석
    # ══════════════════════════════════════
    risk_word = "높은" if region_factor > 1 else "낮은"
    risk_color = "#ff2e5e" if region_factor > 1 else "#00ff9d"
    st.markdown(
        f"<div class='glass-card'>"
        f"<h3>🗺️ 지역 분석 ({city} {district})</h3>"
        f"<p>📍 <b>{district}</b> 연간 총 범죄 발생: "
        f"<b style='color:#ff2e9a;'>{int(region_total):,}건</b></p>"
        f"<p>📊 {city} 자치구 평균({int(city_avg):,}건) 대비: "
        f"<b style='color:{risk_color};'>{round(region_factor*100)}%</b> "
        f"(평균보다 {risk_word} 편)</p>"
        f"</div>",
        unsafe_allow_html=True
    )

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
        f"<p>⚠️ 가장 위험한 시간: <b style='color:#ff2e5e;'>{most_dangerous[0]}</b> "
        f"(전체의 {most_dangerous[1]}%)</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ══════════════════════════════════════
    # 💡 맞춤 안전 팁
    # ══════════════════════════════════════
    tips = []
    if ranked:
        tips.append(f"당신은 '{ranked[0][0]}'에 가장 취약합니다. 특별히 주의하세요.")
    if region_factor > 1:
        tips.append(f"{district}는 {city} 평균보다 범죄가 많은 지역입니다. 주변을 살피세요.")
    if "밤늦게" in active_time or "새벽" in active_time:
        tips.append("심야·새벽은 위험 시간대입니다. 밝고 사람 많은 길로 다니세요.")
    if sns_open in ["많이 공개", "전체 공개"]:
        tips.append("SNS 공개 범위를 줄이면 표적이 될 확률이 낮아져요.")
    if careless >= 6:
        tips.append("귀중품 관리에 더 신경 쓰세요.")
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
