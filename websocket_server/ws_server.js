const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 8765 });

wss.on("connection", function connection(ws) {
  console.log("WebSocket bağlantısı kuruldu.");

  ws.on("message", function incoming(message) {
    console.log("Telegram'dan Gelen Mesaj:", JSON.parse(message));
    
    // Burada mesajı bir veritabanına veya frontend'e gönderebilirsin
  });
});

console.log("WebSocket sunucusu 8765 portunda çalışıyor.");
