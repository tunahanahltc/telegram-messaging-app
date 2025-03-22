from telethon import TelegramClient, events
import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
WEBSOCKET_URL = "wss://websocket-server-vubd.onrender.com"

# Render Cloud'un geçici depolama alanında oturum dosyasını sakla
SESSION_FILE = "/tmp/session_name"

# Render tarafından atanan PORT çevresel değişkenini al
PORT = os.getenv("PORT", 10000)  # Varsayılan olarak 10000 portunu kullanıyoruz

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

async def connect_websocket():
    # WebSocket sunucusuna bağlan
    return await websockets.connect(WEBSOCKET_URL)

async def handle_phone_code(websocket):
    print("WebSocket'e bağlandı.")
    
    while True:
        # WebSocket sunucusundan mesaj al
        message = await websocket.recv()
        data = json.loads(message)

        if data.get("action") == "phone_received":
            phone = data.get("phone")
            print("Telefon numarası alındı:", phone)

            # Telegram'dan kod talep et
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

async def websocket_handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data.get("action") == "phone_received":
            phone = data.get("phone")
            print(f"Telefon numarası alındı: {phone}")
        elif data.get("action") == "code_received":
            code = data.get("code")
            print(f"Kod alındı: {code}")

async def start_websocket_server():
    # WebSocket sunucusunu başlat
    server = await websockets.serve(websocket_handler, "0.0.0.0", int(PORT))
    print(f"WebSocket sunucusu {PORT} portunda başlatıldı.")
    await server.wait_closed()

async def main():
    # WebSocket bağlantısını aç
    websocket = await connect_websocket()

    # Telefon kodunu ve giriş işlemini başlat
    await handle_phone_code(websocket)
    
    # WebSocket sunucusunu başlat
    await start_websocket_server()

    # Telegram istemcisini çalıştır
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())