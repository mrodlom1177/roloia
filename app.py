import streamlit as st
import os
from dotenv import load_dotenv
import anthropic

# Cargar las llaves secretas
load_dotenv()
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Configuración de la aplicación
st.set_page_config(page_title="ROLOIA System", layout="wide", initial_sidebar_state="expanded")

# --- MEMORIA INTERNA ---
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []
if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0
if "datos_negocio" not in st.session_state:
    st.session_state.datos_negocio = {}

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://unsplash.com", width=150)
    st.title("🦅 ROLOIA System")
    st.write("Director General: **Fer Rodríguez Lomeli**")
    st.write("---")
    st.write("### 🧭 Elige el Rol de MAYA:")
    modo = st.radio(
        "¿Qué hacemos hoy, Fer?",
        ["☕ Café con Maya (Conóceme)", "🦈 Consultor Tiburón (Hacer Negocio)", "📊 Mi Progreso Semanal/Mensual"]
    )
    st.write("---")
    st.caption("MAIA Framework v4.0")

# Validar llave
if not api_key:
    st.error("🚨 Falta la ANTHROPIC_API_KEY en tus secretos de Streamlit.")
    st.stop()

client = anthropic.Anthropic(api_key=api_key)

# =========================================================================
# MODO 1: CAFE CON MAYA
# =========================================================================
if modo == "☕ Café con Maya (Conóceme)":
    st.title("☕ Conectando con MAYA")
    st.subheader("Modo Confidente")
    st.write("Fer, este espacio es tuyo. Cuéntame quién eres o cómo quieres que actúe contigo.")
    
    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
            
    if prompt := st.chat_input("Platica conmigo, Fer..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.historial_chat.append({"role": "user", "content": prompt})
        
        with st.spinner("Maya pensando..."):
            try:
                system_prompt = "Eres MAYA, la mano derecha de Fer Rodríguez Lomeli (siempre llámala 'Fer'). Sé empática, motivadora, inteligente y conversacional. Conócela a fondo."
                messages_input = [{"role": m["role"], "content": m["content"]} for m in st.session_state.historial_chat]
                
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    temperature=0.5,
                    system=system_prompt,
                    messages=messages_input
                )
                
                with st.chat_message("assistant"):
                    st.markdown(message.content.text)
                st.session_state.historial_chat.append({"role": "assistant", "content": message.content.text})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# =========================================================================
# MODO 2: CONSULTOR TIBURÓN
# =========================================================================
if modo == "🦈 Consultor Tiburón (Hacer Negocio)":
    st.title("🦈 MAYA en Modo: Consultor Tiburón")
    st.subheader("Transformando ideas en riqueza para México")
    
    if st.session_state.paso_entrevista == 0:
        idea = st.text_area("¿Cuál es tu idea de negocio en bruto, Fer?")
        mercado = st.text_input("¿A qué público específico en México quieres dirigirte?")
        if st.button("Iniciar Análisis Tiburón"):
            if idea and mercado:
                st.session_state.datos_negocio["idea_bruta"] = idea
                st.session_state.datos_negocio["mercado_meta"] = mercado
                st.session_state.paso_entrevista = 1
                st.rerun()

    elif st.session_state.paso_entrevista == 1:
        preg_1 = st.text_input("1. ¿Cuál crees que es tu mayor ventaja competitiva real frente a lo que ya existe en México?")
        preg_2 = st.text_input("2. ¿Cómo planeas conseguir a tus primeros clientes si no tienes presupuesto?")
        
        if st.button("🧠 Generar Manual"):
            st.session_state.datos_negocio["ventaja"] = preg_1
            st.session_state.datos_negocio["marketing"] = preg_2
            st.session_state.paso_entrevista = 2
            st.rerun()

    elif st.session_state.paso_entrevista == 2:
        with st.spinner("Fabricando soluciones reales..."):
            try:
                system_prompt_tiburon = "Actúas como MAYA en modo Consultor Tiburón Élite para México. Destruye los sesgos de Fer, dile qué está mal de forma cruda, pero REDISEÑAR la idea tú mismo para que funcione. Entrega un Manual Operativo con: QUÉ, QUIÉN, CÓMO, CUÁNDO, CUÁNTO y DÓNDE. Siempre llámala 'Fer'."
                contexto = f"Idea de Fer: {st.session_state.datos_negocio['idea_bruta']}. Mercado: {st.session_state.datos_negocio['mercado_meta']}. Ventaja: {st.session_state.datos_negocio['ventaja']}. Marketing: {st.session_state.datos_negocio['marketing']}."
                
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2500,
                    temperature=0.2,
                    system=system_prompt_tiburon,
                    messages=[{"role": "user", "content": contexto}]
                )
                st.success("🏆 ¡Manual de Operaciones Completado!")
                st.markdown(message.content.text)
                if st.button("🚀 Evaluar una nueva idea"):
                    st.session_state.paso_entrevista = 0
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# =========================================================================
# MODO 3: MI PROGRESO SEMANAL/MENSUAL
# =========================================================================
if modo == "📊 Mi Progreso Semanal/Mensual":
    st.title("📊 Control de Progreso")
    st.write("Fer, cuéntale a MAYA qué hiciste esta semana o este mes.")
    
    tipo_reporte = st.selectbox("¿Qué periodo vamos a evaluar hoy, Fer?", ["Evaluación Semanal", "Evaluación Mensual"])
    reporte_usuario = st.text_area("Escribe aquí tu bitácora de avances:")
    
    if st.button("Solicitar Auditoría"):
        if reporte_usuario:
            with st.spinner("Maya analizando..."):
                try:
                    system_prompt_auditor = "Actúas como MAYA, Directora de Rendimiento. Haz una auditoría profunda, fría y realista. Dile qué 3 acciones específicas debe ejecutar para acelerar. Siempre llámala 'Fer'."
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1500,
                        temperature=0.1,
                        system=system_prompt_auditor,
                        messages=[{"role": "user", "content": f"Periodo: {tipo_reporte}. Avances: {reporte_usuario}"}]
                    )
                    st.success("📈 ¡Auditoría Completada!")
                    st.markdown(message.content.text)
                except Exception as e:
                    st.error(f"Error: {e}")
