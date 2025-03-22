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
WS_SERVER_URL = os.getenv("URL")
client = TelegramClient("session_name" + PHONE, API_ID, API_HASH)

async def send_to_websocket(message):
    try:
        async with websockets.connect(WS_SERVER_URL) as websocket:
            await websocket.send(json.dumps(message))
    except Exception as e:
        print(f"WebSocket bağlantısı sırasında hata: {e}")

@client.on(events.NewMessage)
async def handle_new_message(event):
    message_data = {
        "sender": event.sender_id,
        "message": event.raw_text,
        "chat_id": event.chat_id
    }
    await send_to_websocket(message_data)

async def main():
    await client.start(PHONE)
    print("Telegram Listener Başladı!")
    await client.run_until_disconnected()
    
if __name__ == "__main__":
    asyncio.run(main())
