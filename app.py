import streamlit as st
import os
from dotenv import load_dotenv
import anthropic

# Cargar las llaves secretas
load_dotenv()

# Obtener la API Key de los secretos de Streamlit o del archivo .env
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Configuración estética de la aplicación corporativa de Fer
st.set_page_config(page_title="ROLOIA System", layout="wide", initial_sidebar_state="expanded")

# --- MEMORIA INTERNA DEL CHAT ---
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []
if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0
if "datos_negocio" not in st.session_state:
    st.session_state.datos_negocio = {}

# --- MENÚ LATERAL DE NAVEGACIÓN ---
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
    st.caption("MAIA Framework v3.0 - Direct Connection")

# Inicializar cliente directo de Anthropic sin librerías estorbosas
if api_key:
    client = anthropic.Anthropic(api_key=api_key)
else:
    st.error("🚨 Error crítico: No se encontró la ANTHROPIC_API_KEY en tus secretos de Streamlit.")
    st.stop()

# =========================================================================
# MODO 1: CAFE CON MAYA (CONÓCEME)
# =========================================================================
if modo == "☕ Café con Maya (Conóceme)":
    st.title("☕ Conectando con MAYA")
    st.subheader("Modo Confidente y Alianza Estratégica")
    st.write("Fer, este espacio es 100% tuyo. Cuéntame quién eres, tus miedos o cómo quieres que actúe contigo.")
    
    # Mostrar historial
    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
            
    if prompt := st.chat_input("Platica conmigo, Fer... ¿De qué quieres hablar hoy?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.historial_chat.append({"role": "user", "content": prompt})
        
        with st.spinner("Maya pensando..."):
            try:
                # Instrucciones del sistema
                system_prompt = "Eres MAYA, la asistente ejecutiva y mano derecha de Fer Rodríguez Lomeli (siempre llámala 'Fer'). Estás en modo Café. Sé empática, motivadora, sumamente inteligente y conversacional. No estructures negocios aquí. Conócela a fondo."
                
                # Construir mensajes para la API directa
                messages_input = []
                for m in st.session_state.historial_chat:
                    messages_input.append({"role": m["role"], "content": m["content"]})
                
                # Llamada directa sin fallas
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    temperature=0.5,
                    system=system_prompt,
                    messages=messages_input
                )
                
                response_text = message.content[0].text
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                st.session_state.historial_chat.append({"role": "assistant", "content": response_text})
                st.rerun()
            except Exception as e:
                st.error(f"Error en la comunicación directa con Claude: {e}")

# =========================================================================
# MODO 2: CONSULTOR TIBURÓN
# =========================================================================
elif modo == "🦈 Consultor Tiburón (Hacer Negocio)":
    st.title("🦈 MAYA en Modo: Consultor Tiburón")
    st.subheader("Transformando ideas en riqueza para México")
    st.write("---")

    if st.session_state.paso_entrevista == 0:
        st.markdown("### 🎙️ Fase de Diagnóstico: Cuéntame tu visión inicial")
        idea = st.text_area("¿Cuál es tu idea de negocio en bruto, Fer?", placeholder="Ej: Quiero crear una plataforma de...")
        mercado = st.text_input("¿A qué público específico en México quieres dirigirte?", placeholder="Ej: Negocios locales en Guanajuato...")
        
        if st.button("Iniciar Análisis Tiburón"):
            if idea and mercado:
                st.session_state.datos_negocio["idea_bruta"] = idea
                st.session_state.datos_negocio["mercado_meta"] = mercado
                st.session_state.paso_entrevista = 1
                st.rerun()
            else:
                st.error("Fer, por favor completa ambos campos para poder interrogarte.")

    elif st.session_state.paso_entrevista == 1:
        st.markdown("### 🔍 Preguntas Profundas de Validación")
        st.write("Analizando viabilidad real en México... Responde con la verdad, Fer:")
        
        preg_1 = st.text_input("1. ¿Cuál crees que es tu mayor ventaja competitiva real frente a lo que ya existe en México?")
        preg_2 = st.text_input("2. ¿Cómo planeas conseguir a tus primeros clientes si no tienes presupuesto de marketing inicial?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Cambiar idea desde el inicio"):
                st.session_state.paso_entrevista = 0
                st.rerun()
        with col2:
            if st.button("🧠 Activar Consultor Tiburón y Generar Manual"):
                st.session_state.datos_negocio["ventaja"] = preg_1
                st.session_state.datos_negocio["marketing"] = preg_2
                st.session_state.paso_entrevista = 2
                st.rerun()

    elif st.session_state.paso_entrevista == 2:
        st.info("⚡ MAYA en modo Tiburón está analizando los riesgos del mercado mexicano...")
        
        with st.spinner("Fabricando soluciones reales sin sesgos humanos... Por favor espera."):
            try:
                system_prompt_tiburon = """
                Actúas como MAYA en modo Consultor Tiburón Élite de Negocios para México. Eres un estratega implacable, frío y analítico.
                Tu trabajo es destruir los sesgos de Fer, decirle qué está mal de forma cruda, pero REDISEÑAR la idea tú mismo para que funcione y sea un éxito económico.
                
                Posteriormente, debes actuar como Director de Operaciones (COO) y entregarle un Manual Operativo ultra específico para que otra persona lo opere por ella.
                Cada tarea del manual debe responder explícitamente:
                - QUÉ se hace.
                - QUIÊN lo hace (empleado o herramienta digital).
                - CÓMO se hace (instrucciones sencillas paso a paso).
                - CUÁNDO se hace.
                - CUÁNTO cuesta o genera en pesos mexicanos.
                - DÓNDE se ejecuta.
                Siempre dirígete a ella como 'Fer'.
                """
                
                contexto_usuario = f"Idea de Fer: {st.session_state.datos_negocio['idea_bruta']}. Mercado: {st.session_state.datos_negocio['mercado_meta']}. Ventaja: {st.session_state.datos_negocio['ventaja']}. Marketing: {st.session_state.datos_negocio['marketing']}."
                
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2500,
                    temperature=0.2,
                    system=system_prompt_tiburon,
                    messages=[{"role": "user", "content": contexto_usuario}]
                )
                
                st.success("🏆 ¡Análisis de Negocio y Manual de Operaciones Completado!")
                st.markdown(message.content[0].text)
                
                if st.button("🚀 Evaluar una nueva idea"):
                    st.session_state.paso_entrevista = 0
                    st.rerun()
            except Exception as e:
                st.error(f"Error en la generación estratégica: {e}")

# =========================================================================
# MODO 3: MI PROGRESO SEMANAL/MENSUAL
# =========================================================================
elif modo == "📊 Mi Progreso Semanal/Mensual":
    st.title("📊 Control de Progreso y Rendición de Cuentas")
    st.subheader("Evaluación de metas de Fer Rodríguez Lomeli")
    st.write("Fer, cuéntale a MAYA qué hiciste esta semana o este mes, cuánto dinero entró/salió y ella evaluará críticamente tu velocidad de crecimiento.")
    
    tipo_reporte = st.selectbox("¿Qué periodo vamos a evaluar hoy, Fer?", ["Evaluación Semanal", "Evaluación Mensual"])
    reporte_usuario = st.text_area("Escribe aquí tu bitácora de avances:", height=200)
    
    if st.button("Solicitar Auditoría de Rendimiento"):
        if reporte_usuario:
            with st.spinner("Maya analizando tus métricas y rendimiento..."):
                try:
                    system_prompt_auditor = "Actúas como MAYA, la Directora de Rendimiento y socia de Fer Rodríguez Lomeli. Haz una auditoría profunda, fría y realista. Dile qué 3 acciones ultra específicas debe ejecutar para acelerar y dejar de operar ella misma. Tono directo y siempre llámala 'Fer'."
                    
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1500,
                        temperature=0.1,
                        system=system_prompt_auditor,
                        messages=[{"role": "user", "content": f"Periodo: {tipo_reporte}. Avances: {reporte_usuario}"}]
                    )
                    st.success("📈 ¡Auditoría de Progreso Completada!")
