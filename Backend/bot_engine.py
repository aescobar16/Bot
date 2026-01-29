import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# Silenciar logs molestos
# =========================
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# =========================
# Cargar .env desde raíz
# =========================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("No se encontró GEMINI_API_KEY en .env")

genai.configure(api_key=API_KEY)

# =========================
# Modelo
# =========================
model = genai.GenerativeModel("models/gemini-flash-latest")
chat = model.start_chat(history=[])

# =========================
# Estado de modo
# =========================
modo_respuesta = "normal"

# =========================
# Modos de respuesta
# =========================
def construir_estilo():
    if modo_respuesta == "estricto":
        return "Responde técnico, directo y breve."
    
    if modo_respuesta == "explicativo":
        return "Explica paso a paso con ejemplos."

    if modo_respuesta == "copiloto":
        return """
Actúa como copiloto programador senior.
Analiza código.
Corrige errores.
Sugiere mejoras.
Entrega código listo.
Cierra con 'Siguiente paso recomendado'.
"""

    return "Responde claro y profesional."

def set_modo(modo: str):
    global modo_respuesta
    if modo in ["normal", "estricto", "explicativo", "copiloto"]:
        modo_respuesta = modo

# =========================
# Responder
# =========================
def responder(mensaje: str) -> str:

    texto = mensaje.strip().lower()

    # respuestas locales rápidas
    if texto in ["hola", "hey", "buenas"]:
        return "Qué tal. Listo para programar. Dime qué necesitas."

    if texto in ["ayuda", "help"]:
        return (
            "Puedo ayudarte con:\n"
            "- revisar código\n"
            "- explicar conceptos\n"
            "- debug\n"
            "- arquitectura\n"
            "- mejoras\n"
        )

    estilo = construir_estilo()

    prompt = f"""
Eres un asistente experto en programación.
{estilo}

Mensaje:
{mensaje}
"""

    try:
        r = chat.send_message(prompt)
        return r.text

    except Exception as e:
        if "429" in str(e):
            return "Error: demasiadas peticiones. Espera 30s."
        return f"Error LLM: {e}"
