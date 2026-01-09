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
        st.session_state.llm_provider = "openai"
    if "cerebras_key" not in st.session_state:
        st.session_state.cerebras_key = None
    if "legend_minimized" not in st.session_state:
        st.session_state.legend_minimized = True

def get_api_key(lang: str) -> tuple[str | None, str]:
    """
    Get API key with BYOK (Bring Your Own Key) pattern
    Returns: (api_key, provider) where provider is 'openai' or 'cerebras'
    """
    st.sidebar.markdown(f"### 🤖 {get_text('llm_provider_section', lang) if 'llm_provider_section' in get_text.__code__.co_names else 'LLM Provider'}")
    
    # Provider selector
    provider_options = {
        "OpenAI (GPT-4o-mini)": "openai",
        "Cerebras (Llama 3.3 70B)": "cerebras"
    }
    selected_provider = st.sidebar.selectbox(
        "Select Provider",
        options=list(provider_options.keys()),
        index=0 if st.session_state.llm_provider == "openai" else 1,
        key="provider_selector"
    )
    provider = provider_options[selected_provider]
    st.session_state.llm_provider = provider
    
    st.sidebar.divider()
    st.sidebar.markdown(f"### 🔑 API Key")
    
    # Check for owner keys
    if st.session_state.saved_owner_key is None:
        owner_key = None
        try:
            key_name = "CEREBRAS_API_KEY" if provider == "cerebras" else "OPENAI_API_KEY"
            if hasattr(st, 'secrets') and key_name in st.secrets:
                owner_key = st.secrets[key_name]
        except:
            pass
        
        if not owner_key:
            key_name = "CEREBRAS_API_KEY" if provider == "cerebras" else "OPENAI_API_KEY"
            owner_key = os.getenv(key_name)
        
        st.session_state.saved_owner_key = owner_key
    else:
        owner_key = st.session_state.saved_owner_key
    
    has_owner_key = owner_key is not None and len(owner_key) > 10
    
    if has_owner_key:
        st.sidebar.success(f"✅ Demo key available")
        use_own = st.sidebar.toggle("Use my own API Key", value=False, key="use_own_key_toggle")
    else:
        st.sidebar.warning(f"⚠️ No demo key - enter your API Key")
        use_own = True
    
    if use_own:
        # Get appropriate key based on provider
        if provider == "cerebras":
            st.sidebar.success("🆓 **100% GRATIS**: Cerebras + Hugging Face embeddings (sin costo)")
            st.sidebar.info("Obtén tu clave gratuita en [cloud.cerebras.ai](https://cloud.cerebras.ai)")
            default_value = st.session_state.cerebras_key if st.session_state.cerebras_key else ""
            user_key = st.sidebar.text_input(
                "Cerebras API Key",
                type="password",
                value=default_value,
                placeholder="csk-...",
                help="Formato: csk-xxxxxxxxxxxxxxxxxxxxxxxx",
                key="cerebras_api_key_input"
            )
            if user_key and len(user_key) > 10:
                st.session_state.cerebras_key = user_key
                return user_key, "cerebras"
            elif st.session_state.cerebras_key and len(st.session_state.cerebras_key) > 10:
                return st.session_state.cerebras_key, "cerebras"
            else:
                return None, "cerebras"
        else:
            default_value = st.session_state.api_key if st.session_state.api_key and st.session_state.api_key.startswith("sk-") else ""
            user_key = st.sidebar.text_input(
                "OpenAI API Key",
                type="password",
                value=default_value,
                placeholder="sk-...",
                help="Get your key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)",
                key="openai_api_key_input"
            )
            if user_key and user_key.startswith("sk-"):
                st.session_state.api_key = user_key
                return user_key, "openai"
            return st.session_state.api_key if st.session_state.api_key and st.session_state.api_key.startswith("sk-") else None, "openai"
    else:
        return owner_key, provider

def render_sidebar(lang: str):
    """Render sidebar with information and controls"""
    st.sidebar.markdown(f"# {get_text('sidebar_title', lang)}")
    st.sidebar.markdown(f"*{get_text('sidebar_subtitle', lang)}*")
    st.sidebar.divider()
    
    # Triage legend
    render_triage_legend_sidebar(lang)
    st.sidebar.divider()
    
    # Quick guide
    with st.sidebar.expander(get_text("info_to_provide", lang)):
        st.markdown(get_text("info_list", lang))
    
    st.sidebar.divider()
    
    # Sources
    st.sidebar.markdown(f"### {get_text('medical_sources', lang)}")
    st.sidebar.markdown("""
    - [🌐 AAP HealthyChildren.org](https://healthychildren.org)
    - [🌐 NHS UK](https://nhs.uk)
    """)
    
    # Knowledge base files
    with st.sidebar.expander(get_text("knowledge_files", lang)):
        knowledge_path = Path(__file__).parent / "knowledge"
        if knowledge_path.exists():
            md_files = list(knowledge_path.glob("*.md"))
            for file in sorted(md_files):
                st.markdown(f"📄 `{file.name}`")
        else:
            st.warning(get_text("no_knowledge_files", lang))
    
    # Clear chat button
    st.sidebar.divider()
    if st.sidebar.button(f"🗑️ {get_text('clear_chat', lang)}", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

def render_fixed_language_selector(lang: str):
    """Render fixed language selector at top right"""
    lang_options = {
        "English 🇺🇸": "en",
        "Español 🇪🇸": "es"
    }
    
    # Create HTML for fixed language selector
    current_lang_display = "English 🇺🇸" if lang == "en" else "Español 🇪🇸"
    other_lang = "es" if lang == "en" else "en"
    other_lang_display = "Español 🇪🇸" if lang == "en" else "English 🇺🇸"
    
    st.markdown(f"""
    <div class="fixed-language-selector">
        <div class="language-toggle">
            <span class="current-lang">🌐 {current_lang_display}</span>
            <button class="lang-switch-btn" onclick="document.getElementById('lang-switch-trigger').click();">⇄</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden selectbox for actual language switching
    with st.container():
        selected_lang = st.selectbox(
            "Language",
            options=list(lang_options.keys()),
            index=0 if lang == "en" else 1,
            key="main_language_selector",
            label_visibility="collapsed"
        )
        
        new_lang = lang_options[selected_lang]
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.session_state.rag_engine = None
            st.rerun()

def render_triage_legend_sidebar(lang: str):
    """Render triage legend in sidebar as expander"""
    triage_levels = get_triage_levels(lang)
    legend_title = get_text('triage_levels_title', lang)
    
    with st.sidebar.expander(f"📊 {legend_title}", expanded=False):
        for level, info in triage_levels.items():
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; 
                        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%); 
                        border-radius: 10px; margin: 0.5rem 0; border: 1px solid #e2e8f0;">
                <span style="font-size: 1.2rem;">{info['emoji']}</span>
                <span style="font-weight: 700; color: {info['color']}; font-size: 0.9rem;">{level}</span>
            </div>
            """, unsafe_allow_html=True)

def render_header(lang: str):
    """Render main header"""
    st.markdown(f'<h1 class="main-header">{get_text("main_title", lang)}</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sub-header">{get_text("subtitle", lang)}</p>',
        unsafe_allow_html=True
    )
    
    st.markdown(f"""
    <div class="disclaimer-box">
        {get_text("disclaimer", lang)}
    </div>
    """, unsafe_allow_html=True)

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
        
        /* Fixed Language Selector - Top Right */
        .fixed-language-selector {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 0.85rem 1.5rem;
            border-radius: 50px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideInRight 0.6s ease-out;
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .fixed-language-selector:hover {
            box-shadow: 0 12px 32px rgba(0,0,0,0.16), 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .language-toggle {
            display: flex;
            align-items: center;
            gap: 0.85rem;
        }
        
        .current-lang {
            font-weight: 600;
            color: #1e293b;
            font-size: 0.95rem;
            letter-spacing: -0.01em;
        }
        
        .lang-switch-btn {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            cursor: pointer;
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        }
        
        .lang-switch-btn:hover {
            transform: rotate(180deg) scale(1.1);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.5);
        }
        
        /* Fixed Triage Legend - Bottom (Compacto y menos intrusivo) */
        .fixed-triage-legend {
            position: fixed;
            bottom: 15px;
            right: 20px;
            z-index: 9998;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 0.75rem 1.25rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08);
            border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            max-width: 600px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Estado minimizado por defecto */
        .fixed-triage-legend.minimized {
            padding: 0.65rem 1rem;
            max-width: 200px;
        }
        
        .fixed-triage-legend.minimized .legend-content {
            display: none;
        }
        
        .legend-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            user-select: none;
        }
        
        .fixed-triage-legend.minimized .legend-header {
            margin-bottom: 0;
        }
        
        .legend-title {
            font-weight: 700;
            color: #1e293b;
            font-size: 0.9rem;
            white-space: nowrap;
        }
        
        .legend-toggle-icon {
            color: #6366f1;
            font-size: 0.85rem;
            font-weight: 700;
            transition: transform 0.3s ease;
        }
        
        .legend-header:hover .legend-toggle-icon {
            transform: scale(1.2);
        }
        
        .legend-content {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid #e2e8f0;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.45rem 0.75rem;
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border-radius: 10px;
            transition: all 0.2s ease;
            border: 1px solid #e2e8f0;
            cursor: default;
        }
        
        .legend-item:hover {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            transform: translateY(-2px);
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
        }
        
        .legend-emoji {
            font-size: 1.15rem;
        }
        
        .legend-level {
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: -0.01em;
        }
        
        /* Adjust main content to avoid overlap with fixed elements */
        .main .block-container {
            padding-bottom: 120px !important;
            padding-top: 80px !important;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .fixed-language-selector {
                top: 10px;
                right: 10px;
                padding: 0.5rem 0.75rem;
            }
            
            .current-lang {
                font-size: 0.85rem;
            }
            
            .lang-switch-btn {
                width: 28px;
                height: 28px;
                font-size: 1rem;
            }
            
            .fixed-triage-legend {
                bottom: 10px;
                right: 10px;
                padding: 0.6rem 0.85rem;
                max-width: calc(100% - 20px);
            }
            
            .fixed-triage-legend.minimized {
                max-width: 180px;
            }
            
            .legend-title {
                font-size: 0.8rem;
            }
            
            .legend-content {
                gap: 0.5rem;
            }
            
            .legend-item {
                padding: 0.35rem 0.55rem;
            }
            
            .legend-emoji {
                font-size: 1rem;
            }
            
            .legend-level {
                font-size: 0.75rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar(lang)
    
    # Get API key and provider
    api_key, provider = get_api_key(lang)
    
    # Fixed elements (rendered first to be available throughout)
    render_fixed_language_selector(lang)
    
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
