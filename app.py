import streamlit as st
from openai import OpenAI

# CONFIGURAR API
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# CONFIGURACIÓN
st.set_page_config(
    page_title="ROLOIA",
    layout="wide"
)

# MEMORIA
if "chat" not in st.session_state:
    st.session_state.chat = []

# TÍTULO
st.title("🦅 ROLOIA / MAIA")
st.subheader("Consultora Estratégica de Fer Rodríguez Lomelí")

# MOSTRAR CHAT
for mensaje in st.session_state.chat:

    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# INPUT
if prompt := st.chat_input("Habla con MAYA..."):

    st.session_state.chat.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("MAYA pensando..."):

        try:

            respuesta = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Eres MAYA, la consultora estratégica de Fer.

                        Personalidad:
                        - Inteligente
                        - Estratégica
                        - Elegante
                        - Directa
                        - Visionaria

                        Tu trabajo:
                        - ayudar a Fer a crear negocios
                        - mejorar ideas
                        - detectar errores
                        - proponer soluciones
                        - estructurar planes

                        Siempre llámala Fer.
                        """
                    },
                    *st.session_state.chat
                ]
            )

            texto = respuesta.choices[0].message.content

            st.session_state.chat.append({
                "role": "assistant",
                "content": texto
            })

            with st.chat_message("assistant"):
                st.markdown(texto)

        except Exception as e:

            st.error(str(e))
