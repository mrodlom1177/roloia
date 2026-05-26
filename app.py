import streamlit as st
import anthropic

api_key = st.secrets["ANTHROPIC_API_KEY"]

st.write("API cargada:", bool(api_key))

client = anthropic.Anthropic(api_key=api_key)

try:

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=50,
        messages=[
            {
                "role": "user",
                "content": "Hola"
            }
        ]
    )

    st.success("FUNCIONA")
    st.write(response.content[0].text)

except Exception as e:
    st.error(e)
