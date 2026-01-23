# backend/api.py

from flask import Flask, request, jsonify
from flask_cors import CORS 
from bot_engine import responder, set_modo

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)

    mensaje = data.get("mensaje", "")
    modo = data.get("modo")  # opcional

    if modo:
        set_modo(modo)

    if not mensaje.strip():
        return jsonify({"respuesta": "Mensaje vacío."}), 400

    respuesta = responder(mensaje)
    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
