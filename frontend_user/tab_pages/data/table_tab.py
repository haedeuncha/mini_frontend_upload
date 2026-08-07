from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from core.auth import is_logged_in
from core.product_client import ProductAPIError, get_products


def show_table() -> None:
    """관리자 상품 조회와 검색 필터를 보여줍니다."""
    st.subheader("상품 관리")
    st.caption("상품명, 등록일, 가격 조건으로 등록된 상품을 검색합니다.")

    if not is_logged_in():
        st.warning("로그인 후 상품 관리 기능을 이용할 수 있습니다.")
        return

    try:
        products = get_products()
    except ProductAPIError as error:
        st.error(str(error))
        return

    dataframe = pd.DataFrame(products)
    if dataframe.empty:
        st.info("등록된 상품이 없습니다.")
        return

    dataframe["created_at"] = pd.to_datetime(dataframe["created_at"], errors="coerce")
    dataframe["price"] = pd.to_numeric(dataframe["price"], errors="coerce")

    st.markdown("#### 검색 조건")
    with st.form("product_search_form"):
        name_keyword = st.text_input("상품명", placeholder="예: 아메리카노")
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date = st.date_input("등록일 시작", value=None)
        with date_col2:
            end_date = st.date_input("등록일 종료", value=None)

        price_col1, price_col2 = st.columns(2)
        with price_col1:
            min_price = st.number_input("최소 가격", min_value=0, value=0, step=100)
        with price_col2:
            max_price = st.number_input("최대 가격", min_value=0, value=10_000_000, step=100)

        searched = st.form_submit_button("검색", type="primary")

    filtered = dataframe.copy()
    if name_keyword:
        filtered = filtered[filtered["name"].str.contains(name_keyword, case=False, na=False)]
    if start_date:
        filtered = filtered[filtered["created_at"].dt.date >= start_date]
    if end_date:
        filtered = filtered[filtered["created_at"].dt.date <= end_date]
    if min_price > max_price:
        st.warning("최소 가격은 최대 가격보다 클 수 없습니다.")
        return
    filtered = filtered[filtered["price"].between(min_price, max_price)]

    if searched:
        st.success(f"검색 결과: {len(filtered)}건")

    if filtered.empty:
        st.info("검색 조건에 맞는 상품이 없습니다.")
        return

    display = filtered[["id", "name", "price", "created_at"]].copy()
    display["price"] = display["price"].map(lambda value: f"{int(value):,}원")
    display["created_at"] = display["created_at"].dt.strftime("%Y-%m-%d %H:%M")
    display.columns = ["상품 ID", "상품명", "가격", "등록일"]

    st.dataframe(display, use_container_width=True, hide_index=True)
    st.caption(f"전체 {len(products)}건 중 {len(filtered)}건 표시")
