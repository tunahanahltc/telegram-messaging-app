const WebSocket = require('ws');

// Render üzerindeki WebSocket sunucusuna bağlan
const ws = new WebSocket('wss://websocket-server-vubd.onrender.com');

ws.on('open', () => {
    console.log('WebSocket sunucusuna bağlandı.');
    // Sunucuya mesaj gönder
    ws.send('Merhaba, ben Node.js istemcisi!');
});

ws.on('message', (data) => {
    console.log(`Sunucudan gelen yanıt: ${data}`);
});

ws.on('close', () => {
    console.log('WebSocket bağlantısı kapatıldı.');
});