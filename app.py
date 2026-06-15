import streamlit as st

st.set_page_config(
    page_title="범죄 시뮬레이터",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 범죄 노출 & 대결 시뮬레이터")
st.markdown("---")

st.markdown(
    """
    ### 👋 환영합니다!
    이 앱은 두 가지 기능을 제공합니다.

    - **🔍 범죄 노출 시뮬레이터** : 나의 생활 습관을 입력하면
      범죄에 노출될 확률과 예상 결말을 예측해줍니다.
    - **⚔️ 턴제 대결 게임** : 범죄자를 상대로 턴제 전투를 펼쳐보세요!

    👈 **왼쪽 사이드바**에서 원하는 페이지를 선택하세요.
    """
)

st.info("⚠️ 이 앱은 교육·오락용 시뮬레이션이며, 실제 범죄 통계와 무관합니다.")

st.markdown("---")
st.caption("Made with ❤️ by 당곡고 학생 | Streamlit + GitHub")
