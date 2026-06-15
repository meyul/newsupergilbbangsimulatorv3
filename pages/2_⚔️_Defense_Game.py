import streamlit as st
import random

st.set_page_config(page_title="범죄자 퇴치 게임", page_icon="⚔️", layout="centered")

st.title("⚔️ 만난 범죄자를 상대하라! 턴제 방어 게임")
st.write("일촉즉발의 상황! 올바른 대처법을 골라 범죄자를 무력화하고 안전하게 탈출하세요.")
st.markdown("---")

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'player_hp' not in st.session_state:
    st.session_state.player_hp = 100
if 'enemy_hp' not in st.session_state:
    st.session_state.enemy_hp = 100
if 'enemy_type' not in st.session_state:
    st.session_state.enemy_type = ""
if 'game_log' not in st.session_state:
    st.session_state.game_log = []

# 게임 시작 버튼
if not st.session_state.game_started:
    if st.button("🎮 게임 시작하기"):
        st.session_state.game_started = True
        st.session_state.player_hp = 100
        st.session_state.enemy_hp = 100
        st.session_state.enemy_type = random.choice(["보이스피싱 사기꾼", "골목길 미행범", "중고거래 빌런"])
        st.session_state.game_log = [f"🚨 무시무시한 [{st.session_state.enemy_type}]이(가) 나타났다!"]
        st.rerun()

# 게임 진행 화면
if st.session_state.game_started:
    st.subheader(" 체력 상황")
    col_p, col_e = st.columns(2)
    with col_p:
        st.write(f"🧑‍💼 **나의 멘탈/체력:** {st.session_state.player_hp} / 100")
        st.progress(max(0, st.session_state.player_hp))
    with col_e:
        st.write(f"🦹 **{st.session_state.enemy_type}의 전의:** {st.session_state.enemy_hp} / 100")
        st.progress(max(0, st.session_state.enemy_hp))
        
    st.markdown("---")
    st.subheader(" ACTIONS: 어떻게 대처하시겠습니까?")
    
    act_col1, act_col2, act_col3 = st.columns(3)
    
    if st.session_state.enemy_type == "보이스피싱 사기꾼":
        with act_col1:
            if st.button("📞 '링크 보내주세요' 하고 누르기"):
                st.session_state.player_hp -= 30
                st.session_state.game_log.append("❌ 악성 앱이 설치되어 멘탈에 치명타를 입었습니다! (-30 HP)")
                st.rerun()
        with act_col2:
            if st.button("🛑 일단 끊고 해당 기관 공식 번호로 재확인"):
                st.session_state.enemy_hp -= 50
                st.session_state.game_log.append("🏽 올바른 대처! 사기꾼이 당황하여 말을 더듬습니다. (-50 Damage)")
                st.rerun()
        with act_col3:
            if st.button(" 대포통장 명의 대여해주기"):
                st.session_state.player_hp -= 50
                st.session_state.game_log.append("💥 공범으로 연루될 위기! 경찰서 뷰를 보게 생겼습니다. (-50 HP)")
                st.rerun()
                
    elif st.session_state.enemy_type == "골목길 미행범":
        with act_col1:
            if st.button("🏃 편의점이나 사람이 많은 밝은 곳으로 뛰기"):
                st.session_state.enemy_hp -= 60
                st.session_state.game_log.append("🏽 훌륭합니다! 미행범이 CCTV와 사람들을 의식해 접근을 포기합니다. (-60 Damage)")
                st.rerun()
        with act_col2:
            if st.button("📱 이어폰 끼고 스마트폰 보면서 유유히 걷기"):
                st.session_state.player_hp -= 40
                st.session_state.game_log.append("❌ 표적이 되기 가장 좋은 행동입니다! 미행범이 거리를 좁힙니다. (-40 HP)")
                st.rerun()
        with act_col3:
            if st.button("🚨 '112 긴급신고 앱' 원터치 신고 발동"):
                st.session_state.enemy_hp -= 40
                st.session_state.game_log.append("🏽 경찰 두 명이 근처 지구대에서 출동 대기 상태에 들어갑니다! (-40 Damage)")
                st.rerun()

    elif st.session_state.enemy_type == "중고거래 빌런":
        with act_col1:
            if st.button("🤝 '안전결재'라며 보내준 외부 링크로 결제"):
                st.session_state.player_hp -= 40
                st.session_state.game_log.append("❌ 가짜 피싱 사이트였습니다! 돈만 날아갔습니다. (-40 HP)")
                st.rerun()
        with act_col2:
            if st.button("📍 낮 시간에 사람 많은 지하철역 개찰구에서 직거래"):
                st.session_state.enemy_hp -= 70
                st.session_state.game_log.append("🏽 사기꾼이 발붙일 곳이 없습니다. 완벽한 방어! (-70 Damage)")
                st.rerun()
        with act_col3:
            if st.button("💸 '선입금 시 할인' 유혹에 바로 송금"):
                st.session_state.player_hp -= 50
                st.session_state.game_log.append("💥 송금하자마자 상대방이 탈퇴했습니다. 혈압 상승! (-50 HP)")
                st.rerun()

    st.markdown("---")
    st.subheader("📜 전투 기록")
    for log in reversed(st.session_state.game_log):
        st.write(log)
        
    if st.session_state.enemy_hp <= 0:
        st.balloons()
        st.success("🎉 승리! 올바른 대처법으로 범죄자를 성공적으로 격퇴하고 안전을 확보했습니다!")
        st.session_state.game_started = False
        st.markdown("""
        ### 💡 필수 범죄자 퇴치법 요약
        1. **지능형 사기범:** 의심스러운 외부 링크(URL)는 절대 누르지 말고, 공식 고객센터 번호로 직접 전화해 확인하세요.
        2. **대인 범죄(미행/폭행):** 이어폰을 낀 채 주변 경계를 게을리하는 행동은 금물입니다. 위기 시 주변 편의점(아동안전지킴이집 등)이나 밝은 곳으로 즉시 대피하세요.
        3. **중고거래:** 가급적 대낮에 사람이 많은 곳에서 직거래를 하거나, 플랫폼 내 공식 안전결제 시스템만 이용하세요.
        """)
        
    elif st.session_state.player_hp <= 0:
        st.error("💀 패배... 잘못된 대처로 인해 범죄자에게 취약점을 노출당했습니다. 대처법을 다시 숙지해 보세요!")
        st.session_state.game_started = False
