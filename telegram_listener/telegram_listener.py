import asyncio
import websockets
import json

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

async def main():
    server = await websockets.serve(handle_connection, "0.0.0.0", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
