from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ⚠️ Token de tu bot (no lo compartas en público)
TOKEN = "8449870941:AAFi3BGCE6rrbOgWMHlaAI5DAXPRqIWrdTQ"

# Diccionario para guardar stock en memoria
stock = {}

# Comando /anadir
async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tipo = context.args[0].lower().strip()       # camiseta
        talla = context.args[1].upper().strip()     # XL
        color = context.args[2].lower().strip()     # blanca
        cantidad = int(context.args[3])

        clave = f"{tipo}_{talla}_{color}"
        stock[clave] = stock.get(clave, 0) + cantidad

        await update.message.reply_text(
            f"✅ Añadido {cantidad} {tipo}(s) talla {talla} color {color}. "
            f"Total ahora: {stock[clave]}"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correcto: /anadir <tipo> <talla> <color> <cantidad>")

# Comando /eliminar
async def remove_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tipo = context.args[0].lower().strip()
        talla = context.args[1].upper().strip()
        color = context.args[2].lower().strip()
        cantidad = int(context.args[3])

        clave = f"{tipo}_{talla}_{color}"

        if clave not in stock or stock[clave] < cantidad:
            await update.message.reply_text(
                f"⚠️ No hay suficiente stock de {tipo} talla {talla} color {color} para eliminar."
            )
            return

        stock[clave] -= cantidad
        await update.message.reply_text(
            f"🗑️ Eliminado {cantidad} {tipo}(s) talla {talla} color {color}. "
            f"Total ahora: {stock[clave]}"
        )
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Uso correcto: /eliminar <tipo> <talla> <color> <cantidad>")

# Comando /stock
async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stock:
        await update.message.reply_text("📦 El stock está vacío.")
        return

    respuesta = "📋 Stock actual:\n"
    for clave, cantidad in stock.items():
        tipo, talla, color = clave.split("_")
        respuesta += f"- {tipo} {talla} {color}: {cantidad}\n"

    await update.message.reply_text(respuesta)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido a *StockAxonBot*.\n\n"
        "Comandos disponibles:\n"
        "➕ /anadir <tipo> <talla> <color> <cantidad>\n"
        "➖ /eliminar <tipo> <talla> <color> <cantidad>\n"
        "📦 /stock (ver inventario)\n",
        parse_mode="Markdown"
    )

# Configuración principal del bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anadir", add_stock))
    app.add_handler(CommandHandler("eliminar", remove_stock))
    app.add_handler(CommandHandler("stock", show_stock))

    print("🤖 Bot en marcha... ve a Telegram y habla con @StockAxonBot")
    app.run_polling()

if __name__ == "__main__":
    main()
