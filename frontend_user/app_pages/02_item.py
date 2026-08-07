import pandas as pd
import streamlit as st

from core.auth import is_logged_in
from core.product_client import ProductAPIError, get_products


st.title("아이템 조회")
st.caption("선택한 상품 한 건의 상세 정보를 확인합니다.")

if not is_logged_in():
    st.warning("로그인 후 아이템 조회 기능을 이용할 수 있습니다.")
    st.stop()

try:
    products = get_products()
except ProductAPIError as error:
    st.error(str(error))
    st.stop()

if not products:
    st.info("등록된 상품이 없습니다.")
    st.stop()

dataframe = pd.DataFrame(products)
dataframe["created_at"] = pd.to_datetime(dataframe["created_at"], errors="coerce")
dataframe["price"] = pd.to_numeric(dataframe["price"], errors="coerce")

st.markdown("#### 아이템 필터")
with st.form("item_filter_form"):
    keyword = st.text_input("상품명", placeholder="예: 아메리카노")
    date_column1, date_column2 = st.columns(2)
    with date_column1:
        start_date = st.date_input("등록일 시작", value=None)
    with date_column2:
        end_date = st.date_input("등록일 종료", value=None)

    price_column1, price_column2 = st.columns(2)
    with price_column1:
        min_price = st.number_input("최소 가격", min_value=0, value=0, step=100)
    with price_column2:
        max_price = st.number_input("최대 가격", min_value=0, value=10_000_000, step=100)

    st.form_submit_button("필터 적용", type="primary")

if min_price > max_price:
    st.warning("최소 가격은 최대 가격보다 클 수 없습니다.")
    st.stop()

filtered = dataframe.copy()
if keyword:
    filtered = filtered[filtered["name"].str.contains(keyword, case=False, na=False)]
if start_date:
    filtered = filtered[filtered["created_at"].dt.date >= start_date]
if end_date:
    filtered = filtered[filtered["created_at"].dt.date <= end_date]
filtered = filtered[filtered["price"].between(min_price, max_price)]

if filtered.empty:
    st.info("필터 조건에 맞는 상품이 없습니다.")
    st.stop()

st.caption(f"필터 결과: {len(filtered)}건")
filtered_products = filtered.to_dict("records")
options = {
    f"{product['name']} · {int(product['price']):,}원": product
    for product in filtered_products
}
selected_label = st.selectbox("조회할 상품 선택", options)
item = options[selected_label]

column1, column2 = st.columns(2)
with column1:
    st.metric("가격", f"{int(item['price']):,}원")
with column2:
    st.metric("상품 ID", item["id"])

st.markdown("#### 상품 정보")
st.write(f"**상품명:** {item['name']}")
st.write(f"**등록일:** {item.get('created_at', '-')}")
