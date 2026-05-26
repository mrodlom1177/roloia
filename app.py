import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("MODELOS DISPONIBLES")

if st.button("Ver modelos"):

    try:

        modelos = client.models.list()

        st.write(modelos)

    except Exception as e:

        st.error(str(e))
