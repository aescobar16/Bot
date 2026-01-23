const chat = document.getElementById("chat");
const input = document.getElementById("mensaje");

function agregarMensaje(texto, clase) {
    const div = document.createElement("div");
    div.className = "mensaje " + clase;
    div.innerText = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function enviar() {
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje("Tú: " + texto, "usuario");
    input.value = "";

    const respuesta = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensaje: texto,
            modo: "explicativo"
        })
    });

    const data = await respuesta.json();
    agregarMensaje("Bot: " + data.respuesta, "bot");
}
