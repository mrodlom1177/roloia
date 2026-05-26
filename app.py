import streamlit as st
from anthropic import Anthropic

client = Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("Test")

if st.button("Probar"):

    try:

        models = client.models.list()

        st.write(models)

    except Exception as e:

        st.error(str(e))
