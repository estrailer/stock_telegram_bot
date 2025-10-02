from flask import Flask
import threading
import bot_telegram

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot de Telegram corriendo en Render!"

if __name__ == "__main__":
    # Inicia el bot en un hilo separado
    threading.Thread(target=bot_telegram.main).start()
    # Render necesita que escuchemos en el puerto asignado
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
