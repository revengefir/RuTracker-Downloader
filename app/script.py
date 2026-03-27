import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

#CONFIG
BOT_TOKEN = os.environ.get("BOT_TOKEN")

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

LOGIN_URL = "https://rutracker.org/forum/login.php"
BASE_TORRENT_URL = "https://rutracker.org/forum/dl.php?t="

DOWNLOAD_DIR = "/home/downloads"

TYPE, TORRENT_ID = range(2)


def login():
    session = requests.Session()

    login_data = {
        "login_username": USERNAME,
        "login_password": PASSWORD,
        "login": "Вход"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    session.post(LOGIN_URL, data=login_data, headers=headers)
    return session


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send type: films or series")
    return TYPE


async def get_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_type = update.message.text.lower()

    if user_type not in ["films", "series"]:
        await update.message.reply_text("Only 'films' or 'series'")
        return TYPE

    context.user_data["type"] = user_type
    await update.message.reply_text("Now send torrent ID (number after t=)")
    return TORRENT_ID


async def get_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    torrent_id = update.message.text.strip()

    if not torrent_id.isdigit():
        await update.message.reply_text("ID must be a number")
        return TORRENT_ID

    content_type = context.user_data["type"]

    session = login()

    url = BASE_TORRENT_URL + torrent_id

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = session.get(url, headers=headers)


    folder_path = os.path.join(DOWNLOAD_DIR, content_type)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{torrent_id}.torrent")

    with open(file_path, "wb") as f:
        f.write(response.content)

    await update.message.reply_text(f"Downloaded to {file_path}")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled")
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            TORRENT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_torrent)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()