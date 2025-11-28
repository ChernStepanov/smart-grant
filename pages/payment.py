import streamlit as st

st.set_page_config(page_title="МойГрант", page_icon="💰")
grant_name = st.query_params["id"]

st.title("МойГрант")
st.write("онлайн-сервис управления грантами")
st.divider()


st.subheader(f"Оплата средствами гранта: {grant_name}")

bill_photo = st.file_uploader("Загрузка чека", 
    type=["jpg"], 
    help="Загрузите фотографию чека с расширением JPG"
)

if(st.button("Оплатить")): st.switch_page("pages/payment.py")