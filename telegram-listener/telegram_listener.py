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

client = TelegramClient("session_name" + PHONE, API_ID, API_HASH)

async def send_to_websocket(message):
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(json.dumps(message))

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
    print("MENU")
    choose = input("1 -giris yap\n2 -cikis yap\n")
    if choose == "1":
        await client.start(PHONE)
        print("Telegram Listener Başladı!")
        await client.run_until_disconnected()

    if choose == "2":
        await client.connect()
        await client.log_out()
        print("Cikis yapildi")

if __name__ == "__main__":
    asyncio.run(main())
