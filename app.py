import streamlit as st
import anthropic

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("🦅 ROLOIA")

pregunta = st.text_input("Pregunta")

if st.button("Enviar"):

    try:

        response = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=100,
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
