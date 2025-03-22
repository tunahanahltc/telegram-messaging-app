const WebSocket = require("ws");

// Render'ın atadığı portu kullan
const PORT = process.env.PORT || 8765;

const wss = new WebSocket.Server({ port: PORT });

wss.on("connection", function connection(ws) {
  console.log("WebSocket bağlantısı kuruldu.");

  ws.on("message", function incoming(message) {
    console.log("Telegram'dan Gelen Mesaj:", JSON.parse(message));
    
    // Burada mesajı bir veritabanına veya frontend'e gönderebilirsin
  });
});

console.log(`WebSocket sunucusu ${PORT} portunda çalışıyor.`);