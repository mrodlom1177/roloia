import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import TavilySearchTool

# Cargar las llaves secretas del archivo .env
load_dotenv()

# Configuración estética de la aplicación corporativa de María Fernanda
st.set_page_config(page_title="ROLOIA / MAIA - Business Consultor", layout="wide")

# Inicializar estados de la conversación para que sea interactivo
if "paso_entrevista" not in st.session_state:
    st.session_state.paso_entrevista = 0
    st.session_state.datos_negocio = {}

st.title("🦅 ROLOIA / MAIA // Consultoría de Negocios Automatizada")
st.subheader("Socio Estratégico de María Fernanda Rodríguez Lomeli")
st.write("---")

# --- DISEÑO DEL MÓDULO DE ENTREVISTA INTERACTIVA ---
if st.session_state.paso_entrevista == 0:
    st.markdown("### 🎙️ Fase de Diagnóstico: Cuéntame tu visión inicial")
    idea = st.text_area("¿Cuál es tu idea de negocio en bruto?", placeholder="Ej: Quiero crear una marca de ropa sustentable hecha en México...")
    mercado = st.text_input("¿A qué público específico en México quieres dirigirte?", placeholder="Ej: Jóvenes de 20 a 35 años en Guadalajara y CDMX")
    
    if st.button("Iniciar Análisis Tiburón"):
        if idea and mercado:
            st.session_state.datos_negocio["idea_bruta"] = idea
            st.session_state.datos_negocio["mercado_meta"] = mercado
            st.session_state.paso_entrevista = 1
            st.rerun()
        else:
            st.error("Por favor completa ambos campos para poder interrogarte con precisión.")

elif st.session_state.paso_entrevista == 1:
    st.markdown("### 🔍 Preguntas Profundas de Validación")
    st.write("Analizando la viabilidad inicial... Para no sesgar el modelo, responde estas preguntas críticas:")
    
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
    st.info("⚡ ROLOIA / MAIA está activando sus procesos automatizados. Investigando mercado en México...")
    
    with st.spinner("Fabricando soluciones reales sin sesgos humanos. Por favor espera..."):
        try:
            # Configurar el motor con Claude 3.5 Sonnet
            cerebro_premium = LLM(model="anthropic/claude-3-5-sonnet", temperature=0.1)
            herramienta_busqueda = TavilySearchTool()

            # AGENTE 1: EL CONSULTOR TIBURÓN REESTRUCTURADOR
            tiburon = Agent(
                role='Consultor Tiburón de Negocios Élite',
                goal='Destruir sesgos, identificar fallas críticas en la idea y reestructurarla para que sea un éxito económico masivo en México.',
                backstory='Eres un estratega comercial implacable. No suavizas la realidad. Si una idea es mala, dices por qué de forma fría y analítica, pero la rediseñas tú mismo para que funcione y deje mucho dinero.',
                tools=[herramienta_busqueda],
                llm=cerebro_premium,
                verbose=True
            )

            # AGENTE 2: EL DIRECTOR DE OPERACIONES AUTOMATIZADAS
            coo = Agent(
                role='Director de Operaciones Corporativas (COO)',
                goal='Convertir la propuesta corregida por el tiburón en un Manual Operativo ultra específico para empleados.',
                backstory='Experto en automatización de empresas y creación de manuales de procesos sencillos. Tu obsesión es que el dueño no trabaje en la operación, sino que todo lo ejecuten terceros de forma automática.',
                llm=cerebro_premium,
                verbose=True
            )

            # DEFINICIÓN DE TAREAS EN CADENA
            contexto_usuario = f"""
            Idea: {st.session_state.datos_negocio['idea_bruta']}
            Mercado en México: {st.session_state.datos_negocio['mercado_meta']}
            Ventaja percibida: {st.session_state.datos_negocio['ventaja']}
            Estrategia clientes: {st.session_state.datos_negocio['marketing']}
            """

            tarea_analisis = Task(
                description=f'Analiza con frialdad matemática este negocio de forma realista para el mercado mexicano actual: {contexto_usuario}. Encuentra fallas de dinero o logística y rediseña la idea para arreglar esos huecos por completo.',
                expected_output='Informe crudo con errores encontrados y la nueva propuesta completamente resuelta y optimizada para generar riqueza.',
                agent=tiburon
            )

            tarea_manual = Task(
                description='Toma la idea resuelta y crea un Manual Operativo detallado por tareas simples. Cada tarea debe responder obligatoriamente de forma explícita: - QUÉ se hace, - QUIÊN lo hace (empleado/herramienta), - CÓMO se hace (paso a paso sencillo), - CUÁNDO se hace, - CUÁNTO cuesta o genera, - DÓNDE se ejecuta. Asegura que el dueño no intervenga en la operación diaria.',
                expected_output='Un Manual de Operación y Delegación impecable con instrucciones ultra específicas.',
                agent=coo
            )

            # Lanzar los procesos autónomos
            corporacion = Crew(
                agents=[tiburon, coo],
                tasks=[tarea_analisis, tarea_manual],
                process=Process.sequential
            )

            resultado = corporacion.kickoff()

            # Mostrar el resultado final en pantalla
            st.success("🏆 ¡Proceso Automatizado Completado por ROLOIA / MAIA!")
            st.markdown(resultado.raw)
            
            if st.button("🚀 Crear un nuevo negocio / Reiniciar"):
                st.session_state.paso_entrevista = 0
                st.rerun()

        except Exception as e:
            st.error(f"Ocurrió un detalle en la conexión: {e}")
            if st.button("Intentar de nuevo"):
                st.session_state.paso_entrevista = 0
                st.rerun()
