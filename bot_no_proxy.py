from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f'Your Telegram ID is: {user.id}')
    await update.message.reply_text(f'Your username is: {user.username}')
    await update.message.reply_text(f'Your first name is: {user.first_name}')
    await update.message.reply_text(f'Your last name is: {user.last_name}')

def main() -> None:
    # Read the bot token from the environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN environment variable set.")

    # Create the Application
    application = Application.builder().token(token).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start polling for updates
    application.run_polling()

if __name__ == '__main__':
    main()
