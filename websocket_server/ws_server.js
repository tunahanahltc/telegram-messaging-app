const WebSocket = require("ws");
const http = require("http");

const server = http.createServer((req, res) => {
    if (req.url === "/health") {
        res.writeHead(200, { "Content-Type": "text/plain" });
        res.end("OK");
    }
});

const wss = new WebSocket.Server({ server });

wss.on("connection", (ws) => {
    console.log("Client connected");

    ws.on("message", async (message) => {
        try {
            const data = JSON.parse(message);
            const result = { result: data.num1 + data.num2 };
            ws.send(JSON.stringify(result));
        } catch (error) {
            ws.send(JSON.stringify({ error: "Error processing request" }));
        }
    });

    ws.on("close", () => {
        console.log("Client disconnected");
    });
});

server.listen(8080, () => {
    console.log("Server running on http://localhost:8080");
});
