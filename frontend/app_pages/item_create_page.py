# item_create_page.py
import streamlit as st

st.title("상품등록 페이지")

with st.form("create_item_form"):
    name =st.text_input("상품명")
    description = st.text_area("상품설명")
    price = st.number_input("가격", min_value=0, step=1000)
    image = st.file_uploader("이미지", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("등록")

if submit_button:
    if not name or not description or not price or not image:
        st.error("모든 필드를 입력해주세요.")
    else:
        # Here you would typically save the item to a database or perform other actions
        st.success(f"상품 '{name}'이(가) 등록되었습니다!")   





