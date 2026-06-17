import streamlit as st
from style import load_css

st.set_page_config(
    page_title="범죄 시뮬레이터",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 범죄 노출 & 대결 시뮬레이터")
st.markdown("---")
load_css()

# 히어로 영역
st.markdown("""
<div style='text-align:center; padding: 30px 0;'>
    <h1 style='font-size:2.8em;'>🚨 CRIME SIMULATOR</h1>
    <p style='color:#a0a0d0; font-size:1.1em; letter-spacing:2px;'>
        범죄 노출 예측 · 턴제 대결 시스템
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    ### 👋 환영합니다!
    이 앱은 두 가지 기능을 제공합니다.
st.markdown("---")

    - **🔍 범죄 노출 시뮬레이터** : 나의 생활 습관을 입력하면
      범죄에 노출될 확률과 예상 결말을 예측해줍니다.
    - **⚔️ 턴제 대결 게임** : 범죄자를 상대로 턴제 전투를 펼쳐보세요!
# 기능 카드
st.markdown("""
<div class='glass-card'>
    <h3>🔍 범죄 노출 시뮬레이터</h3>
    <p style='color:#c0c0e0;'>
        당신의 생활 습관을 분석해 범죄 노출 확률과
        예상 결말을 예측합니다.
    </p>
</div>

    👈 **왼쪽 사이드바**에서 원하는 페이지를 선택하세요.
    """
)
<div class='glass-card'>
    <h3>⚔️ 턴제 대결 게임</h3>
    <p style='color:#c0c0e0;'>
        범죄자를 상대로 전략적인 턴제 전투를 펼치세요.
        공격 · 방어 · 강공격으로 승리를 쟁취하라!
    </p>
</div>
""", unsafe_allow_html=True)

st.info("⚠️ 이 앱은 교육·오락용 시뮬레이션이며, 실제 범죄 통계와 무관합니다.")
st.markdown("""
<p style='text-align:center; color:#8080b0; margin-top:20px;'>
    👈 왼쪽 사이드바에서 시작하세요
</p>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤️ by 당곡고 학생 | Streamlit + GitHub")
st.markdown("""
<p style='text-align:center; color:#6060a0; font-size:0.85em;'>
    ⚠️ 본 앱은 교육·오락용 시뮬레이션입니다<br>
    Made with 💜 by 당곡고 학생
</p>
""", unsafe_allow_html=True)
