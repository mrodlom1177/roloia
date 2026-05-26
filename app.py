import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("MODELOS DISPONIBLES")

if st.button("Ver modelos"):

    try:

        modelos = client.models.list()

        for modelo in modelos.data:
            st.write(modelo.id)

    except Exception as e:

        st.error(str(e))
