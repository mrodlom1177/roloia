import streamlit as st
import anthropic

client = anthropic.Client(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("ROLOIA TEST")

pregunta = st.text_input("Pregunta")

if st.button("Enviar"):

    try:

        response = client.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} {pregunta}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-2.1",
            max_tokens_to_sample=100,
        )

        st.success("FUNCIONA 🎉")

        st.write(response["completion"])

    except Exception as e:

        st.error(str(e))
