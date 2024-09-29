import logging
import hmac
import hashlib
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configuración básica de logging para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot
BOT_TOKEN = '7932135408:AAFpBzgkq2ZPcrFQgMiRGf5s_633LTYvZ8Q'
WHOP_SECRET = 'tu_secreto_del_webhook'  # Puedes obtenerlo en Whop si es necesario

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Definir el comando /start
def start(update: Update, context: CallbackContext):
    logger.info("El comando /start fue ejecutado")
    update.message.reply_text("¡Bienvenido! Este es el bot de control de acceso.")

# Verificar la firma del Webhook de Whop
def verify_signature(payload, signature):
    computed_signature = hmac.new(WHOP_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

# Ruta para recibir Webhooks de Whop
@app.route('/whop-webhook', methods=['POST'])
def whop_webhook():
    payload = request.get_data(as_text=True)
    signature = request.headers.get('X-Whop-Signature')

    if not verify_signature(payload, signature):
        return jsonify({'error': 'Firma inválida'}), 400

    data = request.json
    event = data.get('event')
    telegram_user_id = data.get('telegram_user_id')

    if event == 'membership_went_valid':
        invite_link = bot.export_chat_invite_link(chat_id='@tu_canal_premium')
        bot.send_message(chat_id=telegram_user_id, text=f"¡Bienvenido al canal premium! Únete aquí: {invite_link}")

    elif event == 'membership_went_invalid':
        bot.send_message(chat_id=telegram_user_id, text="Tu suscripción ha expirado. Se te ha removido del canal premium.")

    return 'OK', 200

# Función principal para iniciar el bot de Telegram y el servidor Flask
def main():
    logger.info("Iniciando el bot...")

    # Crear el objeto Updater y pasarle el token del bot
    updater = Updater(BOT_TOKEN, use_context=True)

    # Obtener el dispatcher para registrar los comandos
    dispatcher = updater.dispatcher

    # Registrar el comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Iniciar el bot de Telegram
    updater.start_polling()
    logger.info("Bot está ejecutándose. Esperando comandos.")

    # Iniciar el servidor Flask para los Webhooks de Whop
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
