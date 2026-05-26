import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="MAIA", layout="wide")

DATA_FILE = "maia_data.json"

# ----------------------------
# DATA
# ----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "chat": [],
            "negocios": [],
            "reflexion": []
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# ----------------------------
# MAIA CORE LOGIC
# ----------------------------
def maia_response(user_input):
    """
    MAIA siempre:
    1. hace preguntas primero
    2. responde si hay contexto suficiente
    3. incluye reflexión con score
    """

    preguntas = [
        "Fer, ¿cuál es el objetivo exacto de lo que quieres hacer?",
        "Fer, ¿esto es para negocio, escuela o algo personal?"
    ]

    respuesta = ""
    
    # lógica simple: si el mensaje es corto, pedimos más contexto
    if len(user_input.split()) < 6:
        respuesta = "Fer, necesito más contexto para darte una respuesta útil."
    else:
        respuesta = (
            "Análisis MAIA:\n"
            "- CEO: estructura la idea y define objetivo claro\n"
            "- Marketing: revisar cómo se comunica\n"
            "- Finanzas: evaluar si tiene costo o ganancia\n"
            "- Operaciones: definir pasos de ejecución\n"
            "- Ventas: identificar cómo se monetiza o se presenta"
        )

    reflexion = {
        "claridad": 8,
        "utilidad": 7,
        "riesgo_error": "medio",
        "mejora": "Solicitar más contexto antes de analizar"
    }

    return preguntas, respuesta, reflexion

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("MAIA")
page = st.sidebar.selectbox(
    "Secciones",
    ["Chat", "Negocios", "Reflexión", "Documentos"]
)

# ----------------------------
# CHAT
# ----------------------------
if page == "Chat":
    st.title("MAIA - Chat con Fer")

    if "messages" not in st.session_state:
        st.session_state.messages = data["chat"]

    user_input = st.text_input("Fer, escribe tu mensaje")

    if st.button("Enviar"):
        if user_input:

            preguntas, respuesta, reflexion = maia_response(user_input)

            entry = {
                "user": user_input,
                "questions": preguntas,
                "response": respuesta,
                "reflection": reflexion,
                "time": str(datetime.now())
            }

            st.session_state.messages.append(entry)
            data["chat"].append(entry)
            save_data(data)

    st.subheader("Historial")

    for m in st.session_state.messages:
        st.markdown("### Usuario")
        st.write(m["user"])

        st.markdown("### MAIA Preguntas")
        for q in m["questions"]:
            st.write(q)

        st.markdown("### MAIA Respuesta")
        st.write(m["response"])

        st.markdown("### Reflexión MAIA")
        st.write(m["reflection"])

        st.write("---")

# ----------------------------
# NEGOCIOS
# ----------------------------
elif page == "Negocios":
    st.title("Negocios")

    idea = st.text_input("Fer, nueva idea de negocio")
    status = st.selectbox("Estado", ["Idea", "En proceso", "Activo"])

    if st.button("Guardar"):
        if idea:
            data["negocios"].append({
                "idea": idea,
                "status": status,
                "time": str(datetime.now())
            })
            save_data(data)

    if data["negocios"]:
        st.dataframe(pd.DataFrame(data["negocios"]))

# ----------------------------
# REFLEXIÓN
# ----------------------------
elif page == "Reflexion":
    st.title("Reflexión")

    tipo = st.selectbox("Tipo", ["Semanal", "Mensual"])
    texto = st.text_area("Fer, escribe tu reflexión")

    if st.button("Guardar"):
        if texto:
            data["reflexion"].append({
                "tipo": tipo,
                "texto": texto,
                "time": str(datetime.now())
            })
            save_data(data)

    if data["reflexion"]:
        st.dataframe(pd.DataFrame(data["reflexion"]))

# ----------------------------
# DOCUMENTOS
# ----------------------------
elif page == "Documentos":
    st.title("Documentos")

    titulo = st.text_input("Título")
    contenido = st.text_area("Contenido")

    if st.button("Crear documento"):
        if titulo and contenido:
            filename = f"{titulo.replace(' ', '_')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(contenido)

            st.success("Documento creado")
