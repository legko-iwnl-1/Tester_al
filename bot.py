import os
import re
from telethon import TelegramClient, events

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

session_path = "/etc/secrets/forward_bot.session"

#
source_chat_ids = list(map(int, os.getenv("SOURCE_CHAT_IDS").split(',')))
target_chat_id = int(os.getenv("TARGET_CHAT_ID"))

client = TelegramClient(session_path, api_id, api_hash)

@client.on(events.NewMessage(chats=source_chat_ids))
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
        await client.send_message(target_chat_id, clean_message)

print("Запуск Telegram клиента...")
client.start()
print("Бот запущен. Ожидаем сообщения...")
client.run_until_disconnected()
