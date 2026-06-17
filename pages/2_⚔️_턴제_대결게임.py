import streamlit as st
import pandas as pd
import random
from style import load_css

st.set_page_config(page_title="범죄자 대결 게임", page_icon="⚔️")
load_css()

st.markdown("<h1>⚔️ 범죄자 BATTLE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a0a0d0;'>실제 범죄 통계로 강해진 범죄자들을 물리쳐라!</p>", unsafe_allow_html=True)
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
# 데이터로 범죄자(적) 만들기
# ═══════════════════════════════════════
@st.cache_data
def build_enemies():
    """시간대 데이터로 범죄자 능력치 생성"""
    time_df = pd.read_csv("data/crime_occurrence_by_time.csv", encoding="utf-8-sig")

    strong_crimes = ["살인기수", "살인미수등", "강도", "강간", "방화"]

    enemies = []
    exclude = ["계", "소계"]
    for _, row in time_df.iterrows():
        crime = str(row["세부죄종"]).strip()
        big = str(row["죄종"]).strip()   # ⭐ '대분류' → '죄종'으로 수정!
        if crime in exclude:
            continue
        total = to_num(row["계"])
        if total < 1000:
            continue

        hp = int(50 + min(100, total / 5000))

        if crime in strong_crimes or big == "강력범죄":
            atk_min, atk_max = 15, 28
            tier = "강력"
        elif big == "폭력범죄":
            atk_min, atk_max = 12, 22
            tier = "폭력"
        else:
            atk_min, atk_max = 8, 16
            tier = "일반"

        enemies.append({
            "name": crime,
            "hp": hp,
            "max_hp": hp,
            "atk_min": atk_min,
            "atk_max": atk_max,
            "tier": tier,
            "total": int(total),
        })

    enemies.sort(key=lambda x: x["total"])
    return enemies

try:
    ALL_ENEMIES = build_enemies()
    data_loaded = True
    if len(ALL_ENEMIES) == 0:
        st.error("⚠️ 적을 만들 데이터가 없어요. CSV를 확인해주세요.")
        data_loaded = False
except Exception as e:
    st.error(f"⚠️ 데이터를 불러오지 못했어요: {e}")
    data_loaded = False
    ALL_ENEMIES = []

TIER_EMOJI = {"강력": "🔴", "폭력": "🟠", "일반": "🟡"}

# ═══════════════════════════════════════
# 게임 상태 초기화
# ═══════════════════════════════════════
def init_game():
    chosen = random.sample(ALL_ENEMIES, min(5, len(ALL_ENEMIES)))
    chosen.sort(key=lambda x: x["total"])
    st.session_state.enemies = [dict(e, hp=e["max_hp"]) for e in chosen]
    st.session_state.stage = 0
    st.session_state.player_hp = 100
    st.session_state.player_max_hp = 100
    st.session_state.log = []
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.defending = False
    st.session_state.potions = 2

if "enemies" not in st.session_state and data_loaded:
    init_game()

# ═══════════════════════════════════════
# HP 바 그리기
# ═══════════════════════════════════════
def hp_bar(label, hp, max_hp, color, emoji):
    pct = max(0, hp) / max_hp * 100 if max_hp else 0
    st.markdown(
        f"<div class='glass-card' style='padding:16px;'>"
        f"<h3 style='margin:0; color:{color} !important;'>{emoji} {label}</h3>"
        f"<div style='background:rgba(0,0,0,0.4); border-radius:10px; height:22px; margin-top:10px; overflow:hidden;'>"
        f"<div style='width:{pct}%; height:100%; "
        f"background:linear-gradient(90deg,{color},#ffffff44); "
        f"box-shadow:0 0 12px {color}; border-radius:10px; transition:width 0.4s ease;'></div>"
        f"</div>"
        f"<p style='text-align:right; color:#e0e0ff; margin:6px 0 0 0;'>HP {max(0,int(hp))} / {int(max_hp)}</p>"
        f"</div>",
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════
# 게임 화면
# ═══════════════════════════════════════
if data_loaded and "enemies" in st.session_state:
    stage = st.session_state.stage
    total_stages = len(st.session_state.enemies)

    st.markdown(
        f"<div class='glass-card' style='padding:14px; text-align:center;'>"
        f"<p style='margin:0; color:#00f0ff;'>"
        f"⚔️ STAGE {min(stage+1, total_stages)} / {total_stages} "
        f"&nbsp;|&nbsp; 🧪 회복약 {st.session_state.potions}개</p>"
        f"</div>",
        unsafe_allow_html=True
    )

    if not st.session_state.game_over and stage < total_stages:
        enemy = st.session_state.enemies[stage]
        emoji = TIER_EMOJI.get(enemy["tier"], "🦹")

        col1, col2 = st.columns(2)
        with col1:
            hp_bar("나", st.session_state.player_hp,
                   st.session_state.player_max_hp, "#00f0ff", "🧑")
        with col2:
            hp_bar(f"{enemy['name']}", enemy["hp"],
                   enemy["max_hp"], "#ff2e5e", emoji)

        st.markdown(
            f"<div class='glass-card'>"
            f"<p style='color:#e0e0ff;'>"
            f"{emoji} <b style='color:#ff2e5e;'>{enemy['name']}</b> "
            f"({enemy['tier']}범죄) 등장!</p>"
            f"<p style='color:#a0a0d0; font-size:0.85em;'>"
            f"※ 실제 연간 {enemy['total']:,}건 발생 → HP {enemy['max_hp']}, "
            f"공격력 {enemy['atk_min']}~{enemy['atk_max']}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        def enemy_attack():
            e = st.session_state.enemies[st.session_state.stage]
            dmg = random.randint(e["atk_min"], e["atk_max"])
            if st.session_state.defending:
                dmg = dmg // 2
                st.session_state.log.append("🛡️ 방어 성공! 데미지 절반 감소!")
                st.session_state.defending = False
            st.session_state.player_hp -= dmg
            st.session_state.log.append(f"{emoji} {e['name']}의 공격! {dmg} 데미지!")

        def check_state():
            if st.session_state.player_hp <= 0:
                st.session_state.log.append("💀 당신은 쓰러졌습니다... 패배!")
                st.session_state.game_over = True
                return
            if st.session_state.enemies[st.session_state.stage]["hp"] <= 0:
                e = st.session_state.enemies[st.session_state.stage]
                st.session_state.log.append(f"🎉 {e['name']}을(를) 물리쳤다!")
                st.session_state.stage += 1
                if st.session_state.stage < total_stages:
                    heal = 15
                    st.session_state.player_hp = min(
                        st.session_state.player_max_hp,
                        st.session_state.player_hp + heal)
                    st.session_state.log.append(f"✨ 다음 상대 등장 전 HP {heal} 회복!")
                else:
                    st.session_state.victory = True
                    st.session_state.game_over = True
                    st.session_state.log.append("👑 모든 범죄자를 물리쳤다! 완전 승리!")

        st.markdown("<h3>⚡ 행동 선택</h3>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)

        with b1:
            if st.button("🗡️ 공격"):
                dmg = random.randint(12, 22)
                enemy["hp"] -= dmg
                st.session_state.log.append(f"🗡️ 공격! {enemy['name']}에게 {dmg} 데미지!")
                check_state()
                if not st.session_state.game_over and st.session_state.enemies[st.session_state.stage]["hp"] > 0:
                    enemy_attack()
                    check_state()
                st.rerun()

        with b2:
            if st.button("💥 강공격"):
                if random.random() < 0.6:
                    dmg = random.randint(22, 38)
                    enemy["hp"] -= dmg
                    st.session_state.log.append(f"💥 강공격 명중! {dmg} 데미지!")
                else:
                    st.session_state.log.append("💨 강공격이 빗나갔다!")
                check_state()
                if not st.session_state.game_over and st.session_state.enemies[st.session_state.stage]["hp"] > 0:
                    enemy_attack()
                    check_state()
                st.rerun()

        with b3:
            if st.button("🛡️ 방어"):
                st.session_state.defending = True
                st.session_state.log.append("🛡️ 방어 자세!")
                enemy_attack()
                check_state()
                st.rerun()

        with b4:
            if st.button("🧪 회복"):
                if st.session_state.potions > 0:
                    st.session_state.potions -= 1
                    heal = 30
                    st.session_state.player_hp = min(
                        st.session_state.player_max_hp,
                        st.session_state.player_hp + heal)
                    st.session_state.log.append(f"🧪 회복약 사용! HP {heal} 회복!")
                    enemy_attack()
                    check_state()
                else:
                    st.session_state.log.append("❌ 회복약이 없습니다!")
                st.rerun()

    elif st.session_state.game_over:
        if st.session_state.victory:
            st.markdown(
                f"<div class='glass-card' style='text-align:center; border-color:#00ff9d; box-shadow:0 0 30px #00ff9d44;'>"
                f"<h2 style='color:#00ff9d !important;'>👑 ALL CLEAR!</h2>"
                f"<p style='color:#e0e0ff;'>모든 범죄자를 물리쳤습니다! 당신은 진정한 영웅!</p>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.balloons()
        else:
            cleared = st.session_state.stage
            st.markdown(
                f"<div class='glass-card' style='text-align:center; border-color:#ff2e5e; box-shadow:0 0 30px #ff2e5e44;'>"
                f"<h2 style='color:#ff2e5e !important;'>💀 GAME OVER</h2>"
                f"<p style='color:#e0e0ff;'>{cleared}명의 범죄자를 물리쳤습니다.<br>"
                f"다시 도전하세요!</p>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("<h3>📜 BATTLE LOG</h3>", unsafe_allow_html=True)
    log_html = "".join([
        f"<p style='color:#b0b0e0; margin:4px 0; font-size:0.92em;'>▸ {line}</p>"
        for line in reversed(st.session_state.log[-8:])
    ])
    st.markdown(
        f"<div class='glass-card'>{log_html if log_html else '<p style=color:#8080b0;>전투를 시작하세요!</p>'}</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    if st.button("🔄 새 게임 시작"):
        init_game()
        st.rerun()
