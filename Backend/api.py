from flask import Flask, request, jsonify
from bot_engine import responder, set_modo

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"respuesta": "JSON inválido"}), 400

        mensaje = data.get("mensaje", "")

        # blindaje tipo
        if not isinstance(mensaje, str):
            mensaje = str(mensaje)

        modo = data.get("modo")

        if modo:
            set_modo(modo)

        if not mensaje.strip():
            return jsonify({"respuesta": "Mensaje vacío"}), 400

        respuesta = responder(mensaje)

        return jsonify({"respuesta": respuesta})

    except Exception as e:
        return jsonify({"respuesta": f"Error servidor: {e}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
