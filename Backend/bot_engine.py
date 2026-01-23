# backend/bot_engine.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Reducir ruido en consola
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# =========================
# Configuración inicial
# =========================

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("No se encontró GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=API_KEY)

# Modelo estable y rápido
model = genai.GenerativeModel("models/gemini-flash-latest")

# Chat persistente (memoria)
chat = model.start_chat(history=[])

# =========================
# Estado del bot
# =========================

modo_respuesta = "normal"  # normal | estricto | explicativo

# =========================
# Utilidades internas
# =========================

def construir_estilo():
    if modo_respuesta == "estricto":
        return "Responde de forma concisa, técnica y directa."
    elif modo_respuesta == "explicativo":
        return "Explica paso a paso, con ejemplos claros."
    return "Responde de forma clara y profesional."

def set_modo(modo: str):
    global modo_respuesta
    if modo in ["normal", "estricto", "explicativo"]:
        modo_respuesta = modo

# =========================
# API pública del motor
# =========================

def responder(mensaje: str) -> str:
    texto = mensaje.strip().lower()

    # Respuestas locales (NO usar LLM)
    if texto in ["hola", "buenas", "hey", "hello"]:
        return "Qué tal. Listo para programar. Dime qué necesitas."

    if texto in ["ayuda", "help"]:
        return (
            "Puedo ayudarte con:\n"
            "- Explicaciones de programación\n"
            "- Análisis de código\n"
            "- Debugging\n"
            "- Buenas prácticas\n\n"
            "Escribe tu duda directamente."
        )

    # === LLM ===
    estilo = construir_estilo()

    prompt = f"""
Eres un asistente de programación experto.
{estilo}

Mensaje del usuario:
{mensaje}
"""

    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "Error: demasiadas peticiones. Espera unos segundos."
        return f"Error inesperado: {e}"

