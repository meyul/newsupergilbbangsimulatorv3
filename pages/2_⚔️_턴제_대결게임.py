import streamlit as st
import random
from style import load_css

st.set_page_config(page_title="턴제 대결 게임", page_icon="⚔️")
load_css()

st.markdown("<h1>⚔️ 범죄자 BATTLE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>전략적인 턴제 전투로 범죄자를 제압하라!</p>", unsafe_allow_html=True)
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

# HP 바를 그려주는 함수 (네온 스타일)
def hp_bar(label, hp, color, emoji):
    pct = max(0, hp)
    st.markdown(f"""
    <div class='glass-card' style='padding:16px;'>
        <h3 style='margin:0; color:{color} !important;'>{emoji} {label}</h3>
        <div style='background:rgba(0,0,0,0.4); border-radius:10px; height:22px; margin-top:10px; overflow:hidden;'>
            <div style='width:{pct}%; height:100%;
                background:linear-gradient(90deg, {color}, #ffffff44);
                box-shadow:0 0 12px {color}; border-radius:10px;
                transition:width 0.4s ease;'></div>
        </div>
        <p style='text-align:right; color:#e0e0ff; margin:6px 0 0 0;'>HP {pct} / 100</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    hp_bar("나", st.session_state.player_hp, "#00f0ff", "🧑")
with col2:
    hp_bar("범죄자", st.session_state.enemy_hp, "#ff2e5e", "🦹")

st.markdown("---")

# 적 턴
def enemy_turn():
    if st.session_state.enemy_hp <= 0:
        return
    enemy_dmg = random.randint(8, 18)
    if st.session_state.defending:
        enemy_dmg = enemy_dmg // 2
        st.session_state.log.append("🛡️ 방어 성공! 데미지 절반 감소!")
        st.session_state.defending = False
    st.session_state.player_hp -= enemy_dmg
    st.session_state.log.append(f"🦹 범죄자의 공격! {enemy_dmg} 데미지를 입었다.")

def check_end():
    if st.session_state.enemy_hp <= 0:
        st.session_state.log.append("🎉 범죄자를 물리쳤다! 승리!")
        st.session_state.game_over = True
    elif st.session_state.player_hp <= 0:
        st.session_state.log.append("💀 당신은 쓰러졌다... 패배!")
        st.session_state.game_over = True

# 행동 버튼
if not st.session_state.game_over:
    st.markdown("<h3>⚡ 행동 선택</h3>", unsafe_allow_html=True)
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
            st.session_state.log.append("🛡️ 방어 자세!")
            enemy_turn()
            check_end()
            st.rerun()

    with b3:
        if st.button("💥 강공격"):
            if random.random() < 0.6:
                dmg = random.randint(20, 35)
                st.session_state.enemy_hp -= dmg
                st.session_state.log.append(f"💥 강공격 명중! {dmg} 데미지!")
            else:
                st.session_state.log.append("💨 강공격이 빗나갔다!")
            check_end()
            if not st.session_state.game_over:
                enemy_turn()
                check_end()
            st.rerun()
else:
    if st.session_state.enemy_hp <= 0:
        st.markdown("""
        <div class='glass-card' style='text-align:center; border-color:#00ff9d; box-shadow:0 0 30px #00ff9d44;'>
            <h2 style='color:#00ff9d !important;'>🎉 VICTORY</h2>
            <p style='color:#e0e0ff;'>범죄자를 물리쳤습니다!</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class='glass-card' style='text-align:center; border-color:#ff2e5e; box-shadow:0 0 30px #ff2e5e44;'>
            <h2 style='color:#ff2e5e !important;'>💀 GAME OVER</h2>
            <p style='color:#e0e0ff;'>당신은 쓰러졌습니다...</p>
        </div>
        """, unsafe_allow_html=True)

# 전투 로그
st.markdown("---")
st.markdown("<h3>📜 BATTLE LOG</h3>", unsafe_allow_html=True)
log_html = "".join([
    f"<p style='color:#b0b0e0; margin:4px 0; font-size:0.92em;'>▸ {line}</p>"
    for line in reversed(st.session_state.log[-8:])
])
st.markdown(f"<div class='glass-card'>{log_html if log_html else '<p style=color:#808;>전투를 시작하세요!</p>'}</div>", unsafe_allow_html=True)

# 재시작
st.markdown("---")
if st.button("🔄 다시 시작"):
    init_game()
    st.rerun()
