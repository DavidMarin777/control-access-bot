import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configuración básica de logging para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot
BOT_TOKEN = '7932135408:AAFpBzgkq2ZPcrFQgMiRGf5s_633LTYvZ8Q'

# Definir el comando /start
def start(update: Update, context: CallbackContext):
    logger.info("El comando /start fue ejecutado")
    update.message.reply_text("¡Bienvenido! Este es el bot de control de acceso.")

def main():
    logger.info("Iniciando el bot...")
    
    # Crear el objeto Updater y pasarlo el token del bot
    updater = Updater(BOT_TOKEN, use_context=True)

    # Obtener el dispatcher para registrar los comandos
    dispatcher = updater.dispatcher

    # Registrar el comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Iniciar el bot
    updater.start_polling()
    logger.info("Bot está ejecutándose. Esperando comandos.")
    updater.idle()

if __name__ == '__main__':
    main()
