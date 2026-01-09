"""
PediSafe Configuration
Configuración central para el agente de triaje pediátrico
"""

# System Prompt - Prompt Maestro para el agente
SYSTEM_PROMPT = """Eres PediSafe, un asistente INFORMATIVO de triaje pediátrico para fiebre.
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
Siempre produce una respuesta en español con:
- Nivel de urgencia (🟢 VERDE / 🟡 AMARILLO / 🟠 NARANJA / 🔴 ROJO)
- Qué hacer ahora (acciones)
- Señales de alarma a vigilar
- Qué información falta (si aplica)
- Fuentes/citas: lista de URLs y títulos de los fragmentos usados del contexto."""

# RAG Prompt Template
RAG_TEMPLATE = """CONTEXTO (fragmentos recuperados; úsalo como única fuente de verdad):
{context}

HISTORIAL DE CONVERSACIÓN:
{chat_history}

MENSAJE DEL USUARIO:
{user_message}

INSTRUCCIONES DE RESPUESTA:
1) Si faltan datos mínimos, haz hasta 3 preguntas cortas (máximo) antes de clasificar.
2) Si hay datos suficientes, clasifica el nivel: 🔴 ROJO / 🟠 NARANJA / 🟡 AMARILLO / 🟢 VERDE.
3) Resume la razón en 1–2 líneas y da pasos concretos.
4) Incluye "Fuentes" con título + URL por cada fragmento usado.
5) Si el contexto no permite responder con seguridad, di "No lo sé con certeza" y recomienda contacto médico.
6) Responde siempre en español de forma clara y empática.

IMPORTANTE: Al final de CADA respuesta, incluye este disclaimer:
"⚠️ AVISO: Esta información es solo orientativa y no reemplaza la consulta con un profesional de salud. Ante cualquier duda, consulta a tu pediatra."
"""

# Triage rules for deterministic pre-classification (Capa A)
TRIAGE_RULES = {
    "red_flags": [
        "convulsión", "seizure", "convulsion",
        "no respira", "dificultad respiratoria", "breathing difficulty",
        "piel azul", "blue skin", "cianosis",
        "rigidez cuello", "stiff neck",
        "inconsciente", "unresponsive", "no responde",
        "manchas púrpuras", "purple spots", "petequias",
        "fontanela abultada", "bulging fontanelle"
    ],
    "age_thresholds": {
        "0-3_months": {"temp_c": 38.0, "level": "ROJO"},
        "3-6_months": {"temp_c": 38.3, "level": "NARANJA"},
        "6-12_months": {"temp_c": 38.9, "level": "AMARILLO"},
        "over_12_months": {"temp_c": 39.0, "level": "AMARILLO"}
    }
}

# UI Configuration
UI_CONFIG = {
    "page_title": "🩺 PediSafe - Triaje Pediátrico",
    "page_icon": "🩺",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Triage level colors and descriptions
TRIAGE_LEVELS = {
    "ROJO": {
        "emoji": "🔴",
        "color": "#dc3545",
        "description": "URGENCIA - Busca atención médica INMEDIATA",
        "action": "Llama al 911 o ve a urgencias ahora"
    },
    "NARANJA": {
        "emoji": "🟠", 
        "color": "#fd7e14",
        "description": "PRIORIDAD ALTA - Contacta al pediatra hoy",
        "action": "Llama a tu pediatra lo antes posible"
    },
    "AMARILLO": {
        "emoji": "🟡",
        "color": "#ffc107",
        "description": "MONITOREAR - Vigila la evolución",
        "action": "Puedes cuidar en casa, pero mantente atento"
    },
    "VERDE": {
        "emoji": "🟢",
        "color": "#28a745",
        "description": "BAJO RIESGO - Cuidados en casa apropiados",
        "action": "Medidas de confort y observación"
    }
}
