import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="ROLOIA", layout="wide")

DATA_FILE = "data.json"

# ----------------------------
# DATA HANDLING
# ----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "chat_general": [],
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
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.title("ROLOIA")
page = st.sidebar.selectbox(
    "Selecciona sección",
    ["Chat", "Negocios", "Reflexión", "Documentos"]
)

# ----------------------------
# CHAT GENERAL
# ----------------------------
if page == "Chat":
    st.title("Chat general")

    if "messages" not in st.session_state:
        st.session_state.messages = data["chat_general"]

    user_input = st.text_input("Escribe aquí")

    if st.button("Enviar"):
        if user_input:
            message = {
                "role": "user",
                "text": user_input,
                "time": str(datetime.now())
            }
            st.session_state.messages.append(message)
            data["chat_general"].append(message)
            save_data(data)

    st.write("Historial")

    for msg in st.session_state.messages:
        st.write(f"{msg['role']}: {msg['text']} ({msg['time']})")

# ----------------------------
# NEGOCIOS
# ----------------------------
elif page == "Negocios":
    st.title("Negocios")

    idea = st.text_input("Nueva idea de negocio")
    status = st.selectbox("Estado", ["Idea", "En proceso", "Activo"])

    if st.button("Guardar negocio"):
        if idea:
            item = {
                "idea": idea,
                "status": status,
                "time": str(datetime.now())
            }
            data["negocios"].append(item)
            save_data(data)

    st.subheader("Tus negocios")

    if data["negocios"]:
        df = pd.DataFrame(data["negocios"])
        st.dataframe(df)

# ----------------------------
# REFLEXIÓN
# ----------------------------
elif page == "Reflexion":
    st.title("Reflexión y progreso")

    tipo = st.selectbox("Tipo de reflexión", ["Semanal", "Mensual"])
    texto = st.text_area("Escribe tu reflexión")

    if st.button("Guardar reflexión"):
        if texto:
            item = {
                "tipo": tipo,
                "texto": texto,
                "time": str(datetime.now())
            }
            data["reflexion"].append(item)
            save_data(data)

    st.subheader("Historial de reflexiones")

    if data["reflexion"]:
        df = pd.DataFrame(data["reflexion"])
        st.dataframe(df)

# ----------------------------
# DOCUMENTOS
# ----------------------------
elif page == "Documentos":
    st.title("Generador de documentos")

    titulo = st.text_input("Título del documento")
    contenido = st.text_area("Contenido")

    if st.button("Guardar documento"):
        if titulo and contenido:
            filename = f"documento_{titulo.replace(' ', '_')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(contenido)

            st.success("Documento guardado")

    st.subheader("Exportación rápida")

    if st.button("Ver archivos guardados"):
        files = [f for f in os.listdir() if f.endswith(".txt")]
        st.write(files)
