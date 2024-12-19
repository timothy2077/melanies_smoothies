import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import requests

# Snowflake 연결 설정
st.title("Melanie's Smoothie Shop")

# Snowflake 연결 정보
connection_params = {
    "account": "your_account",
    "user": "your_user",
    "password": "your_password",
    "role": "your_role",
    "warehouse": "your_warehouse",
    "database": "smoothies",
    "schema": "public"
}

# Snowflake 세션 생성
session = Session.builder.configs(connection_params).create()

# 데이터 프레임 가져오기
my_dataframe = session.table("fruit_options").to_pandas()

st.write("Available Ingredients:")
st.dataframe(my_dataframe, use_container_width=True)

# 이름 입력받기
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# 사용자가 선택할 수 있는 재료 리스트
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['fruit_name'].tolist(),  # 적합한 열 이름 사용
    max_selections=5
)

# 재료 문자열 생성
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("You selected:", ingredients_string)

# SQL 삽입문 생성
time_to_insert = st.button('Submit Order')
if time_to_insert and name_on_order:
    my_insert_stmt = f"""
    INSERT INTO orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}');
    """
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon='✅')
else:
    st.warning("Please enter your name and select ingredients!")

# 외부 API 호출
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.text)













