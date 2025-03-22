import os
import asyncio
import websockets
from aiohttp import web

# Render'ın atadığı portu kullan
PORT = int(os.getenv("PORT", 8765))

# WebSocket handler
async def websocket_handler(websocket, path):
    print("Bir istemci bağlandı.")
    try:
        async for message in websocket:
            print(f"Alınan mesaj: {message}")
            # İstemciye yanıt gönder
            await websocket.send(f"Sunucu: {message} alındı!")
    except websockets.exceptions.ConnectionClosed:
        print("İstemci bağlantısı kapatıldı.")

# Health check endpoint
async def health_check(request):
    return web.Response(text="OK")

# HTTP sunucusunu başlat (Health Check için)
async def start_http_server():
    app = web.Application()
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"HTTP sunucusu {PORT} portunda başlatıldı.")

# WebSocket sunucusunu başlat
async def start_websocket_server():
    async with websockets.serve(websocket_handler, "0.0.0.0", PORT):
        print(f"WebSocket sunucusu {PORT} portunda başlatıldı.")
        await asyncio.Future()  # Sunucuyu sürekli çalışır halde tut

# Ana fonksiyon
async def main():
    await start_http_server()
    await start_websocket_server()

if __name__ == "__main__":
    asyncio.run(main())