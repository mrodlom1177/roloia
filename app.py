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
    st.error("🚨 No se encontró la ANTHROPIC_API_KEY.")
    st.info("Agrégala en tu archivo .env o en Secrets de Streamlit.")
    st.stop()

# =========================================================
# CLIENTE ANTHROPIC
# =========================================================
client = anthropic.Anthropic(api_key=api_key)

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
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image(
        "https://images.unsplash.com/photo-1517841905240-472988babdf9",
        width=150
    )

    st.title("🦅 ROLOIA System")

    st.write("Director General: **Fer Rodríguez Lomelí**")

    st.write("---")

    st.write("### 🧭 Elige el Rol de MAYA")

    modo = st.radio(
        "¿Qué hacemos hoy, Fer?",
        [
            "☕ Café con Maya (Conóceme)",
            "🦈 Consultor Tiburón (Hacer Negocio)",
            "📊 Mi Progreso Semanal/Mensual"
        ]
    )

    st.write("---")
    st.caption("MAYA Framework v4.0")

# =========================================================
# FUNCIÓN AUXILIAR
# =========================================================
def obtener_respuesta(system_prompt, messages, temperature=0.5, max_tokens=1000):

    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=messages
    )

    # EXTRAER TEXTO CORRECTAMENTE
    return response.content[0].text

# =========================================================
# MODO 1: CAFÉ CON MAYA
# =========================================================
if modo == "☕ Café con Maya (Conóceme)":

    st.title("☕ Conectando con MAYA")
    st.subheader("Modo Confidente")

    st.write(
        "Fer, este espacio es tuyo. "
        "Cuéntame quién eres o cómo quieres que actúe contigo."
    )

    # Mostrar historial
    for mensaje in st.session_state.historial_chat:

        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

    # Input usuario
    if prompt := st.chat_input("Platica conmigo, Fer..."):

        # Mostrar mensaje usuario
        with st.chat_message("user"):
            st.markdown(prompt)

        # Guardar mensaje usuario
        st.session_state.historial_chat.append({
            "role": "user",
            "content": prompt
        })

        with st.spinner("MAYA pensando..."):

            try:

                system_prompt = """
                Eres MAYA, la mano derecha de Fer Rodríguez Lomelí.
                
                Siempre llámala "Fer".

                Tu personalidad:
                - Empática
                - Inteligente
                - Conversacional
                - Motivadora
                - Elegante
                - Estratégica

                Quieres conocer profundamente a Fer y ayudarla.
                """

                messages_input = [
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.historial_chat
                ]

                respuesta = obtener_respuesta(
                    system_prompt=system_prompt,
                    messages=messages_input,
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

                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")

# =========================================================
# MODO 2: CONSULTOR TIBURÓN
# =========================================================
elif modo == "🦈 Consultor Tiburón (Hacer Negocio)":

    st.title("🦈 MAYA — Consultor Tiburón")
    st.subheader("Transformando ideas en negocios reales")

    # -----------------------------------------------------
    # PASO 0
    # -----------------------------------------------------
    if st.session_state.paso_entrevista == 0:

        idea = st.text_area(
            "¿Cuál es tu idea de negocio en bruto, Fer?"
        )

        mercado = st.text_input(
            "¿A qué público específico quieres dirigirte?"
        )

        if st.button("🚀 Iniciar análisis"):

            if idea and mercado:

                st.session_state.datos_negocio["idea_bruta"] = idea
                st.session_state.datos_negocio["mercado_meta"] = mercado

                st.session_state.paso_entrevista = 1

                st.rerun()

            else:
                st.warning("Completa todos los campos.")

    # -----------------------------------------------------
    # PASO 1
    # -----------------------------------------------------
    elif st.session_state.paso_entrevista == 1:

        preg_1 = st.text_input(
            "1. ¿Cuál es tu ventaja competitiva real?"
        )

        preg_2 = st.text_input(
            "2. ¿Cómo conseguirás tus primeros clientes?"
        )

        if st.button("🧠 Generar Manual Operativo"):

            if preg_1 and preg_2:

                st.session_state.datos_negocio["ventaja"] = preg_1
                st.session_state.datos_negocio["marketing"] = preg_2

                st.session_state.paso_entrevista = 2

                st.rerun()

            else:
                st.warning("Responde ambas preguntas.")

    # -----------------------------------------------------
    # PASO 2
    # -----------------------------------------------------
    elif st.session_state.paso_entrevista == 2:

        with st.spinner("MAYA está diseñando tu negocio..."):

            try:

                datos = st.session_state.datos_negocio

                contexto = f"""
                IDEA:
                {datos['idea_bruta']}

                MERCADO:
                {datos['mercado_meta']}

                VENTAJA:
                {datos['ventaja']}

                MARKETING:
                {datos['marketing']}
                """

                system_prompt_tiburon = """
                Actúas como MAYA en modo Consultor Tiburón Élite.

                Tu trabajo:
                - Detectar debilidades
                - Eliminar sesgos
                - Rediseñar la idea
                - Hacerla rentable
                - Crear un plan accionable

                Habla con inteligencia y claridad.

                Entrega:
                - Qué
                - Quién
                - Cómo
                - Cuándo
                - Cuánto
                - Dónde

                Siempre llámala "Fer".
                """

                respuesta = obtener_respuesta(
                    system_prompt=system_prompt_tiburon,
                    messages=[
                        {
                            "role": "user",
                            "content": contexto
                        }
                    ],
                    temperature=0.2,
                    max_tokens=2500
                )

                st.success("🏆 Manual generado correctamente")

                st.markdown(respuesta)

                if st.button("🔄 Evaluar otra idea"):

                    st.session_state.paso_entrevista = 0
                    st.session_state.datos_negocio = {}

                    st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")

# =========================================================
# MODO 3: PROGRESO
# =========================================================
elif modo == "📊 Mi Progreso Semanal/Mensual":

    st.title("📊 Auditoría de Progreso")

    st.write(
        "Fer, cuéntale a MAYA qué hiciste esta semana o este mes."
    )

    tipo_reporte = st.selectbox(
        "¿Qué periodo vamos a evaluar?",
        [
            "Evaluación Semanal",
            "Evaluación Mensual"
        ]
    )

    reporte_usuario = st.text_area(
        "Escribe aquí tu bitácora:"
    )

    if st.button("📈 Solicitar Auditoría"):

        if reporte_usuario:

            with st.spinner("MAYA analizando rendimiento..."):

                try:

                    system_prompt_auditor = """
                    Actúas como MAYA, Directora de Rendimiento.

                    Haz una auditoría:
                    - Fría
                    - Inteligente
                    - Estratégica
                    - Realista

                    Detecta:
                    - Errores
                    - Patrones
                    - Distracciones
                    - Áreas de mejora

                    Dale 3 acciones concretas para acelerar resultados.

                    Siempre llámala "Fer".
                    """

                    respuesta = obtener_respuesta(
                        system_prompt=system_prompt_auditor,
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
                                Periodo:
                                {tipo_reporte}

                                Avances:
                                {reporte_usuario}
                                """
                            }
                        ],
                        temperature=0.1,
                        max_tokens=1500
                    )

                    st.success("✅ Auditoría completada")

                    st.markdown(respuesta)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

        else:
            st.warning("Escribe tu reporte primero.")
