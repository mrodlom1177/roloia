import streamlit as st
import os
from dotenv import load_dotenv
import anthropic

# =========================================================
# CARGAR VARIABLES DE ENTORNO
# =========================================================
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

# =========================================================
# CONFIGURACIÓN DE STREAMLIT
# =========================================================
st.set_page_config(
    page_title="ROLOIA System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# VALIDAR API KEY
# =========================================================
if not api_key:
    st.error("🚨 No se encontró la variable ANTHROPIC_API_KEY")
    st.info("Agrégala en tu archivo .env")
    st.stop()

# =========================================================
# CLIENTE DE ANTHROPIC
# =========================================================
try:
    client = anthropic.Anthropic(api_key=api_key)

except Exception as e:
    st.error(f"Error inicializando Anthropic: {e}")
    st.stop()

# =========================================================
# MEMORIA INTERNA
# =========================================================
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []

if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0

if "datos_negocio" not in st.session_state:
    st.session_state.datos_negocio = {}

# =========================================================
# FUNCIÓN PARA GENERAR RESPUESTAS
# =========================================================
def obtener_respuesta(
    system_prompt,
    messages,
    temperature=0.5,
    max_tokens=1000
):

    try:

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text

    except Exception as e:
        return f"❌ Error generando respuesta: {e}"

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.title("🦅 ROLOIA System")

    st.image(
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
        width=180
    )

    st.write("Director General: **Fer Rodríguez Lomelí**")

    st.write("---")

    st.subheader("🧭 Selecciona un modo")

    modo = st.radio(
        "¿Qué quieres hacer hoy?",
        [
            "☕ Café con Maya (Conóceme)",
            "🦈 Consultor Tiburón (Negocios)",
            "📊 Mi Progreso Semanal/Mensual"
        ]
    )

    st.write("---")
    st.caption("MAYA Framework v4.0")

# =========================================================
# MODO 1 — CAFÉ CON MAYA
# =========================================================
if modo == "☕ Café con Maya (Conóceme)":

    st.title("☕ Café con MAYA")
    st.subheader("Modo Confidente")

    st.write(
        "Fer, este espacio es tuyo. "
        "Puedes hablar conmigo de lo que quieras."
    )

    # MOSTRAR HISTORIAL
    for mensaje in st.session_state.historial_chat:

        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # INPUT USUARIO
    if prompt := st.chat_input("Escribe algo..."):

        # Mostrar mensaje usuario
        with st.chat_message("user"):
            st.markdown(prompt)

        # Guardar mensaje
        st.session_state.historial_chat.append({
            "role": "user",
            "content": prompt
        })

        with st.spinner("MAYA pensando..."):

            system_prompt = """
            Eres MAYA, la asistente personal de Fer Rodríguez Lomelí.

            PERSONALIDAD:
            - Inteligente
            - Elegante
            - Conversacional
            - Estratégica
            - Empática
            - Motivadora

            Siempre llámala "Fer".

            Habla de forma natural y humana.
            """

            respuesta = obtener_respuesta(
                system_prompt=system_prompt,
                messages=st.session_state.historial_chat,
                temperature=0.6,
                max_tokens=1000
            )

            # Mostrar respuesta
            with st.chat_message("assistant"):
                st.markdown(respuesta)

            # Guardar respuesta
            st.session_state.historial_chat.append({
                "role": "assistant",
                "content": respuesta
            })

# =========================================================
# MODO 2 — CONSULTOR TIBURÓN
# =========================================================
elif modo == "🦈 Consultor Tiburón (Negocios)":

    st.title("🦈 MAYA — Consultor Tiburón")
    st.subheader("Convirtiendo ideas en negocios reales")

    # =====================================================
    # PASO 0
    # =====================================================
    if st.session_state.paso_entrevista == 0:

        idea = st.text_area(
            "¿Cuál es tu idea de negocio?"
        )

        mercado = st.text_input(
            "¿A qué público quieres dirigirte?"
        )

        if st.button("🚀 Iniciar análisis"):

            if idea and mercado:

                st.session_state.datos_negocio["idea"] = idea
                st.session_state.datos_negocio["mercado"] = mercado

                st.session_state.paso_entrevista = 1

                st.rerun()

            else:
                st.warning("Completa todos los campos.")

    # =====================================================
    # PASO 1
    # =====================================================
    elif st.session_state.paso_entrevista == 1:

        ventaja = st.text_input(
            "¿Cuál es tu ventaja competitiva?"
        )

        marketing = st.text_input(
            "¿Cómo conseguirás tus primeros clientes?"
        )

        if st.button("🧠 Generar estrategia"):

            if ventaja and marketing:

                st.session_state.datos_negocio["ventaja"] = ventaja
                st.session_state.datos_negocio["marketing"] = marketing

                st.session_state.paso_entrevista = 2

                st.rerun()

            else:
                st.warning("Responde ambas preguntas.")

    # =====================================================
    # PASO 2
    # =====================================================
    elif st.session_state.paso_entrevista == 2:

        with st.spinner("MAYA diseñando estrategia..."):

            datos = st.session_state.datos_negocio

            contexto = f"""
            IDEA:
            {datos['idea']}

            MERCADO:
            {datos['mercado']}

            VENTAJA:
            {datos['ventaja']}

            MARKETING:
            {datos['marketing']}
            """

            system_prompt = """
            Actúas como MAYA en modo Consultor Tiburón Élite.

            Tu trabajo:
            - Detectar debilidades
            - Eliminar sesgos
            - Rediseñar ideas
            - Crear estrategias reales
            - Hacer modelos rentables

            Entrega:
            - Qué hacer
            - Cómo hacerlo
            - Cuánto costaría
            - Cómo venderlo
            - Riesgos
            - Oportunidades

            Siempre llámala "Fer".
            """

            respuesta = obtener_respuesta(
                system_prompt=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": contexto
                    }
                ],
                temperature=0.2,
                max_tokens=2500
            )

            st.success("🏆 Estrategia generada")

            st.markdown(respuesta)

            if st.button("🔄 Analizar otra idea"):

                st.session_state.paso_entrevista = 0
                st.session_state.datos_negocio = {}

                st.rerun()

# =========================================================
# MODO 3 — PROGRESO
# =========================================================
elif modo == "📊 Mi Progreso Semanal/Mensual":

    st.title("📊 Auditoría de Rendimiento")

    st.write(
        "Fer, escribe tus avances para analizarlos."
    )

    tipo_reporte = st.selectbox(
        "Selecciona un periodo",
        [
            "Evaluación Semanal",
            "Evaluación Mensual"
        ]
    )

    reporte = st.text_area(
        "Escribe tu reporte aquí"
    )

    if st.button("📈 Analizar progreso"):

        if reporte:

            with st.spinner("MAYA analizando..."):

                system_prompt = """
                Actúas como MAYA, Directora de Rendimiento.

                Analiza:
                - Productividad
                - Disciplina
                - Errores
                - Patrones
                - Oportunidades

                Sé estratégica, inteligente y directa.

                Dale 3 acciones concretas para mejorar.

                Siempre llámala "Fer".
                """

                respuesta = obtener_respuesta(
                    system_prompt=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            PERIODO:
                            {tipo_reporte}

                            REPORTE:
                            {reporte}
                            """
                        }
                    ],
                    temperature=0.1,
                    max_tokens=1500
                )

                st.success("✅ Auditoría completada")

                st.markdown(respuesta)

        else:
            st.warning("Escribe un reporte primero.")
