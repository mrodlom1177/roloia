import streamlit as st
from openai import OpenAI

st.write("APP INICIANDO...")

try:

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    st.success("OPENAI CONECTADO")

except Exception as e:

    st.error(e)

    st.stop()
