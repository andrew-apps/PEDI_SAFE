"""
PediSafe - Pediatric Fever Triage Agent
Streamlit Application with RAG for fever guidance in children
Hackathon: Alameda Hacks 2026
Track: Social Good + ML/AI

Bilingual: English (Primary) / Spanish (Secondary)
"""

import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path

from config import get_ui_config, get_triage_levels, TRIAGE_RULES
from rag_engine import PediSafeRAG
from i18n import get_text

def init_session_state():
    """Initialize session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = None
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "saved_owner_key" not in st.session_state:
        st.session_state.saved_owner_key = None
    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = "cerebras"  # Default to FREE Cerebras
    if "cerebras_key" not in st.session_state:
        st.session_state.cerebras_key = None
    if "legend_minimized" not in st.session_state:
        st.session_state.legend_minimized = True

def get_api_key(lang: str) -> tuple[str | None, str]:
    """
    Get API key with BYOK (Bring Your Own Key) pattern
    Returns: (api_key, provider) where provider is 'openai' or 'cerebras'
    API keys are loaded ONLY from secrets.toml or environment variables - NEVER hardcoded
    """
    # Provider selector with modern styling
    provider_options = {
        "🚀 Cerebras (Llama 3.3 70B) - FREE": "cerebras",
        "💎 OpenAI (GPT-4o-mini)": "openai"
    }
    
    selected_provider = st.sidebar.selectbox(
        "🤖 AI Provider",
        options=list(provider_options.keys()),
        index=0 if st.session_state.llm_provider == "cerebras" else 1,
        key="provider_selector",
        help="Cerebras is FREE and ultra-fast!"
    )
    provider = provider_options[selected_provider]
    st.session_state.llm_provider = provider
    
    # For Cerebras
    if provider == "cerebras":
        # Check for key in secrets/env
        cerebras_key = None
        try:
            if hasattr(st, 'secrets') and 'CEREBRAS_API_KEY' in st.secrets:
                cerebras_key = st.secrets['CEREBRAS_API_KEY']
        except:
            pass
        if not cerebras_key:
            cerebras_key = os.getenv('CEREBRAS_API_KEY')
        
        if cerebras_key and len(cerebras_key) > 10:
            st.sidebar.success("✅ Cerebras API key configured")
            return cerebras_key, "cerebras"
        
        # No key found - ask user to input
        st.sidebar.info("🆓 Cerebras is FREE! Get your key at [cloud.cerebras.ai](https://cloud.cerebras.ai)")
        user_key = st.sidebar.text_input(
            "Cerebras API Key",
            type="password",
            placeholder="csk-...",
            help="Format: csk-xxxxxxxx",
            key="cerebras_api_key_input"
        )
        if user_key and len(user_key) > 10:
            st.session_state.cerebras_key = user_key
            return user_key, "cerebras"
        return None, "cerebras"
    
    else:  # OpenAI
        # Check for key in secrets/env
        owner_key = None
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                owner_key = st.secrets['OPENAI_API_KEY']
        except:
            pass
        if not owner_key:
            owner_key = os.getenv('OPENAI_API_KEY')
        
        if owner_key and len(owner_key) > 10:
            st.sidebar.success("✅ OpenAI API key configured")
            return owner_key, "openai"
        
        st.sidebar.warning("⚠️ OpenAI requires an API key")
        user_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Get your key from platform.openai.com",
            key="openai_api_key_input"
        )
        if user_key and user_key.startswith("sk-"):
            st.session_state.api_key = user_key
            return user_key, "openai"
        return None, "openai"

def render_sidebar(lang: str):
    """Render sidebar with information and controls - Modern Design"""
    # Logo and title
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🩺</div>
        <h1 style="font-size: 1.5rem; margin: 0; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PediSafe</h1>
        <p style="color: #64748b; font-size: 0.85rem; margin: 0.25rem 0 0 0;">AI Pediatric Triage</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    # Triage Legend - Always visible, interactive
    render_triage_legend_sidebar(lang)
    
    st.sidebar.divider()
    
    # Quick Tips
    tips_title = "💡 Tips for Best Results" if lang == "en" else "💡 Consejos"
    with st.sidebar.expander(tips_title, expanded=False):
        if lang == "en":
            st.markdown("""
            **Include in your message:**
            - 👶 Child's age (months/years)
            - 🌡️ Temperature reading
            - ⏱️ How long they've had fever
            - 📋 Other symptoms
            - 💊 Any medications given
            """)
        else:
            st.markdown("""
            **Incluye en tu mensaje:**
            - 👶 Edad del niño (meses/años)
            - 🌡️ Temperatura medida
            - ⏱️ Duración de la fiebre
            - 📋 Otros síntomas
            - 💊 Medicamentos dados
            """)
    
    # Medical Sources - ONLY official validated sources
    sources_title = "📚 Medical Sources" if lang == "en" else "📚 Fuentes Médicas"
    note_text = "All medical advice is grounded in these 5 validated clinical guidelines." if lang == "en" else "Todos los consejos médicos se basan en estas 5 directrices clínicas validadas."
    
    with st.sidebar.expander(sources_title, expanded=False):
        st.markdown(f"""
        <div style="font-size: 0.85rem; line-height: 1.6;">
            <div style="margin-bottom: 0.75rem;">
                <strong>🏥 American Academy of Pediatrics (AAP)</strong><br>
                <a href="https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-and-Your-Baby.aspx" target="_blank" style="color: #6366f1; text-decoration: none;">
                    • Fever and Your Baby
                </a><br>
                <a href="https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/Fever-Without-Fear.aspx" target="_blank" style="color: #6366f1; text-decoration: none;">
                    • Fever Without Fear
                </a><br>
                <a href="https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/When-to-Call-the-Pediatrician.aspx" target="_blank" style="color: #6366f1; text-decoration: none;">
                    • When to Call the Pediatrician
                </a><br>
                <a href="https://www.healthychildren.org/English/tips-tools/symptom-checker/Pages/symptomviewer.aspx?symptom=Fever+(0-12+Months)" target="_blank" style="color: #6366f1; text-decoration: none;">
                    • Symptom Checker: Fever
                </a>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <strong>🏥 NHS UK</strong><br>
                <a href="https://www.nhs.uk/conditions/fever-in-children/" target="_blank" style="color: #6366f1; text-decoration: none;">
                    • High Temperature (Fever) in Children
                </a>
            </div>
            <div style="background: #fef3c7; padding: 0.5rem; border-radius: 6px; border-left: 3px solid #f59e0b; margin-top: 0.75rem;">
                <small><strong>ℹ️ Note:</strong> {note_text}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    # Clear chat button
    clear_text = "Clear Conversation" if lang == "en" else "Limpiar Chat"
    if st.sidebar.button(f"🗑️ {clear_text}", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

def render_language_selector_sidebar(lang: str):
    """Render language selector in sidebar - clean and simple"""
    lang_options = {
        "🇺🇸 English": "en",
        "🇪🇸 Español": "es"
    }
    
    selected_lang = st.sidebar.selectbox(
        "🌐 Language / Idioma",
        options=list(lang_options.keys()),
        index=0 if lang == "en" else 1,
        key="language_selector"
    )
    
    new_lang = lang_options[selected_lang]
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.session_state.rag_engine = None
        st.rerun()

def render_triage_legend_sidebar(lang: str):
    """Render triage legend in sidebar - Always visible with modern design"""
    triage_levels = get_triage_levels(lang)
    legend_title = "🚦 Triage Levels" if lang == "en" else "🚦 Niveles de Triaje"
    
    # Always visible triage legend with modern cards
    st.sidebar.markdown(f"**{legend_title}**")
    
    # Triage level cards
    triage_data = [
        ("🔴", "RED", "#dc2626", "#fee2e2", "Emergency" if lang == "en" else "Emergencia"),
        ("🟠", "ORANGE", "#ea580c", "#ffedd5", "Urgent" if lang == "en" else "Urgente"),
        ("🟡", "YELLOW", "#ca8a04", "#fef9c3", "Monitor" if lang == "en" else "Monitorear"),
        ("🟢", "GREEN", "#059669", "#d1fae5", "Home Care" if lang == "en" else "Cuidado en Casa"),
    ]
    
    for emoji, level, color, bg_color, desc in triage_data:
        st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 0.75rem; 
                    background: {bg_color}; border-radius: 10px; margin: 0.4rem 0; 
                    border-left: 4px solid {color}; transition: transform 0.2s;">
            <span style="font-size: 1.1rem;">{emoji}</span>
            <div style="flex: 1;">
                <span style="font-weight: 700; color: {color}; font-size: 0.85rem;">{level}</span>
                <span style="color: #64748b; font-size: 0.75rem; margin-left: 0.5rem;">{desc}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_header(lang: str):
    """Render main header"""
    st.markdown(f'<h1 class="main-header">{get_text("main_title", lang)}</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sub-header">{get_text("subtitle", lang)}</p>',
        unsafe_allow_html=True
    )
    
    # Use st.warning for proper Markdown rendering
    st.warning(get_text("disclaimer", lang))

def render_chat():
    """Render chat history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_chat_history() -> str:
    """Get formatted chat history for context"""
    history = []
    for msg in st.session_state.messages[-6:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history.append(f"{role}: {msg['content']}")
    return "\n".join(history)

def handle_api_error(error: Exception, lang: str):
    """Handle API errors in a user-friendly way"""
    error_str = str(error).lower()
    
    if "insufficient_quota" in error_str or "rate_limit" in error_str:
        st.error(get_text("quota_error", lang))
    elif "invalid_api_key" in error_str:
        st.error(get_text("invalid_key_error", lang))
    else:
        st.error(get_text("generic_error", lang).format(error=error))

def main():
    """Main application function"""
    init_session_state()
    lang = st.session_state.language
    
    # Page configuration
    ui_config = get_ui_config(lang)
    st.set_page_config(
        page_title=ui_config["page_title"],
        page_icon=ui_config["page_icon"],
        layout=ui_config["layout"],
        initial_sidebar_state=ui_config["initial_sidebar_state"]
    )
    
    # Custom CSS for modern, beautiful UI
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Modern color scheme */
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --secondary-color: #8b5cf6;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --text-dark: #1e293b;
            --text-light: #64748b;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main container */
        .main .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-bottom: 140px;
        }
        
        /* Stunning header */
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
            line-height: 1.1;
            animation: fadeInDown 0.8s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .sub-header {
            font-size: 1.35rem;
            color: #64748b;
            text-align: center;
            margin-bottom: 2.5rem;
            font-weight: 500;
            animation: fadeIn 1s ease-out 0.2s both;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Beautiful disclaimer box */
        .disclaimer-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 1.5rem 2rem;
            border-radius: 16px;
            border-left: 5px solid #f59e0b;
            font-size: 0.95rem;
            color: #78350f;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.15);
            margin-bottom: 2.5rem;
            animation: fadeIn 1s ease-out 0.4s both;
        }
        
        .triage-card {
            padding: 1.5rem;
            border-radius: 16px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        
        .triage-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }
        
        .triage-red { 
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 6px solid #dc2626;
        }
        
        .triage-orange { 
            background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%);
            border-left: 6px solid #ea580c;
        }
        
        .triage-yellow { 
            background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
            border-left: 6px solid #ca8a04;
        }
        
        .triage-green { 
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 6px solid #059669;
        }
        
        .source-badge {
            display: inline-block;
            background-color: #e0e7ff;
            color: #3730a3;
            padding: 0.35rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            margin: 0.25rem;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .source-badge:hover {
            background-color: #c7d2fe;
            transform: scale(1.05);
        }
        
        /* Enhanced chat messages */
        .stChatMessage {
            border-radius: 20px;
            padding: 1.25rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            animation: fadeIn 0.4s ease-out;
        }
        
        /* User messages */
        [data-testid="stChatMessageContent"] {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* Improved sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
            border-right: 1px solid #e2e8f0;
        }
        
        section[data-testid="stSidebar"] .stMarkdown {
            color: #334155;
        }
        
        /* Sidebar más compacto */
        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        section[data-testid="stSidebar"] .element-container {
            margin-bottom: 0.5rem;
        }
        
        section[data-testid="stSidebar"] h1 {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        section[data-testid="stSidebar"] h2 {
            font-size: 1.1rem;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
        
        /* Beautiful buttons */
        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Stunning welcome card */
        .welcome-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 3rem 2.5rem;
            border-radius: 24px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            margin: 2rem 0;
            color: white;
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .welcome-card h3 {
            color: white;
            margin-bottom: 1.25rem;
            font-size: 1.75rem;
            font-weight: 700;
        }
        
        .welcome-card p {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.05rem;
            line-height: 1.7;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #1e293b;
        }
        
        /* Beautiful input styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        /* Chat input */
        .stChatInputContainer {
            border-top: 1px solid #e2e8f0;
            padding-top: 1rem;
            margin-top: 1rem;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #6366f1 !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
        }
        
        /* Status badges for API */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .status-badge.ready {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            color: #065f46;
        }
        
        .status-badge.free {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            color: #1e40af;
        }
        
        /* Powered by badge */
        .powered-by {
            text-align: center;
            padding: 1rem;
            color: #94a3b8;
            font-size: 0.75rem;
        }
        
        .powered-by a {
            color: #6366f1;
            text-decoration: none;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.5rem;
            }
            
            .sub-header {
                font-size: 1.1rem;
            }
            
            .welcome-card {
                padding: 2rem 1.5rem;
            }
            
            .disclaimer-box {
                padding: 1rem 1.25rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar - Language selector first
    render_language_selector_sidebar(lang)
    st.sidebar.divider()
    
    # Get API key and provider
    api_key, provider = get_api_key(lang)
    st.sidebar.divider()
    
    # Rest of sidebar
    render_sidebar(lang)
    
    # Main content
    render_header(lang)
    
    # Check API key
    if not api_key:
        st.info(f"👈 {get_text('configure_api', lang)}")
        
        # Show example conversation
        with st.expander(f"💡 {get_text('example_title', lang)}"):
            st.markdown(get_text("example_user", lang))
            st.markdown("---")
            st.markdown(get_text("example_assistant", lang))
        return
    
    # Initialize RAG engine if needed or if provider changed
    if st.session_state.rag_engine is None or (hasattr(st.session_state.rag_engine, 'provider') and st.session_state.rag_engine.provider != provider):
        with st.spinner(f"🔄 {get_text('loading_knowledge', lang)}"):
            try:
                knowledge_path = Path(__file__).parent / "knowledge"
                st.session_state.rag_engine = PediSafeRAG(api_key, str(knowledge_path), lang, provider)
            except Exception as e:
                handle_api_error(e, lang)
                return
    
    # Render chat history
    render_chat()
    
    # Welcome message if no messages
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="welcome-card">
            <h3>{get_text('welcome_title', lang)}</h3>
            {get_text('welcome_message', lang)}
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input(get_text("chat_placeholder", lang)):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner(f"{get_text('analyzing', lang)}..."):
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
                    handle_api_error(e, lang)

if __name__ == "__main__":
    main()
