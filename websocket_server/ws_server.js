const WebSocket = require("ws");
const http = require("http");
const fetch = require("node-fetch");

const wss = new WebSocket.Server({ port: 8080 });

wss.on("connection", (ws) => {
    console.log("Client connected");
    
    ws.on("message", async (message) => {
        try {
            const data = JSON.parse(message);
            const response = await fetch("http://localhost:8765", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            ws.send(JSON.stringify(result));
        } catch (error) {
            ws.send(JSON.stringify({ error: "Error processing request" }));
        }
    });
    
    ws.on("close", () => {
        console.log("Client disconnected");
    });
});

console.log("WebSocket server running on ws://localhost:8080");
