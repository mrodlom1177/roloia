import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.set_page_config(
    page_title="ROLOIA",
    layout="wide"
)

st.title("🦅 ROLOIA / MAIA")

pregunta = st.text_input("Habla con MAYA")

if st.button("Enviar"):

    try:

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": pregunta
                }
            ]
        )

        respuesta = response.content[0].text

        st.success("MAYA respondió 🎉")

        st.write(respuesta)

    except Exception as e:

        st.error(str(e))
