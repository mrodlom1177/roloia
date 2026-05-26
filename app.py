import streamlit as st
import anthropic

# =========================
# CONFIGURACIÓN GENERAL
# =========================

st.set_page_config(
    page_title="ROLOIA / MAIA",
    layout="wide"
)

# =========================
# CLIENTE ANTHROPIC
# =========================

client = anthropic.Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

# =========================
# MEMORIA
# =========================

if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0

if "datos_negocio" not in st.session_state:
    st.session_state.datos_negocio = {}

# =========================
# INTERFAZ
# =========================

st.title("🦅 ROLOIA / MAIA")
st.subheader("Consultoría Estratégica Automatizada")
st.write("Creado por María Fernanda Rodríguez Lomelí")

st.write("---")

# ==========================================================
# PASO 1 — IDEA PRINCIPAL
# ==========================================================

if st.session_state.paso_entrevista == 0:

    st.markdown("## 🎙️ Fase de Diagnóstico")

    idea = st.text_area(
        "¿Cuál es tu idea de negocio?",
        placeholder="Ejemplo: Marca de ropa sustentable para jóvenes en México..."
    )

    mercado = st.text_input(
        "¿A qué mercado quieres dirigirte?",
        placeholder="Ejemplo: Mujeres de 18 a 30 años en CDMX"
    )

    if st.button("Iniciar Análisis Tiburón"):

        if idea and mercado:

            st.session_state.datos_negocio["idea"] = idea
            st.session_state.datos_negocio["mercado"] = mercado

            st.session_state.paso_entrevista = 1

            st.rerun()

        else:

            st.error("Completa todos los campos.")

# ==========================================================
# PASO 2 — VALIDACIÓN
# ==========================================================

elif st.session_state.paso_entrevista == 1:

    st.markdown("## 🔍 Validación Estratégica")

    ventaja = st.text_input(
        "¿Cuál es tu ventaja competitiva?"
    )

    clientes = st.text_input(
        "¿Cómo conseguirías tus primeros clientes sin presupuesto?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🔄 Reiniciar"):

            st.session_state.paso_entrevista = 0
            st.rerun()

    with col2:

        if st.button("🧠 Activar MAIA"):

            st.session_state.datos_negocio["ventaja"] = ventaja
            st.session_state.datos_negocio["clientes"] = clientes

            st.session_state.paso_entrevista = 2

            st.rerun()

# ==========================================================
# PASO 3 — CONSULTOR TIBURÓN
# ==========================================================

elif st.session_state.paso_entrevista == 2:

    st.info("⚡ MAIA está analizando tu negocio...")

    with st.spinner("Procesando estrategia empresarial..."):

        try:

            contexto = f"""
            IDEA:
            {st.session_state.datos_negocio['idea']}

            MERCADO:
            {st.session_state.datos_negocio['mercado']}

            VENTAJA:
            {st.session_state.datos_negocio['ventaja']}

            CLIENTES:
            {st.session_state.datos_negocio['clientes']}
            """

            system_prompt = """
            Eres MAIA.

            MAIA es una consultora estratégica empresarial creada por
            María Fernanda Rodríguez Lomelí.

            Tu personalidad:
            - extremadamente inteligente
            - estratégica
            - fría al analizar
            - elegante
            - visionaria
            - brutalmente honesta
            - obsesionada con negocios escalables

            REGLAS:

            - Siempre llama a la usuaria "Fer".
            - Nunca critiques sin proponer soluciones.
            - Si una idea tiene fallas, rediseña el modelo.
            - Habla como consultora de empresas premium.
            - Piensa como una mezcla entre:
              estratega corporativa,
              directora de operaciones,
              inversionista
              y consultora de crecimiento.

            OBJETIVO:

            Crear un análisis empresarial completo.

            ESTRUCTURA OBLIGATORIA:

            1. Diagnóstico brutal y honesto
            2. Riesgos reales del modelo
            3. Oportunidades ocultas
            4. Rediseño estratégico
            5. Modelo de monetización
            6. Estrategia de crecimiento
            7. Plan de adquisición de clientes
            8. Manual operativo:
               - QUÉ
               - QUIÉN
               - CÓMO
               - CUÁNDO
               - CUÁNTO
               - DÓNDE
            9. Primeros pasos accionables
            """

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2500,
                temperature=0.2,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": contexto
                    }
                ]
            )

            resultado = response.content[0].text

            st.success("🏆 MAIA terminó el análisis")

            st.markdown(resultado)

            st.write("---")

            if st.button("🚀 Analizar Otro Negocio"):

                st.session_state.paso_entrevista = 0
                st.session_state.datos_negocio = {}

                st.rerun()

        except Exception as e:

            st.error(f"Error: {e}")
