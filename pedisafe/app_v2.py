"""
PediSafe - Pediatric Fever Triage Agent
Streamlit Application with RAG for fever guidance in children
Hackathon: Alameda Hacks 2026
Track: Social Good + ML/AI

Bilingual: English (Primary) / Spanish (Secondary)
"""

import streamlit as st
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

def get_api_key(lang: str) -> str | None:
    """
    Get API key with BYOK (Bring Your Own Key) pattern
    Priority: 1) Owner key (secrets/env) 2) User key
    """
    owner_key = None
    
    try:
        if hasattr(st, 'secrets') and "OPENAI_API_KEY" in st.secrets:
            owner_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    if not owner_key:
        owner_key = os.getenv("OPENAI_API_KEY")
    
    st.sidebar.markdown(f"### {get_text('api_key_section', lang)}")
    
    has_owner_key = owner_key is not None and len(owner_key) > 10
    
    if has_owner_key:
        st.sidebar.success(f"✅ {get_text('demo_key_available', lang)}")
        use_own = st.sidebar.toggle(get_text("use_own_key", lang), value=False)
    else:
        st.sidebar.warning(f"⚠️ {get_text('no_demo_key', lang)}")
        use_own = True
    
    if use_own:
        user_key = st.sidebar.text_input(
            "OpenAI API Key",
            type="password",
            placeholder=get_text("api_key_placeholder", lang),
            help=get_text("api_key_help", lang)
        )
        if user_key and user_key.startswith("sk-"):
            st.session_state["api_key"] = user_key
            return user_key
        elif user_key:
            st.sidebar.error(get_text("api_key_error", lang))
            return None
        return None
    else:
        st.session_state.pop("user_api_key", None)
        return owner_key

def render_sidebar(lang: str):
    """Render sidebar with information and controls"""
    st.sidebar.markdown(f"# {get_text('sidebar_title', lang)}")
    st.sidebar.markdown(f"*{get_text('sidebar_subtitle', lang)}*")
    st.sidebar.divider()
    
    # Language selector at top
    st.sidebar.markdown(f"### {get_text('language_selector', lang)}")
    lang_options = {
        "English 🇺🇸": "en",
        "Español 🇪🇸": "es"
    }
    selected_lang = st.sidebar.selectbox(
        "Select language / Seleccionar idioma",
        options=list(lang_options.keys()),
        index=0 if lang == "en" else 1,
        label_visibility="collapsed"
    )
    
    new_lang = lang_options[selected_lang]
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.session_state.rag_engine = None
        st.rerun()
    
    st.sidebar.divider()
    
    # Triage levels reference
    st.sidebar.markdown(f"### {get_text('triage_levels_title', lang)}")
    triage_levels = get_triage_levels(lang)
    for level, info in triage_levels.items():
        st.sidebar.markdown(f"{info['emoji']} **{level}**: {info['description']}")
    
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
    
    # Custom CSS for modern, intuitive UI
    st.markdown("""
    <style>
        /* Modern color scheme */
        :root {
            --primary-color: #2563eb;
            --secondary-color: #7c3aed;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --bg-light: #f8fafc;
            --text-dark: #1e293b;
        }
        
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .sub-header {
            font-size: 1.25rem;
            color: #64748b;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }
        
        .disclaimer-box {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 1.25rem;
            border-radius: 12px;
            border-left: 4px solid #f59e0b;
            font-size: 0.9rem;
            color: #78350f;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 2rem;
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
            border-radius: 16px;
            padding: 1rem;
            margin: 0.75rem 0;
        }
        
        /* Improved sidebar */
        .css-1d391kg {
            background-color: #f8fafc;
        }
        
        /* Better buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Welcome card */
        .welcome-card {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            padding: 2rem;
            border-radius: 16px;
            border-left: 6px solid #2563eb;
            margin: 2rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .welcome-card h3 {
            color: #1e40af;
            margin-bottom: 1rem;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #1e293b;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #2563eb !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar(lang)
    
    # Get API key
    api_key = get_api_key(lang)
    
    # Main content
    render_header(lang)
    
    st.divider()
    
    # Check API key
    if not api_key:
        st.info(f"👈 {get_text('configure_api', lang)}")
        
        # Show example conversation
        with st.expander(f"💡 {get_text('example_title', lang)}"):
            st.markdown(get_text("example_user", lang))
            st.markdown("---")
            st.markdown(get_text("example_assistant", lang))
        return
    
    # Initialize RAG engine if needed
    if st.session_state.rag_engine is None:
        with st.spinner(f"🔄 {get_text('loading_knowledge', lang)}"):
            try:
                knowledge_path = Path(__file__).parent / "knowledge"
                st.session_state.rag_engine = PediSafeRAG(api_key, str(knowledge_path), lang)
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
