from telethon import TelegramClient, events
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE_NUMBER")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")  # Render Cloud WebSocket URL'si

# Oturum dosyasını Render Cloud'un geçici depolama alanında sakla
SESSION_FILE = "/tmp/session_name_" + PHONE

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

async def send_to_websocket(message):
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(json.dumps(message))
            print("Mesaj WebSocket'e gönderildi:", message)
    except Exception as e:
        print("WebSocket'e bağlanırken hata oluştu:", e)

@client.on(events.NewMessage)
async def handle_new_message(event):
    message_data = {
        "sender": event.sender_id,
        "message": event.raw_text,
        "chat_id": event.chat_id
    }
    print("Yeni mesaj alındı:", message_data)
    await send_to_websocket(message_data)

async def main():
    print("Telegram Listener Başlatılıyor...")
    await client.start(PHONE)
    print("Telegram Listener Başladı!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())