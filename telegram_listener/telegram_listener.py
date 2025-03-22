import asyncio
import websockets
import json
from aiohttp import web

async def handle_connection(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            num1 = data.get("num1", 0)
            num2 = data.get("num2", 0)
            result = num1 + num2
            response = json.dumps({"result": result})
            await websocket.send(response)
        except Exception as e:
            await websocket.send(json.dumps({"error": str(e)}))

async def websocket_server():
    server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
    await server.wait_closed()

async def health_check(request):
    return web.Response(text="OK")

async def start_servers():
    # HTTP Sağlık Kontrol Sunucusu
    app = web.Application()
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    
    # WebSocket Sunucusu
    await websocket_server()

if __name__ == "__main__":
    asyncio.run(start_servers())
