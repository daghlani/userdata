from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import socks, os, socket

# Set up the proxy
socks.set_default_proxy(socks.SOCKS5, "localhost", 2080)
socket.socket = socks.socksocket

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f'Your Telegram ID is: {user.id}')
    update.message.reply_text(f'Your username is: {user.username}')
    update.message.reply_text(f'Your first name is: {user.first_name}')
    update.message.reply_text(f'Your last name is: {user.last_name}')

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set.")
    updater = Updater(token)
    # Replace 'YOUR_TOKEN' with your bot's token
    # updater = Updater("YOUR_TOKEN")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
