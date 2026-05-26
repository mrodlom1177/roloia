import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.title("🦅 ROLOIA")

pregunta = st.text_input("Habla con MAYA")

if st.button("Enviar"):

    try:

        respuesta = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres MAYA, una asistente inteligente y motivadora. Siempre llamas a la usuaria Fer."
                },
                {
                    "role": "user",
                    "content": pregunta
                }
            ]
        )

        st.write(respuesta.choices[0].message.content)

    except Exception as e:

        st.error(str(e))
