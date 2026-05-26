import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import TavilySearchTool

# Cargar las llaves secretas del archivo .env
load_dotenv()

# Configuración estética de la aplicación corporativa de Fer
st.set_page_config(page_title="ROLOIA System", layout="wide", initial_sidebar_state="expanded")

# --- MEMORIA INTERNA DE LA APLICACIÓN ---
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = []
if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0
if "datos_negocio" not in st.session_state:
    st.session_state.datos_negocio = {}

# --- MENÚ LATERAL DE NAVEGACIÓN ---
with st.sidebar:
    st.image("https://unsplash.com", width=150) # Imagen corporativa elegante
    st.title("🦅 ROLOIA System")
    st.write("Director General: **Fer Rodríguez Lomeli**")
    st.write("---")
    st.write("### 🧭 Elige el Rol de MAYA:")
    # El botón/selector que querías para cambiar de tema
    modo = st.radio(
        "¿Qué hacemos hoy, Fer?",
        ["☕ Café con Maya (Conóceme)", "🦈 Consultor Tiburón (Hacer Negocio)", "📊 Mi Progreso Semanal/Mensual"]
    )
    st.write("---")
    st.caption("MAIA Framework v2.0 - Impulsado por Claude 3.5 Sonnet")

# =========================================================================
# MODO 1: CAFE CON MAYA (CONÓCEME)
# =========================================================================
if modo == "☕ Café con Maya (Conóceme)":
    st.title("☕ Conectando con MAYA")
    st.subheader("Modo Confidente y Alianza Estratégica")
    st.write("Fer, este espacio es 100% tuyo. Cuéntame quién eres, qué sueñas, tus miedos o cómo quieres que actúe contigo. Aquí no te voy a presionar con estructuras, estoy guardando todo en mi memoria para conocerte a fondo.")
    
    # Mostrar el chat interactivo
    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])
            
    if prompt := st.chat_input("Platica conmigo, Fer... ¿De qué quieres hablar hoy?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.historial_chat.append({"role": "user", "content": prompt})
        
        with st.spinner("Maya pensando..."):
            try:
                cerebro = LLM(model="anthropic/claude-3-5-sonnet", temperature=0.5)
                instrucciones_personales = f"""
                Eres MAYA, la asistente ejecutiva y mano derecha de María Fernanda Rodríguez Lomeli (a quien siempre, sin excepción, debes llamar 'Fer').
                Estás en el modo 'Café con Maya'. Tu objetivo aquí es conocerla profundamente: sus valores, sus miedos, sus ideas y su estilo. 
                Sé empática, motivadora, inteligente y muy analítica. No estructures negocios aquí a menos que ella te lo pida. 
                Responde de forma conversacional, clara y mantén en tu memoria todo lo que te cuente sobre quién es ella.
                """
                # Llamar al modelo directamente para una conversación fluida
                conversacion = cerebro.call(messages=[
                    {"role": "system", "content": instrucciones_personales},
                    {"role": "user", "content": prompt}
                ])
                
                with st.chat_message("assistant"):
                    st.markdown(conversacion)
                st.session_state.historial_chat.append({"role": "assistant", "content": conversacion})
            except Exception as e:
                st.error(f"Error de conexión: {e}")

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
                st.error("Fer, por favor completa ambos campos para poder interrogarte con precisión.")

    elif st.session_state.paso_entrevista == 1:
        st.markdown("### 🔍 Preguntas Profundas de Validación")
        st.write("Analizando viabilidad real... Responde con la verdad, Fer:")
        
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
        st.info("⚡ MAYA está activando sus procesos automatizados e investigando la competencia...")
        
        with st.spinner("Fabricando soluciones reales sin sesgos humanos... Por favor espera."):
            try:
                cerebro_premium = LLM(model="anthropic/claude-3-5-sonnet", temperature=0.1)
                herramienta_busqueda = TavilySearchTool()

                tiburon = Agent(
                    role='Consultor Tiburón de Negocios Élite',
                    goal='Destruir sesgos, identificar fallas críticas en la idea y reestructurarla para que sea un éxito económico masivo en México.',
                    backstory='Eres MAYA en modo Tiburón. Un estratega comercial implacable. No suavizas la realidad a Fer, pero le rediseñas la idea tú mismo para que funcione y deje mucho dinero.',
                    tools=[herramienta_busqueda],
                    llm=cerebro_premium
                )

                coo = Agent(
                    role='Director de Operaciones Corporativas (COO)',
                    goal='Convertir la propuesta corregida por el tiburón en un Manual Operativo ultra específico para empleados.',
                    backstory='Especialista en procesos sencillos para que Fer no trabaje en la operación, sino que todo lo ejecuten terceros de forma automática.',
                    llm=cerebro_premium
                )

                contexto_usuario = f"""
                Idea de Fer: {st.session_state.datos_negocio['idea_bruta']}
                Mercado en México: {st.session_state.datos_negocio['mercado_meta']}
                Ventaja percibida: {st.session_state.datos_negocio['ventaja']}
                Estrategia clientes: {st.session_state.datos_negocio['marketing']}
                """

                tarea_analisis = Task(
                    description=f'Analiza con frialdad matemática este negocio para el mercado mexicano actual: {contexto_usuario}. Encuentra fallas de dinero o logística y rediseña la idea para arreglar esos huecos por completo.',
                    expected_output='Informe crudo con errores encontrados y la nueva propuesta completamente resuelta.',
                    agent=tiburon
                )

                tarea_manual = Task(
                    description='Toma la idea resuelta y crea un Manual Operativo detallado por tareas simples. Cada tarea debe responder obligatoriamente de forma explícita: - QUÉ se hace, - QUIÉN lo hace (empleado/herramienta), - CÓMO se hace (paso a paso sencillo), - CUÁNDO se hace, - CUÁNTO cuesta o genera, - DÓNDE se ejecuta. Asegura que Fer no intervenga en la operación diaria.',
                    expected_output='Un Manual de Operación y Delegación impecable con instrucciones ultra específicas.',
                    agent=coo
                )

                corporacion = Crew(
                    agents=[tiburon, coo],
                    tasks=[tarea_analisis, tarea_manual],
                    process=Process.sequential
                )

                resultado = corporacion.kickoff()

                st.success("🏆 ¡Proceso Automatizado Completado con Éxito!")
                st.markdown(resultado.raw)
                
                if st.button("🚀 Evaluar una nueva idea"):
                    st.session_state.paso_entrevista = 0
                    st.rerun()

            except Exception as e:
                st.error(f"Ocurrió un detalle en la conexión: {e}")

# =========================================================================
# MODO 3: MI PROGRESO SEMANAL/MENSUAL
# =========================================================================
elif modo == "📊 Mi Progreso Semanal/Mensual":
    st.title("📊 Control de Progreso y Rendición de Cuentas")
    st.subheader("Evaluación de metas de Fer Rodríguez Lomeli")
    st.write("Fer, para construir un imperio necesitas medir tus avances. Cuéntale a MAYA qué hiciste esta semana o este mes, cuánto dinero entró/salió o qué te detuvo, y ella evaluará críticamente tu velocidad de crecimiento.")
