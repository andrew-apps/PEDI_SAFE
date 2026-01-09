"""
PediSafe Internationalization (i18n)
Bilingual support: English (primary) and Spanish (secondary)
"""

TRANSLATIONS = {
    "en": {
        # Page config
        "page_title": "🩺 PediSafe - Pediatric Fever Triage",
        "page_icon": "🩺",
        
        # Header
        "main_title": "🩺 PediSafe",
        "subtitle": "AI-Powered Pediatric Fever Triage Assistant",
        "disclaimer": """⚠️ **IMPORTANT:** PediSafe is an INFORMATIONAL tool based on public guidelines (AAP, NHS). It does **NOT replace** professional medical consultation. If in doubt or in an emergency, contact your pediatrician or emergency services.""",
        
        # Sidebar
        "sidebar_title": "🩺 PediSafe",
        "sidebar_subtitle": "*Pediatric Triage Assistant*",
        "api_key_section": "🔑 OpenAI API Key",
        "demo_key_available": "✅ Demo key available",
        "use_own_key": "Use my own OpenAI API Key",
        "no_demo_key": "⚠️ No demo key - enter your OpenAI API Key",
        "api_key_placeholder": "sk-...",
        "api_key_help": "Your key is NOT stored. Only used in this session. Get it from OpenAI (ChatGPT provider).",
        "api_key_error": "OpenAI API Key must start with 'sk-'",
        "triage_levels_title": "📊 Triage Levels",
        "info_to_provide": "📋 Information to Provide",
        "info_list": """
        - Child's **age** (months or years)
        - **Temperature** and how it was taken
        - **Duration** of fever
        - **Additional symptoms**
        - **Pre-existing** medical conditions
        """,
        "medical_sources": "📚 Medical Sources",
        "knowledge_files": "📄 Knowledge Base Files",
        "no_knowledge_files": "No knowledge files found",
        "clear_chat": "🗑️ Clear conversation",
        "language_selector": "🌐 Language / Idioma",
        
        # Triage levels
        "triage_red": "EMERGENCY - Seek IMMEDIATE medical attention",
        "triage_red_action": "Call 911 or go to ER now",
        "triage_orange": "HIGH PRIORITY - Contact pediatrician today",
        "triage_orange_action": "Call your pediatrician as soon as possible",
        "triage_yellow": "MONITOR - Watch for changes",
        "triage_yellow_action": "Home care is okay, but stay alert",
        "triage_green": "LOW RISK - Home care appropriate",
        "triage_green_action": "Comfort measures and observation",
        
        # Main content
        "configure_api": "Please configure your API key in the sidebar to start using PediSafe.",
        "cerebras_free_note": "**Note:** Cerebras offers free API access with rate limits. Make sure you're using a valid API key from [cloud.cerebras.ai](https://cloud.cerebras.ai).",
        "example_title": "💡 Example of how to use PediSafe",
        "example_user": "**You:** My 4-month-old baby has a fever of 101.3°F (38.5°C) for the past 6 hours. He's a bit fussy but eating well.",
        "example_assistant": """**PediSafe:** 🟠 **ORANGE - HIGH PRIORITY**
        
        Based on the information provided:
        - Baby is 4 months old (3-6 months age group)
        - Temperature: 101.3°F (38.5°C)
        - Duration: 6 hours
        
        **Recommendation:** Contact your pediatrician today...""",
        "loading_knowledge": "🔄 Loading medical knowledge base...",
        "welcome_title": "👋 Hello! I'm PediSafe",
        "welcome_message": """
        I'm here to help you assess your child's fever and guide you on the next steps.
        
        **Tell me:**
        - How old is your child (months or years)?
        - What's the temperature and how did you measure it?
        - How long has the fever lasted?
        - Are there any other symptoms?
        """,
        "chat_placeholder": "Describe your child's situation...",
        "analyzing": "Analyzing...",
        
        # Errors
        "quota_error": """
        😔 **Demo credit exhausted**
        
        To continue:
        1. Enable "Use my own API Key" in the sidebar
        2. Enter your OpenAI API Key
        
        [Get your API Key here](https://platform.openai.com/api-keys)
        """,
        "invalid_key_error": "❌ Invalid API Key. Please verify it's correct.",
        "generic_error": "❌ Error: {error}",
        
        # System prompts
        "system_prompt": """You are PediSafe, an INFORMATIONAL pediatric fever triage assistant.
Your goal: help caregivers decide the "next step" (home care / call pediatrician / emergency),
using ONLY the RETRIEVED CONTEXT (RAG) and safety rules.

HARD RULES (NON-NEGOTIABLE)
1) Safety first: if you detect red flags, escalate the level (RED/ORANGE) and recommend immediate medical attention.
2) Do not diagnose or "guarantee" anything. You do not replace a professional.
3) Do not give medication doses (mg, ml, every X hours). You can mention general comfort measures and hydration, and suggest following pediatrician/label instructions.
4) Use ONLY the provided context. If information is missing or context doesn't cover the case, respond: "I don't know for certain" + "contact a professional".
5) Do not request identifiable data (name, exact address, ID). Only age, temperature, duration, and symptoms.
6) Maintain a calm, clear tone, without medical jargon, with concrete steps.

MINIMUM QUESTIONS (if not yet provided)
- Child's age in months (or years and months).
- Temperature + unit (°C/°F) + method (rectal/axillary/ear/forehead).
- Duration of fever.
- Warning signs: breathing difficulty, seizure, stiff neck, concerning rash, extreme drowsiness, dehydration, persistent vomiting, etc.
- Special conditions: immunodeficiency, heart disease, immunosuppressive treatments.

STRUCTURED OUTPUT
Always produce a response in English with this EXACT structure:
1. **Urgency level** (🟢 GREEN / 🟡 YELLOW / 🟠 ORANGE / 🔴 RED) - First line, bold and prominent
2. **What to do now** - Clear action steps
3. **Warning signs to watch for** - Symptoms that require immediate attention
4. **What information is missing** (if applicable) - Questions to ask
5. **Medical Sources** (at the END) - List of URLs and titles of guidelines used

IMPORTANT: Sources MUST be at the end of the response, after all recommendations.""",
        
        "rag_template": """CONTEXT (retrieved fragments; use as sole source of truth):
{context}

CONVERSATION HISTORY:
{chat_history}

USER MESSAGE:
{user_message}

RESPONSE INSTRUCTIONS:
1) If minimum data is missing, ask up to 3 short questions (maximum) before classifying.
2) If there's sufficient data, classify the level: 🔴 RED / 🟠 ORANGE / 🟡 YELLOW / 🟢 GREEN.
3) Provide clear action steps and warning signs.
4) If the context doesn't allow a safe response, say "I don't know for certain" and recommend medical contact.
5) Always respond in English in a clear and empathetic manner.

RESPONSE FORMAT (MANDATORY):
**[Triage Level Emoji + Level]**

**What to do now:**
- [Action 1]
- [Action 2]

**Warning signs to watch for:**
- [Sign 1]
- [Sign 2]

**Medical Sources:**
- [Source 1 with URL]
- [Source 2 with URL]

⚠️ NOTICE: This information is for guidance only and does not replace consultation with a healthcare professional. If in doubt, consult your pediatrician.
""",
    },
    "es": {
        # Page config
        "page_title": "🩺 PediSafe - Triaje Pediátrico",
        "page_icon": "🩺",
        
        # Header
        "main_title": "🩺 PediSafe",
        "subtitle": "Asistente de Triaje Pediátrico con IA",
        "disclaimer": """⚠️ **IMPORTANTE:** PediSafe es una herramienta INFORMATIVA basada en guías públicas (AAP, NHS). **NO reemplaza** la consulta médica profesional. Ante cualquier duda o emergencia, contacta a tu pediatra o servicios de emergencia.""",
        
        # Sidebar
        "sidebar_title": "🩺 PediSafe",
        "sidebar_subtitle": "*Asistente de Triaje Pediátrico*",
        "api_key_section": "🔑 API Key de OpenAI",
        "demo_key_available": "✅ Demo key disponible",
        "use_own_key": "Usar mi propia API Key de OpenAI",
        "no_demo_key": "⚠️ Sin demo key - ingresa tu API Key de OpenAI",
        "api_key_placeholder": "sk-...",
        "api_key_help": "Tu key NO se almacena. Solo se usa en esta sesión. Consíguela de OpenAI (proveedor de ChatGPT).",
        "api_key_error": "La API Key de OpenAI debe empezar con 'sk-'",
        "triage_levels_title": "📊 Niveles de Triaje",
        "info_to_provide": "📋 Información a Proporcionar",
        "info_list": """
        - **Edad** del niño (meses o años)
        - **Temperatura** y cómo se tomó
        - **Duración** de la fiebre
        - **Síntomas** adicionales
        - **Condiciones** médicas previas
        """,
        "medical_sources": "📚 Fuentes Médicas",
        "knowledge_files": "📄 Archivos de Conocimiento",
        "no_knowledge_files": "No se encontraron archivos de conocimiento",
        "clear_chat": "🗑️ Limpiar conversación",
        "language_selector": "🌐 Language / Idioma",
        
        # Triage levels
        "triage_red": "URGENCIA - Busca atención médica INMEDIATA",
        "triage_red_action": "Llama al 911 o ve a urgencias ahora",
        "triage_orange": "PRIORIDAD ALTA - Contacta al pediatra hoy",
        "triage_orange_action": "Llama a tu pediatra lo antes posible",
        "triage_yellow": "MONITOREAR - Vigila la evolución",
        "triage_yellow_action": "Puedes cuidar en casa, pero mantente atento",
        "triage_green": "BAJO RIESGO - Cuidados en casa apropiados",
        "triage_green_action": "Medidas de confort y observación",
        
        # Main content
        "configure_api": "👈 Por favor, configura tu API Key en la barra lateral para comenzar.",
        "example_title": "💡 Ejemplo de cómo usar PediSafe",
        "example_user": "**Tú:** Mi bebé de 4 meses tiene 38.5°C de fiebre desde hace 6 horas. Está un poco irritable pero come bien.",
        "example_assistant": """**PediSafe:** 🟠 **NARANJA - PRIORIDAD ALTA**
        
        Basándome en la información proporcionada:
        - Bebé de 4 meses (3-6 meses de edad)
        - Temperatura de 38.5°C (101.3°F)
        - Duración: 6 horas
        
        **Recomendación:** Contacta a tu pediatra hoy...""",
        "loading_knowledge": "🔄 Cargando base de conocimientos médicos...",
        "welcome_title": "👋 ¡Hola! Soy PediSafe",
        "welcome_message": """
        Estoy aquí para ayudarte a evaluar la fiebre de tu hijo/a y orientarte 
        sobre los siguientes pasos.
        
        **Cuéntame:**
        - ¿Cuántos meses o años tiene tu hijo/a?
        - ¿Cuál es la temperatura y cómo la mediste?
        - ¿Hace cuánto tiempo tiene fiebre?
        - ¿Tiene otros síntomas?
        """,
        "chat_placeholder": "Describe la situación de tu hijo/a...",
        "analyzing": "Analizando...",
        
        # Errors
        "quota_error": """
        😔 **Se agotó el crédito del demo**
        
        Para continuar:
        1. Activa "Usar mi propia API Key" en la barra lateral
        2. Ingresa tu API Key de OpenAI
        
        [Obtén tu API Key aquí](https://platform.openai.com/api-keys)
        """,
        "invalid_key_error": "❌ API Key inválida. Verifica que esté correcta.",
        "generic_error": "❌ Error: {error}",
        
        # System prompts
        "system_prompt": """Eres PediSafe, un asistente INFORMATIVO de triaje pediátrico para fiebre.
Tu objetivo: ayudar a un cuidador a decidir el "siguiente paso" (casa / llamar al pediatra / urgencias),
usando SOLO el CONTEXTO recuperado (RAG) y reglas de seguridad.

REGLAS DURAS (NO NEGOCIABLES)
1) Seguridad primero: si detectas señales de alarma ("red flags"), eleva el nivel (ROJO/NARANJA) y recomienda atención médica inmediata.
2) No diagnostiques ni "garantices" nada. No reemplazas a un profesional.
3) No des dosis de medicamentos (mg, ml, cada X horas). Puedes mencionar medidas generales de confort e hidratación y sugerir seguir indicaciones del pediatra/etiqueta.
4) Usa SOLO el contexto proporcionado. Si falta información o el contexto no cubre el caso, responde: "No lo sé con certeza" + "contacta a un profesional".
5) No solicites datos identificables (nombre, dirección exacta, DNI). Solo edad, temperatura, duración y síntomas.
6) Mantén tono calmado, claro, sin jerga médica, y con pasos concretos.

PREGUNTAS MÍNIMAS (si aún no están)
- Edad del niño en meses (o años y meses).
- Temperatura + unidad (°C/°F) + método (rectal/axilar/oreja/frente).
- Duración de la fiebre.
- Síntomas de alarma: dificultad respiratoria, convulsión, rigidez de cuello, erupción preocupante, somnolencia extrema, deshidratación, vómitos persistentes, etc.
- Condiciones especiales: inmunodeficiencia, cardiopatía, tratamientos inmunosupresores.

SALIDA ESTRUCTURADA
Siempre produce una respuesta en español con esta estructura EXACTA:
1. **Nivel de urgencia** (🟢 VERDE / 🟡 AMARILLO / 🟠 NARANJA / 🔴 ROJO) - Primera línea, en negrita y prominente
2. **Qué hacer ahora** - Pasos de acción claros
3. **Señales de alarma a vigilar** - Síntomas que requieren atención inmediata
4. **Qué información falta** (si aplica) - Preguntas a realizar
5. **Fuentes Médicas** (al FINAL) - Lista de URLs y títulos de las guías utilizadas

IMPORTANTE: Las fuentes DEBEN estar al final de la respuesta, después de todas las recomendaciones.""",
        
        "rag_template": """CONTEXTO (fragmentos recuperados; úsalo como única fuente de verdad):
{context}

HISTORIAL DE CONVERSACIÓN:
{chat_history}

MENSAJE DEL USUARIO:
{user_message}

INSTRUCCIONES DE RESPUESTA:
1) Si faltan datos mínimos, haz hasta 3 preguntas cortas (máximo) antes de clasificar.
2) Si hay datos suficientes, clasifica el nivel: 🔴 ROJO / 🟠 NARANJA / 🟡 AMARILLO / 🟢 VERDE.
3) Proporciona pasos de acción claros y señales de alarma.
4) Si el contexto no permite responder con seguridad, di "No lo sé con certeza" y recomienda contacto médico.
5) Responde siempre en español de forma clara y empática.

FORMATO DE RESPUESTA (OBLIGATORIO):
**[Emoji de Nivel de Triaje + Nivel]**

**Qué hacer ahora:**
- [Acción 1]
- [Acción 2]

**Señales de alarma a vigilar:**
- [Señal 1]
- [Señal 2]

**Fuentes Médicas:**
- [Fuente 1 con URL]
- [Fuente 2 con URL]

⚠️ AVISO: Esta información es solo orientativa y no reemplaza la consulta con un profesional de salud. Ante cualquier duda, consulta a tu pediatra.
""",
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Get translated text for a given key and language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def get_triage_level_text(level: str, lang: str = "en") -> dict:
    """Get triage level information in the specified language"""
    triage_map = {
        "RED": {
            "emoji": "🔴",
            "color": "#dc3545",
            "description": get_text("triage_red", lang),
            "action": get_text("triage_red_action", lang)
        },
        "ORANGE": {
            "emoji": "🟠",
            "color": "#fd7e14",
            "description": get_text("triage_orange", lang),
            "action": get_text("triage_orange_action", lang)
        },
        "YELLOW": {
            "emoji": "🟡",
            "color": "#ffc107",
            "description": get_text("triage_yellow", lang),
            "action": get_text("triage_yellow_action", lang)
        },
        "GREEN": {
            "emoji": "🟢",
            "color": "#28a745",
            "description": get_text("triage_green", lang),
            "action": get_text("triage_green_action", lang)
        }
    }
    return triage_map.get(level.upper(), triage_map["YELLOW"])
