"""
PediSafe Configuration
Configuración central para el agente de triaje pediátrico
"""

from i18n import get_text, get_triage_level_text

def get_system_prompt(lang: str = "en") -> str:
    """Get system prompt in specified language"""
    return get_text("system_prompt", lang)

def get_rag_template(lang: str = "en") -> str:
    """Get RAG template in specified language"""
    return get_text("rag_template", lang)

# Triage rules for deterministic pre-classification (Capa A)
TRIAGE_RULES = {
    "red_flags": [
        "convulsión", "seizure", "convulsion",
        "no respira", "dificultad para respirar", "breathing difficulty", "dificultad respiratoria",
        "piel azul", "blue skin", "cianosis",
        "cuello rígido", "rigidez de cuello", "stiff neck",
        "inconsciente", "unresponsive", "no responde", "muy difícil de despertar",
        "manchas púrpura", "purple spots", "petequias", "manchas de sangre",
        "fontanela abultada", "bulging fontanelle"
    ],
    "age_thresholds": {
        "0-3_months": {"temp_c": 38.0, "level": "ROJO"},
        "3-6_months": {"temp_c": 38.3, "level": "NARANJA"},
        "6-12_months": {"temp_c": 38.9, "level": "AMARILLO"},
        "over_12_months": {"temp_c": 39.0, "level": "AMARILLO"}
    }
}

def get_ui_config(lang: str = "en") -> dict:
    """Get UI configuration in specified language"""
    return {
        "page_title": get_text("page_title", lang),
        "page_icon": get_text("page_icon", lang),
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }

def get_triage_levels(lang: str = "en") -> dict:
    """Get triage levels in specified language"""
    return {
        "RED": get_triage_level_text("RED", lang),
        "ORANGE": get_triage_level_text("ORANGE", lang),
        "YELLOW": get_triage_level_text("YELLOW", lang),
        "GREEN": get_triage_level_text("GREEN", lang)
    }
