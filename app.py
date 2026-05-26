import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="MAIA", layout="wide")

# ----------------------------
# UI FIX (caja más cómoda)
# ----------------------------
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 120px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DATA_FILE = "maia_data.json"

# ----------------------------
# DATA SAFE LOAD
# ----------------------------
def load_data():
    default = {
        "chats": {},
        "negocios": [],
        "reflexion": [],
        "documentos": []
    }

    if not os.path.exists(DATA_FILE):
        return default

    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except:
            return default

    for key in default:
        if key not in data:
            data[key] = default[key]

    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


data = load_data()

# ----------------------------
# SESSION
# ----------------------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ----------------------------
# MAIA CORE (REAL PERSONALITY)
# ----------------------------
def maia_response(text):

    if len(text.split()) < 6:
        return (
            "Fer, necesito contexto antes de analizar.\n\n"
            "Respóndeme:\n"
            "1. ¿Qué quieres lograr?\n"
            "2. ¿Es negocio, escuela o personal?\n"
            "3. ¿Cuál es el objetivo final?"
        )

    return f"""
MAIA (Modo CEO):

He analizado lo que dijiste:

{text}

---

ESTRATEGIA:
- Definir objetivo claro y medible

MARKETING:
- Cómo se comunica y a quién va dirigido

FINANZAS:
- Costos, recursos o impacto económico

OPERACIONES:
- Pasos concretos de ejecución

VENTAS / RESULTADO:
- Cómo se convierte en resultado real

---

Fer, dime si quieres que lo convierta en un plan de 7 o 30 días.
"""

# ----------------------------
# NEW CHAT
# ----------------------------
def new_chat():
    chat_id = f"chat_{len(data['chats']) + 1}"
    data["chats"][chat_id] = {
        "title": "Nuevo chat",
        "messages": []
    }
    save_data(data)
    st.session_state.current_chat = chat_id

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("MAIA")

page = st.sidebar.selectbox(
    "Secciones",
    ["Chat", "Negocios", "Reflexión", "Documentos"]
)

st.sidebar.markdown("---")

if st.sidebar.button("Nuevo chat"):
    new_chat()

# chats list
for chat_id in data["chats"]:
    title = data["chats"][chat_id]["title"]

    if st.sidebar.button(title, key=chat_id):
        st.session_state.current_chat = chat_id

if not st.session_state.current_chat and data["chats"]:
    st.session_state.current_chat = list(data["chats"].keys())[-1]

chat_id = st.session_state.current_chat

# ----------------------------
# CHAT PAGE
# ----------------------------
if page == "Chat":
    st.title("MAIA - Consultora de Fer")

    if chat_id is None:
        st.info("Crea un nuevo chat para empezar.")
        st.stop()

    chat = data["chats"][chat_id]

    # mensajes tipo WhatsApp
    for m in chat["messages"]:
        if m["role"] == "user":
            st.markdown(
                f"""
                <div style='text-align:right; background:#DCF8C6; padding:10px; border-radius:10px; margin:5px'>
                Fer: {m['text']}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align:left; background:#F1F0F0; padding:10px; border-radius:10px; margin:5px'>
                MAIA: {m['text']}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    user_input = st.text_area("Escribe a MAIA", height=120)

    col1, col2 = st.columns(2)

    with col1:
        send = st.button("Enviar")

    with col2:
        clear = st.button("Limpiar chat")

    if clear:
        chat["messages"] = []
        save_data(data)
        st.rerun()

    if send and user_input:
        if chat["title"] == "Nuevo chat":
            words = user_input.split()
            chat["title"] = " ".join(words[:4])

        chat["messages"].append({
            "role": "user",
            "text": user_input,
            "time": str(datetime.now())
        })

        response = maia_response(user_input)

        chat["messages"].append({
            "role": "maia",
            "text": response,
            "time": str(datetime.now())
        })

        save_data(data)
        st.rerun()

# ----------------------------
# NEGOCIOS
# ----------------------------
elif page == "Negocios":
    st.title("Negocios")

    idea = st.text_input("Fer, nueva idea de negocio")
    status = st.selectbox("Estado", ["Idea", "En proceso", "Activo"])

    if st.button("Guardar negocio"):
        if idea:
            data["negocios"].append({
                "idea": idea,
                "status": status,
                "time": str(datetime.now())
            })
            save_data(data)
            st.rerun()

    st.subheader("Tus negocios")

    for n in data["negocios"]:
        st.write(f"- {n['idea']} | {n['status']}")

# ----------------------------
# REFLEXIÓN
# ----------------------------
elif page == "Reflexion":
    st.title("Reflexión")

    tipo = st.selectbox("Tipo", ["Semanal", "Mensual"])
    texto = st.text_area("Fer, escribe tu reflexión")

    if st.button("Guardar reflexión"):
        if texto:
            data["reflexion"].append({
                "tipo": tipo,
                "texto": texto,
                "time": str(datetime.now())
            })
            save_data(data)
            st.rerun()

    st.subheader("Historial")

    for r in data["reflexion"]:
        st.write(f"[{r['tipo']}] {r['texto']}")

# ----------------------------
# DOCUMENTOS
# ----------------------------
elif page == "Documentos":
    st.title("Documentos")

    titulo = st.text_input("Título del documento")
    contenido = st.text_area("Contenido")

    if st.button("Guardar documento"):
        if titulo and contenido:
            filename = f"{titulo.replace(' ', '_')}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(contenido)

            data["documentos"].append({
                "titulo": titulo,
                "file": filename,
                "time": str(datetime.now())
            })

            save_data(data)
            st.success("Documento guardado")

    st.subheader("Documentos creados")

    for d in data["documentos"]:
        st.write(f"- {d['titulo']} ({d['file']})")
