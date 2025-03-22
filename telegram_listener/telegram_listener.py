from telethon import TelegramClient, events
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL")

# Oturum dosyasını Render Cloud'un geçici depolama alanında sakla
SESSION_FILE = "/tmp/session_name"

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

async def handle_phone_code():
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print("WebSocket'e bağlandı.")

        # WebSocket sunucusuna telefon numarasını gönder
        phone = input("Telefon numaranızı girin (örn. +901234567890): ")
        await websocket.send(json.dumps({"action": "send_phone", "phone": phone}))

        # WebSocket sunucusundan kodu al
        response = await websocket.recv()
        response = json.loads(response)

        if response.get("action") == "code_received":
            code = response.get("code")
            print("Telefon kodu alındı:", code)

            # Telegram'a giriş yap
            await client.start(phone=phone, code=code)
            print("Telegram Listener başladı!")

@client.on(events.NewMessage)
async def handle_new_message(event):
    message_data = {
        "sender": event.sender_id,
        "message": event.raw_text,
        "chat_id": event.chat_id
    }
    print("Yeni mesaj alındı:", message_data)

    # Mesajı WebSocket üzerinden gönder
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        await websocket.send(json.dumps(message_data))

async def main():
    await handle_phone_code()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())