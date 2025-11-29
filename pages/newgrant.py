import streamlit as st
from SCvalidators.SCvalidator import parse_smeta
from SChandler import saveSC

st.set_page_config(page_title="МойГрант", page_icon="💰")

st.title("МойГрант")
st.write("онлайн-сервис управления грантами")
st.divider()


st.subheader("Создать грант")

grant_name = st.text_input("Название гранта", value="Новый грант")
grant_executor = st.selectbox("Исполнитель", ["Команда 1", "Команда 2", "Команда 3"])
grant_estimate = st.file_uploader("Смета проекта", 
    type=["doc", "docx"], 
    help="Загрузите документ в формате Word"
)

if(st.button("Создать")):
    saveSC(grant_name, parse_smeta(grant_estimate))
    st.success("Грант успешно создан!")