import streamlit as st

from core.auth import init_state, is_logged_in, login, logout


st.set_page_config(page_title="관리자 센터", page_icon="🗂️", layout="wide")
init_state()

start_page = st.Page("app_pages/01_start.py", title="시작", icon="🏠", default=True)
data_page = st.Page("app_pages/03_data.py", title="데이터", icon="📊")
item_page = st.Page("app_pages/02_item.py", title="아이템", icon="🛍️")

navigation = st.navigation([start_page, data_page, item_page], position="hidden")

with st.sidebar:
    st.title("관리자 센터")
    st.caption("MULTI TAB MENU")
    st.page_link(start_page)
    st.page_link(data_page)
    st.page_link(item_page)
    st.divider()

    if is_logged_in():
        st.success("로그인 중")
        st.button("로그아웃", on_click=logout, use_container_width=True)
    else:
        st.caption("실습 계정: id01 / pwd01")
        with st.form("sidebar_login_form"):
            user_id = st.text_input("아이디", value="id01")
            password = st.text_input("비밀번호", type="password", value="pwd01")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            if login(user_id, password):
                st.rerun()
            else:
                st.error("로그인 정보가 올바르지 않습니다.")

navigation.run()
