from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import json
import socks
import socket

# Directory to store user data
USER_DATA_DIR = "user_data"

# Ensure the directory exists
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Set up the proxy
socks.set_default_proxy(socks.SOCKS5, "localhost", 2080)  # Use the service name as the host
socket.socket = socks.socksocket

def escape_markdown(text: str) -> str:
    """
    Escape reserved MarkdownV2 characters.
    """
    reserved_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in reserved_chars:
        text = text.replace(char, f"\\{char}")
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Prepare user data
    user_data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    # Create a file named after the user's ID
    file_path = os.path.join(USER_DATA_DIR, f"{user.id}.json")

    # Write user data to the file in JSON format
    with open(file_path, "w") as file:
        json.dump(user_data, file, indent=4)

    # Prepare the response message
    response_message = (
        "Here’s your information:\n\n"
        f"🆔 *ID:* `{escape_markdown(str(user.id))}`\n"
        f"👤 *Username:* `{escape_markdown(user.username or 'N/A')}`\n"
        f"1️⃣ *First Name:* `{escape_markdown(user.first_name or 'N/A')}`\n"
        f"2️⃣ *Last Name:* `{escape_markdown(user.last_name or 'N/A')}`\n"
    )

    # Send the response
    await update.message.reply_text(response_message, parse_mode="MarkdownV2")

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