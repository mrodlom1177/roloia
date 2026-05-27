import streamlit as st
import json
import os
from datetime import datetime

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="MAIA",
    layout="wide"
)

# ---------------------------------------------------
# STYLE
# ---------------------------------------------------
st.markdown("""
<style>

/* Fondo general */
.main {
    background-color: #0E1117;
}

/* Caja de texto */
.stTextArea textarea {
    height: 120px;
    font-size: 16px;
    border-radius: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Botones */
.stButton button {
    border-radius: 10px;
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


data = load_data()

# ---------------------------------------------------
# SESSION
# ---------------------------------------------------
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---------------------------------------------------
# MAIA AI LOGIC
# ---------------------------------------------------
def maia_response(text):

    text_lower = text.lower()

    # ---------------------------------------------------
    # GREETINGS
    # ---------------------------------------------------
    greetings = [
        "hola",
        "hello",
        "hi",
        "buenas",
        "cómo estás",
        "como estas"
    ]

    if any(greet in text_lower for greet in greetings):
        return (
            "Hola Fer.\n\n"
            "Estoy lista para ayudarte con negocios, estrategia, "
            "proyectos, organización, reflexión personal y crecimiento.\n\n"
            "Cuéntame qué tienes en mente."
        )

    # ---------------------------------------------------
    # PRESENTATION / IDENTITY
    # ---------------------------------------------------
    if "soy" in text_lower or "me llamo" in text_lower:

        return (
            "Gracias por compartir eso conmigo, Fer.\n\n"
            "Puedo notar varias fortalezas importantes en ti:\n\n"
            "- liderazgo\n"
            "- pensamiento estratégico\n"
            "- interés en impacto social\n"
            "- iniciativa\n"
            "- visión a futuro\n\n"
            "También noto que tienes ambición y muchas ideas, "
            "pero necesitas estructura, enfoque y sistemas "
            "para convertir ese potencial en resultados sólidos.\n\n"
            "Voy a ayudarte a:\n"
            "- organizar ideas\n"
            "- crear planes\n"
            "- mejorar disciplina\n"
            "- desarrollar proyectos\n"
            "- pensar de forma estratégica\n"
            "- priorizar correctamente"
        )

    # ---------------------------------------------------
    # BUSINESS / PROJECT ANALYSIS
    # ---------------------------------------------------
    keywords = [
        "negocio",
        "empresa",
        "startup",
        "marketing",
        "ventas",
        "finanzas",
        "dinero",
        "proyecto",
        "ia",
        "app",
        "marca"
    ]

    if any(word in text_lower for word in keywords):

        # SI EL CONTEXTO ES MUY POCO
        if len(text.split()) < 10:

            return (
                "Fer, necesito un poco más de contexto "
                "para darte un análisis estratégico útil.\n\n"
                "Explícame:\n"
                "- situación actual\n"
                "- objetivo\n"
                "- qué quieres lograr"
            )

        return (
            "MAIA — Análisis Estratégico\n\n"

            "ESTRATEGIA:\n"
            "- definir objetivo claro\n"
            "- validar oportunidad\n\n"

            "MARKETING:\n"
            "- comunicación\n"
            "- audiencia objetivo\n"
            "- posicionamiento\n\n"

            "FINANZAS:\n"
            "- costos\n"
            "- recursos necesarios\n"
            "- rentabilidad potencial\n\n"

            "OPERACIONES:\n"
            "- pasos de ejecución\n"
            "- estructura\n"
            "- organización\n\n"

            "CRECIMIENTO:\n"
            "- riesgos\n"
            "- oportunidades\n"
            "- escalabilidad\n\n"

            "AUTOEVALUACIÓN MAIA:\n"
            "- claridad: 8/10\n"
            "- profundidad: 7/10\n"
            "- contexto suficiente: parcial\n\n"

            "Fer, puedo convertir esto "
            "en un plan de acción de 7, 30 o 90 días."
        )

    # ---------------------------------------------------
    # GENERAL RESPONSE
    # ---------------------------------------------------
    return (
        "Entiendo, Fer.\n\n"
        "Cuéntame un poco más para ayudarte mejor."
    )

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

# HISTORIAL
for chat_id in data["chats"]:

    title = data["chats"][chat_id]["title"]

    if st.sidebar.button(title, key=chat_id):
        st.session_state.current_chat = chat_id

# AUTO SELECT
if not st.session_state.current_chat and data["chats"]:
    st.session_state.current_chat = list(data["chats"].keys())[-1]

chat_id = st.session_state.current_chat

# ---------------------------------------------------
# CHAT PAGE
# ---------------------------------------------------
if page == "Chat":

    st.title("MAIA")

    if chat_id is None:
        st.info("Crea un nuevo chat para comenzar.")
        st.stop()

    chat = data["chats"][chat_id]

    # ---------------------------------------------------
    # CHAT MESSAGES
    # ---------------------------------------------------
    for m in chat["messages"]:

        # USER
        if m["role"] == "user":

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    background:#2563EB;
                    color:white;
                    padding:12px;
                    border-radius:12px;
                    margin:8px;
                ">
                {m['text']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # MAIA
        else:

            st.markdown(
                f"""
                <div style="
                    text-align:left;
                    background:#1F2937;
                    color:white;
                    padding:12px;
                    border-radius:12px;
                    margin:8px;
                ">
                <b>MAIA</b><br><br>
                {m['text']}
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

    col1, col2 = st.columns(2)

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
    # SEND MESSAGE
    # ---------------------------------------------------
    if send and user_input:

        # TITLE AUTO
        if chat["title"] == "Nuevo chat":

            words = user_input.split()

            chat["title"] = " ".join(words[:4])

        # SAVE USER MESSAGE
        chat["messages"].append({
            "role": "user",
            "text": user_input,
            "time": str(datetime.now())
        })

        # MAIA RESPONSE
        response = maia_response(user_input)

        # SAVE MAIA MESSAGE
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
                background:#1F2937;
                padding:10px;
                border-radius:10px;
                margin:5px;
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
                background:#1F2937;
                padding:10px;
                border-radius:10px;
                margin:5px;
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
                background:#1F2937;
                padding:10px;
                border-radius:10px;
                margin:5px;
                color:white;
            ">
            <b>{d['titulo']}</b><br>
            Archivo: {d['file']}
            </div>
            """,
            unsafe_allow_html=True
        )
