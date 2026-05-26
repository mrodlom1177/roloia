import streamlit as st
import anthropic

api_key = st.secrets["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(
    api_key=api_key
)

st.title("🦅 ROLOIA Test")

pregunta = st.text_input("Escribe algo")

if st.button("Enviar"):

    try:

        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=30,
            messages=[
                {
                    "role": "user",
                    "content": pregunta
                }
            ]
        )

        st.success("FUNCIONA 🎉")

        st.write(response.content[0].text)

    except Exception as e:

        st.error(str(e))
