import asyncio
import websockets
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTP Sağlık Kontrolü için basit bir HTTP sunucu
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

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

def run_health_check_server():
    httpd = HTTPServer(("0.0.0.0", 8080), HealthCheckHandler)
    print("Health check server running on port 8080")
    httpd.serve_forever()

if __name__ == "__main__":
    import threading

    # Sağlık kontrolü için HTTP sunucusunu başlat
    threading.Thread(target=run_health_check_server, daemon=True).start()

    # WebSocket sunucusunu başlat
    asyncio.run(websocket_server())
