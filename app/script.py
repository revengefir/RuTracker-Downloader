import os
import requests
from shingram import Bot

# CONFIG
BOT_TOKEN = os.environ.get("BOT_TOKEN")

USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

LOGIN_URL = "https://rutracker.org/forum/login.php"
BASE_TORRENT_URL = "https://rutracker.org/forum/dl.php?t="

DOWNLOAD_DIR = "/home/downloads"

bot = Bot(BOT_TOKEN)

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

SESSION = login()


@bot.on("command:start")
def handle_start(event):
    bot.send_message(
        chat_id=event.chat_id,
        text=("Send message in format: <type> <rutracker_id>(digits after t=)")
    )

@bot.on("message")
def handle_message(event):
    try:
        if not event.text:
            return

        parts = event.text.strip().split()

        if len(parts) != 2:
            bot.send_message(
                chat_id=event.chat_id,
                text="Format: <type> <id> Example: films 123456"
            )
            return

        content_type = parts[0].lower()
        torrent_id = parts[1]

        if not torrent_id.isdigit():
            bot.send_message(
                chat_id=event.chat_id,
                text="ID must be a number"
            )
            return

        folder_path = os.path.join(DOWNLOAD_DIR, content_type)
        os.makedirs(folder_path, exist_ok=True)

        url = BASE_TORRENT_URL + torrent_id

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = SESSION.get(url, headers=headers)

        file_path = os.path.join(folder_path, f"{torrent_id}.torrent")

        with open(file_path, "wb") as f:
            f.write(response.content)

        bot.send_message(
            chat_id=event.chat_id,
            text=f"Downloaded to {file_path}"
        )

    except Exception as e:
        bot.send_message(
            chat_id=event.chat_id,
            text=f"Error: {str(e)}"
        )

bot.run_async()