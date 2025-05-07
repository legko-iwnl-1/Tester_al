import os
import re
from telethon import TelegramClient, events

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

source_chat_ids = list(map(int, os.getenv("-1002635002901").split(',')))
target_chat_id = int(os.getenv("-1002633022255"))

bot = TelegramClient("forward_bot", api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(chats=source_chat_ids))
async def handler(event):
    text = event.raw_text
    chat_title = event.chat.title if hasattr(event.chat, 'title') else "Unknown Chat"

    name = re.search(r"Имя:\s*(.*)", text)
    phone = re.search(r"Телефон:\s*(.*)", text)
    email = re.search(r"Email:\s*(.*)", text)
    telegram = re.search(r"Ваш Telegram:\s*(.*)", text)

    if all([name, phone, email, telegram]):
        clean_message = (
            f"🔔 Новая заявка (из {chat_title}):\n"
            f"👤 Имя: {name.group(1)}\n"
            f"📞 Телефон: {phone.group(1)}\n"
            f"📧 Email: {email.group(1)}\n"
            f"✈️ Telegram: {telegram.group(1)}"
        )
        await bot.send_message(target_chat_id, clean_message)

print("Бот запущен и мониторит чаты...")
bot.run_until_disconnected()
