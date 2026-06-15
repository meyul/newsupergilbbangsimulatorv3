import streamlit as st
import random
import time

st.set_page_config(page_title="범죄 노출 확률 예측", page_icon="🔮", layout="centered")

st.title("🔮 나의 범죄 노출 확률 & 결말 예측 시뮬레이터")
st.write("재미로 보는 통계 기반 시뮬레이션입니다. 정보를 입력해 보세요!")

st.markdown("---")

# 사용자 입력 폼
col1, col2, col3 = st.columns(3)
with col1:
    gender = st.selectbox("성별", ["선택하세요", "남자", "여자"])
with col2:
    age = st.number_input("나이 (만)", min_value=0, max_value=120, value=25)
with col3:
    place = st.selectbox("현재(또는 자주 있는) 장소", ["선택하세요", "집/주거지", "길거리/노상", "직장/사무실", "온라인/SNS"])

if st.button("🔮 결말 예측하기"):
    if gender == "선택하세요" or place == "선택하세요":
        st.error("🚨 성별과 장소를 올바르게 선택해 주세요!")
    else:
        with st.spinner('📊 대검찰청 범죄통계 데이터를 분석 중...'):
            time.sleep(1.5)
            
        st.success("🎯 분석이 완료되었습니다!")
        
        # 실제 통계 경향 반영 연출 로직
        if place == "온라인/SNS":
            crime_type = "사기 범죄 (보이스피싱 및 중고거래 사기)"
            probability = random.randint(35, 55)
            suspect_desc = "당신의 신뢰를 이용해 지갑을 털어 가려는 '전혀 모르는 온라인 사기꾼'"
            ending = "돈을 송금하기 직전, 금융감독원 경고 알림이 울려 극적으로 자산을 지켜내고 사기꾼은 경찰에 잡힙니다!"
        elif place == "집/주거지":
            crime_type = "절도 또는 면식범에 의한 폭행"
            probability = random.randint(15, 28)
            suspect_desc = "당신의 동선을 은밀히 파악하고 있던 '이웃 또는 안면이 있는 인물'"
            ending = "집 비밀번호를 바꾸고 홈CCTV를 설치한 당신의 철저함에 범인은 문 앞에서 발을 돌려 도망칩니다."
        elif place == "직장/사무실":
            crime_type = "직장 내 괴롭힘 및 지능범죄(배임/횡령 부류)"
            probability = random.randint(20, 35)
            suspect_desc = "겉으로는 웃으면서 뒤로 책임을 떠넘기려는 '직장 상사 또는 동료'"
            ending = "당신이 차곡차곡 모아둔 메신저 캡처와 녹음 파일 앞의 무릎을 꿇고, 고용노동부의 매콤한 맛을 보게 됩니다."
        else: # 길거리/노상
            if gender == "여자":
                crime_type = "강제추행 또는 폭력 범죄"
                probability = random.randint(25, 40)
            else:
                crime_type = "절도 또는 폭행 범죄"
                probability = random.randint(20, 35)
            suspect_desc = "술에 취했거나 욱하는 성질을 참지 못하는 '길거리의 무법자'"
            ending = "당신의 엄청난 호신술(또는 112 빠른 신고 및 대피)로 위기를 모면하고, 범인은 CCTV 투성이인 대한민국 길거리에서 30분 만에 검거됩니다."

        # 결과 화면 출력
        st.markdown("### 📊 당신의 예측 결과")
        st.metric(label="⚠️ 범죄 노출 위험도", value=f"{probability}%")
        
        st.markdown(f"> **예측 죄종:** `{crime_type}`")
        st.markdown(f"> **예측 피의자 성향:** {suspect_desc}")
        
        st.markdown("### 🎬 피해자-피의자 최종 결말")
        st.info(f"🔮 **시나리오:** {ending}")
        
        st.caption("※ 본 결과는 제공된 2024년 범죄통계 자료의 비율적 경향성을 기반으로 각색한 재미용 시뮬레이터입니다.")
