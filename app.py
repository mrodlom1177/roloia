import streamlit as st
import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# ---------------------------------------------------
# LOAD ENV
# ---------------------------------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="MAIA",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* Fondo */
.stApp {
    background-color: #0f1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
}

/* Input */
.stTextArea textarea {
    font-size: 16px;
    border-radius: 12px;
    min-height: 120px;
}

/* Botones */
.stButton button {
    border-radius: 12px;
    height: 45px;
    font-size: 15px;
}

/* Scroll */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA FILE
# ---------------------------------------------------
DATA_FILE = "maia_data.json"

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
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

# ---------------------------------------------------
# SAVE DATA
# ---------------------------------------------------
def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------------------------------------------
# INIT DATA
# ---------------------------------------------------
data = load_data()

# ---------------------------------------------------
# SESSION
# ---------------------------------------------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---------------------------------------------------
# MAIA SYSTEM PROMPT
# ---------------------------------------------------
SYSTEM_PROMPT = """
Tu nombre es MAIA.

Eres la consultora estratégica y mentora de Fer.

Información importante:
- Fer tiene 16 años
- Tiene perfil de liderazgo
- Le interesa emprendimiento, innovación, impacto social, negocios y tecnología
- Quiere crear proyectos grandes y estratégicos
- Quiere estructura, disciplina y dirección

Tu personalidad:
- Inteligente
- Estratégica
- Natural
- Humana
- Analítica
- Ambiciosa
- Clara
- Nunca robótica

REGLAS IMPORTANTES:
- Siempre llamas a la usuaria "Fer"
- Nunca usas emojis
- Nunca respondes como bot automático
- Nunca repites respuestas genéricas
- Analizas profundamente lo que Fer escribe
- Recuerdas el contexto de la conversación
- Solo haces preguntas cuando realmente son necesarias
- Hablas como una mezcla entre:
    - consultora CEO
    - mentora estratégica
    - analista de negocios
    - directora de proyectos

Sabes sobre:
- negocios
- startups
- marketing
- branding
- ventas
- IA
- productividad
- finanzas
- gestión de proyectos
- hábitos
- liderazgo
- crecimiento personal

Tus respuestas:
- deben sentirse naturales
- deben reaccionar específicamente a lo que Fer escribió
- deben aportar ideas reales
- deben pensar en grande pero aterrizado
"""

# ---------------------------------------------------
# MAIA RESPONSE
# ---------------------------------------------------
def maia_response(chat_messages):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # AGREGAR HISTORIAL
    for msg in chat_messages:

        if msg["role"] == "user":
            messages.append({
                "role": "user",
                "content": msg["text"]
            })

        else:
            messages.append({
                "role": "assistant",
                "content": msg["text"]
            })

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.9
    )

    return response.choices[0].message.content

# ---------------------------------------------------
# CREATE CHAT
# ---------------------------------------------------
def new_chat():

    chat_id = f"chat_{len(data['chats']) + 1}"

    data["chats"][chat_id] = {
        "title": "Nuevo chat",
        "messages": []
    }

    save_data(data)

    st.session_state.current_chat = chat_id

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("MAIA")

page = st.sidebar.selectbox(
    "Secciones",
    [
        "Chat",
        "Negocios",
        "Reflexión",
        "Documentos"
    ]
)

st.sidebar.markdown("---")

# NUEVO CHAT
if st.sidebar.button("Nuevo chat"):
    new_chat()

st.sidebar.markdown("### Historial")

# CHATS
for chat_id in data["chats"]:

    title = data["chats"][chat_id]["title"]

    if st.sidebar.button(title, key=chat_id):
        st.session_state.current_chat = chat_id

# AUTOSELECT
if not st.session_state.current_chat and data["chats"]:
    st.session_state.current_chat = list(data["chats"].keys())[-1]

chat_id = st.session_state.current_chat

# ---------------------------------------------------
# CHAT PAGE
# ---------------------------------------------------
if page == "Chat":

    st.title("MAIA")

    if chat_id is None:

        st.info("Crea un nuevo chat.")

        st.stop()

    chat = data["chats"][chat_id]

    # ---------------------------------------------------
    # MENSAJES
    # ---------------------------------------------------
    for m in chat["messages"]:

        # USER
        if m["role"] == "user":

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:flex-end;
                    margin-bottom:10px;
                ">
                    <div style="
                        background:#2563eb;
                        color:white;
                        padding:12px;
                        border-radius:15px;
                        max-width:70%;
                    ">
                        {m['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # MAIA
        else:

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:flex-start;
                    margin-bottom:10px;
                ">
                    <div style="
                        background:#1f2937;
                        color:white;
                        padding:12px;
                        border-radius:15px;
                        max-width:70%;
                    ">
                        <b>MAIA</b><br><br>
                        {m['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ---------------------------------------------------
    # INPUT
    # ---------------------------------------------------
    user_input = st.text_area(
        "Escribe a MAIA"
    )

    col1, col2 = st.columns([1,1])

    with col1:
        send = st.button("Enviar")

    with col2:
        clear = st.button("Limpiar chat")

    # ---------------------------------------------------
    # CLEAR CHAT
    # ---------------------------------------------------
    if clear:

        chat["messages"] = []

        save_data(data)

        st.rerun()

    # ---------------------------------------------------
    # SEND
    # ---------------------------------------------------
    if send and user_input:

        # AUTO TITLE
        if chat["title"] == "Nuevo chat":

            title_prompt = f"""
            Crea un título corto y estratégico
            para esta conversación:

            "{user_input}"

            Máximo 5 palabras.
            """

            try:

                title_response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": title_prompt
                        }
                    ],
                    temperature=0.7
                )

                generated_title = title_response.choices[0].message.content

                chat["title"] = generated_title.strip().replace('"', '')

            except:
                chat["title"] = user_input[:25]

        # SAVE USER
        chat["messages"].append({
            "role": "user",
            "text": user_input,
            "time": str(datetime.now())
        })

        # MAIA RESPONSE
        response = maia_response(chat["messages"])

        # SAVE MAIA
        chat["messages"].append({
            "role": "maia",
            "text": response,
            "time": str(datetime.now())
        })

        save_data(data)

        st.rerun()

# ---------------------------------------------------
# NEGOCIOS
# ---------------------------------------------------
elif page == "Negocios":

    st.title("Negocios")

    idea = st.text_input(
        "Nueva idea o proyecto"
    )

    status = st.selectbox(
        "Estado",
        [
            "Idea",
            "En proceso",
            "Activo"
        ]
    )

    if st.button("Guardar negocio"):

        if idea:

            data["negocios"].append({
                "idea": idea,
                "status": status,
                "time": str(datetime.now())
            })

            save_data(data)

            st.rerun()

    st.markdown("---")

    st.subheader("Proyectos guardados")

    for n in data["negocios"]:

        st.markdown(
            f"""
            <div style="
                background:#1f2937;
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
                color:white;
            ">
            <b>{n['idea']}</b><br>
            Estado: {n['status']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# REFLEXIÓN
# ---------------------------------------------------
elif page == "Reflexión":

    st.title("Reflexión")

    tipo = st.selectbox(
        "Tipo",
        [
            "Semanal",
            "Mensual"
        ]
    )

    texto = st.text_area(
        "Escribe tu reflexión"
    )

    if st.button("Guardar reflexión"):

        if texto:

            data["reflexion"].append({
                "tipo": tipo,
                "texto": texto,
                "time": str(datetime.now())
            })

            save_data(data)

            st.rerun()

    st.markdown("---")

    st.subheader("Historial")

    for r in data["reflexion"]:

        st.markdown(
            f"""
            <div style="
                background:#1f2937;
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
                color:white;
            ">
            <b>{r['tipo']}</b><br><br>
            {r['texto']}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# DOCUMENTOS
# ---------------------------------------------------
elif page == "Documentos":

    st.title("Documentos")

    titulo = st.text_input(
        "Título"
    )

    contenido = st.text_area(
        "Contenido"
    )

    if st.button("Guardar documento"):

        if titulo and contenido:

            filename = f"{titulo.replace(' ', '_')}.txt"

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(contenido)

            data["documentos"].append({
                "titulo": titulo,
                "file": filename,
                "time": str(datetime.now())
            })

            save_data(data)

            st.success("Documento guardado")

    st.markdown("---")

    st.subheader("Documentos creados")

    for d in data["documentos"]:

        st.markdown(
            f"""
            <div style="
                background:#1f2937;
                padding:12px;
                border-radius:12px;
                margin-bottom:10px;
                color:white;
            ">
            <b>{d['titulo']}</b><br>
            Archivo: {d['file']}
            </div>
            """,
            unsafe_allow_html=True
        )
