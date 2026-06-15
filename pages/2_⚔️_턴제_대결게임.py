import streamlit as st
import random

st.set_page_config(page_title="턴제 대결 게임", page_icon="⚔️")

st.title("⚔️ 범죄자 턴제 대결 게임")
st.markdown("범죄자를 상대로 턴제 전투를 펼쳐보세요!")
st.markdown("---")

# 게임 상태 초기화
def init_game():
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.log = []
    st.session_state.game_over = False
    st.session_state.defending = False

if "player_hp" not in st.session_state:
    init_game()

# 체력 표시
col1, col2 = st.columns(2)
with col1:
    st.subheader("🧑 나")
    st.progress(max(0, st.session_state.player_hp) / 100)
    st.write(f"HP: {max(0, st.session_state.player_hp)} / 100")
with col2:
    st.subheader("🦹 범죄자")
    st.progress(max(0, st.session_state.enemy_hp) / 100)
    st.write(f"HP: {max(0, st.session_state.enemy_hp)} / 100")

st.markdown("---")

# 적의 턴 처리 함수
def enemy_turn():
    if st.session_state.enemy_hp <= 0:
        return
    enemy_dmg = random.randint(8, 18)
    if st.session_state.defending:
        enemy_dmg = enemy_dmg // 2
        st.session_state.log.append(f"🛡️ 방어로 데미지를 절반으로 줄였습니다!")
        st.session_state.defending = False
    st.session_state.player_hp -= enemy_dmg
    st.session_state.log.append(f"🦹 범죄자의 공격! {enemy_dmg} 데미지를 입었습니다.")

# 승패 체크
def check_end():
    if st.session_state.enemy_hp <= 0:
        st.session_state.log.append("🎉 범죄자를 물리쳤습니다! 승리!")
        st.session_state.game_over = True
    elif st.session_state.player_hp <= 0:
        st.session_state.log.append("💀 당신은 쓰러졌습니다... 패배!")
        st.session_state.game_over = True

# 행동 버튼
if not st.session_state.game_over:
    st.markdown("### ⚡ 행동을 선택하세요")
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button("🗡️ 공격"):
            dmg = random.randint(10, 20)
            st.session_state.enemy_hp -= dmg
            st.session_state.log.append(f"🗡️ 공격! 범죄자에게 {dmg} 데미지!")
            check_end()
            if not st.session_state.game_over:
                enemy_turn()
                check_end()
            st.rerun()

    with b2:
        if st.button("🛡️ 방어"):
            st.session_state.defending = True
            st.session_state.log.append("🛡️ 방어 자세를 취합니다!")
            enemy_turn()
            check_end()
            st.rerun()

    with b3:
        if st.button("💥 강공격"):
            # 강공격: 높은 데미지지만 빗나갈 확률 있음
            if random.random() < 0.6:
                dmg = random.randint(20, 35)
                st.session_state.enemy_hp -= dmg
                st.session_state.log.append(f"💥 강공격 명중! {dmg} 데미지!")
            else:
                st.session_state.log.append("💨 강공격이 빗나갔습니다!")
            check_end()
            if not st.session_state.game_over:
                enemy_turn()
                check_end()
            st.rerun()
else:
    # 게임 종료 화면
    if st.session_state.enemy_hp <= 0:
        st.success("🎉 승리했습니다! 범죄자를 물리쳤어요!")
        st.balloons()
    else:
        st.error("💀 패배했습니다... 다시 도전하세요!")

# 전투 로그
st.markdown("---")
st.markdown("### 📜 전투 로그")
log_box = st.container()
with log_box:
    for line in reversed(st.session_state.log[-8:]):
        st.write(line)

# 재시작 버튼
st.markdown("---")
if st.button("🔄 게임 다시 시작"):
    init_game()
    st.rerun()
