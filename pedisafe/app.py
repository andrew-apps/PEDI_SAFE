"""
PediSafe - Agente de Triaje Pediátrico
Aplicación Streamlit con RAG para orientación sobre fiebre en niños
Hackathon: Alameda Hacks 2026
Track: Social Good + ML/AI
"""

import streamlit as st
import os
from pathlib import Path

from config import UI_CONFIG, TRIAGE_LEVELS
from rag_engine import PediSafeRAG

# Page configuration
st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["initial_sidebar_state"]
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a5f;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .triage-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .triage-red { background-color: #fee2e2; border-left: 4px solid #dc3545; }
    .triage-orange { background-color: #fff3e0; border-left: 4px solid #fd7e14; }
    .triage-yellow { background-color: #fffde7; border-left: 4px solid #ffc107; }
    .triage-green { background-color: #e8f5e9; border-left: 4px solid #28a745; }
    .disclaimer-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        font-size: 0.85rem;
        color: #666;
    }
    .source-badge {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.25rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def get_api_key() -> str | None:
    """
    Obtiene API key con patrón BYOK (Bring Your Own Key)
    Prioridad: 1) Key del dueño (secrets/env) 2) Key del usuario
    """
    owner_key = None
    
    # 1) Key del dueño desde Streamlit Secrets o env
    try:
        if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets:
            owner_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    if not owner_key:
        owner_key = os.getenv("OPENAI_API_KEY")
    
    # 2) UI: BYOK option
    st.sidebar.markdown("### 🔑 API Key")
    
    has_owner_key = owner_key is not None and len(owner_key) > 10
    
    if has_owner_key:
        st.sidebar.success("✅ Demo key disponible")
        use_own = st.sidebar.toggle("Usar mi propia API Key", value=False)
    else:
        st.sidebar.warning("⚠️ Sin demo key - ingresa tu API Key")
        use_own = True
    
    if use_own:
        user_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Tu key NO se almacena. Solo se usa en esta sesión."
        )
        if user_key and user_key.startswith("sk-"):
            st.session_state["api_key"] = user_key
            return user_key
        elif user_key:
            st.sidebar.error("La API Key debe empezar con 'sk-'")
            return None
        return None
    else:
        st.session_state.pop("user_api_key", None)
        return owner_key


def init_session_state():
    """Inicializa el estado de la sesión"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = None


def render_sidebar():
    """Renderiza la barra lateral con información y controles"""
    st.sidebar.markdown("# 🩺 PediSafe")
    st.sidebar.markdown("*Asistente de Triaje Pediátrico*")
    st.sidebar.divider()
    
    # Triage levels reference
    st.sidebar.markdown("### 📊 Niveles de Triaje")
    for level, info in TRIAGE_LEVELS.items():
        st.sidebar.markdown(f"{info['emoji']} **{level}**: {info['description']}")
    
    st.sidebar.divider()
    
    # Quick guide
    with st.sidebar.expander("📋 Información a proporcionar"):
        st.markdown("""
        - **Edad** del niño (meses o años)
        - **Temperatura** y cómo se tomó
        - **Duración** de la fiebre
        - **Síntomas** adicionales
        - **Condiciones** médicas previas
        """)
    
    st.sidebar.divider()
    
    # Sources
    st.sidebar.markdown("### 📚 Fuentes Médicas")
    st.sidebar.markdown("""
    - [AAP HealthyChildren.org](https://healthychildren.org)
    - [NHS UK](https://nhs.uk)
    """)
    
    # Clear chat button
    st.sidebar.divider()
    if st.sidebar.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def render_header():
    """Renderiza el encabezado principal"""
    st.markdown('<h1 class="main-header">🩺 PediSafe</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Asistente de triaje pediátrico para orientación sobre fiebre</p>',
        unsafe_allow_html=True
    )
    
    # Disclaimer prominente
    st.markdown("""
    <div class="disclaimer-box">
        ⚠️ <strong>IMPORTANTE:</strong> PediSafe es una herramienta INFORMATIVA basada en guías públicas 
        (AAP, NHS). <strong>NO reemplaza</strong> la consulta médica profesional. 
        Ante cualquier duda o emergencia, contacta a tu pediatra o servicios de emergencia.
    </div>
    """, unsafe_allow_html=True)


def render_chat():
    """Renderiza el historial del chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_chat_history() -> str:
    """Obtiene el historial formateado para el contexto"""
    history = []
    for msg in st.session_state.messages[-6:]:  # Últimos 6 mensajes
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        history.append(f"{role}: {msg['content']}")
    return "\n".join(history)


def handle_api_error(error: Exception):
    """Maneja errores de API de forma amigable"""
    error_str = str(error).lower()
    
    if "insufficient_quota" in error_str or "rate_limit" in error_str:
        st.error("""
        😔 **Se agotó el crédito del demo**
        
        Para continuar:
        1. Activa "Usar mi propia API Key" en la barra lateral
        2. Ingresa tu API Key de OpenAI
        
        [Obtén tu API Key aquí](https://platform.openai.com/api-keys)
        """)
    elif "invalid_api_key" in error_str:
        st.error("❌ API Key inválida. Verifica que esté correcta.")
    else:
        st.error(f"❌ Error: {error}")


def main():
    """Función principal de la aplicación"""
    init_session_state()
    
    # Sidebar
    render_sidebar()
    
    # Get API key
    api_key = get_api_key()
    
    # Main content
    render_header()
    
    st.divider()
    
    # Check API key
    if not api_key:
        st.info("👈 Por favor, configura tu API Key en la barra lateral para comenzar.")
        
        # Show example conversation
        with st.expander("💡 Ejemplo de cómo usar PediSafe"):
            st.markdown("""
            **Tú:** Mi bebé de 4 meses tiene 38.5°C de fiebre desde hace 6 horas.
            Está un poco irritable pero come bien.
            
            **PediSafe:** 🟠 **NARANJA - PRIORIDAD ALTA**
            
            Basándome en la información proporcionada:
            - Bebé de 4 meses (3-6 meses de edad)
            - Temperatura de 38.5°C (101.3°F)
            - Duración: 6 horas
            
            **Recomendación:** Contacta a tu pediatra hoy...
            """)
        return
    
    # Initialize RAG engine if needed
    if st.session_state.rag_engine is None:
        with st.spinner("🔄 Cargando base de conocimientos médicos..."):
            try:
                knowledge_path = Path(__file__).parent / "knowledge"
                st.session_state.rag_engine = PediSafeRAG(api_key, str(knowledge_path))
            except Exception as e:
                handle_api_error(e)
                return
    
    # Render chat history
    render_chat()
    
    # Welcome message if no messages
    if not st.session_state.messages:
        st.markdown("""
        ### 👋 ¡Hola! Soy PediSafe
        
        Estoy aquí para ayudarte a evaluar la fiebre de tu hijo/a y orientarte 
        sobre los siguientes pasos.
        
        **Cuéntame:**
        - ¿Cuántos meses o años tiene tu hijo/a?
        - ¿Cuál es la temperatura y cómo la mediste?
        - ¿Hace cuánto tiempo tiene fiebre?
        - ¿Tiene otros síntomas?
        """)
    
    # Chat input
    if prompt := st.chat_input("Describe la situación de tu hijo/a..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                try:
                    chat_history = get_chat_history()
                    response = st.session_state.rag_engine.get_response(
                        prompt, 
                        chat_history
                    )
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response
                    })
                except Exception as e:
                    handle_api_error(e)


if __name__ == "__main__":
    main()
