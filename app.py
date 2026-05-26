import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

st.title("🦅 ROLOIA")

pregunta = st.text_input("Habla con MAYA")

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

if st.button("Enviar"):

    if pregunta:

        with st.spinner("MAYA pensando..."):

            try:

                output = query({
                    "inputs": f"Eres MAYA, una asistente inteligente y motivadora. Responde: {pregunta}"
                })

                respuesta = output[0]["generated_text"]

                st.success("FUNCIONA 🎉")

                st.write(respuesta)

            except Exception as e:

                st.error(str(e))
