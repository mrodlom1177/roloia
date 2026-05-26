import streamlit as st
import anthropic

# =====================================================
# API KEY
# =====================================================
api_key = st.secrets["ANTHROPIC_API_KEY"]

st.write("API cargada:", bool(api_key))

# =====================================================
# CLIENTE
# =====================================================
client = anthropic.Anthropic(
    api_key=api_key
)

# =====================================================
# APP
# =====================================================
st.title("🦅 ROLOIA Test")

pregunta = st.text_input("Escribe algo")

if st.button("Enviar"):

    if pregunta:

        with st.spinner("MAYA pensando..."):

            try:

                response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=30,
                    temperature=0,
                    messages=[
                        {
                            "role": "user",
                            "content": pregunta
                        }
                    ],
                    timeout=20
                )

                texto = response.content[0].text

                st.success("FUNCIONA 🎉")

                st.write(texto)

            except Exception as e:

                st.error(str(e))
