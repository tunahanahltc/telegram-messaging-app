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

        while True:
            # WebSocket sunucusundan mesaj al
            message = await websocket.recv()
            data = json.loads(message)

            if data.get("action") == "phone_received":
                phone = data.get("phone")
                print("Telefon numarası alındı:", phone)

                # Telegram'dan kod talep et
                await client.connect()
                await client.send_code_request(phone)
                print("Telegram'a kod talep edildi.")

            if data.get("action") == "code_received":
                code = data.get("code")
                print("Telefon kodu alındı:", code)

                # Telegram'a giriş yap
                await client.sign_in(phone, code)
                print("Telegram Listener başladı!")
                break

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