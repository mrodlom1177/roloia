import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="MAIA", layout="wide")

DATA_FILE = "maia_chats.json"

# ----------------------------
# DATA
# ----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"chats": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

data = load_data()

# ----------------------------
# INIT
# ----------------------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ----------------------------
# CREATE CHAT
# ----------------------------
def new_chat():
    chat_id = f"chat_{len(data['chats'])+1}"
    data["chats"][chat_id] = {
        "title": "Nuevo chat",
        "messages": []
    }
    save_data(data)
    st.session_state.current_chat = chat_id

# ----------------------------
# MAIA CORE (básico ahora)
# ----------------------------
def maia_answer(text):
    return (
        "Fer, antes de darte una respuesta necesito claridad:\n"
        "1. ¿Cuál es el objetivo?\n"
        "2. ¿Esto es negocio, escuela o personal?\n\n"
        "Cuando me respondas te doy análisis completo como CEO."
    )

# ----------------------------
# SIDEBAR (HISTORIAL)
# ----------------------------
st.sidebar.title("MAIA")

if st.sidebar.button("Nuevo chat"):
    new_chat()

chat_keys = list(data["chats"].keys())

for c in chat_keys:
    title = data["chats"][c]["title"]
    if st.sidebar.button(title):
        st.session_state.current_chat = c

# si no hay chat seleccionado
if not st.session_state.current_chat and chat_keys:
    st.session_state.current_chat = chat_keys[-1]

chat_id = st.session_state.current_chat

# ----------------------------
# MAIN UI
# ----------------------------
st.title("MAIA")

if chat_id:
    chat = data["chats"][chat_id]

    # ----------------------------
    # CHAT VISUAL STYLE (tipo WhatsApp)
    # ----------------------------
    for m in chat["messages"]:
        if m["role"] == "user":
            st.markdown(
                f"""
                <div style='text-align:right; background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px'>
                Fer: {m['text']}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align:left; background-color:#F1F0F0; padding:10px; border-radius:10px; margin:5px'>
                MAIA: {m['text']}
                </div>
                """,
                unsafe_allow_html=True
            )

# ----------------------------
# INPUT GRANDE (tipo WhatsApp)
# ----------------------------
st.markdown("---")
user_input = st.text_area("Escribe a MAIA", height=120)

col1, col2 = st.columns([1,1])

with col1:
    send = st.button("Enviar")

with col2:
    clear = st.button("Limpiar chat")

if clear and chat_id:
    data["chats"][chat_id]["messages"] = []
    save_data(data)
    st.rerun()

if send and user_input and chat_id:
    chat = data["chats"][chat_id]

    # mensaje usuario
    chat["messages"].append({
        "role": "user",
        "text": user_input,
        "time": str(datetime.now())
    })

    # respuesta MAIA
    response = maia_answer(user_input)

    chat["messages"].append({
        "role": "maia",
        "text": response,
        "time": str(datetime.now())
    })

    # título automático si es primer mensaje
    if chat["title"] == "Nuevo chat":
        chat["title"] = user_input[:25]

    save_data(data)
    st.rerun()
