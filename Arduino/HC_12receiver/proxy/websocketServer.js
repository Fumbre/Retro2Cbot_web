const WebSocket = require('ws');

const wss = new WebSocket.Server({
  port: 8081,
  path: '/ws'
});

const REMOTE_WS_URL = 'wss://retro2cbot-web-dugz.onrender.com/ws/robot';
let remoteWS = null;

function connectRemote() {
  remoteWS = new WebSocket(REMOTE_WS_URL);

  remoteWS.on('open', () => {
    console.log('Connected to Render WSS');
  });

  remoteWS.on('close', () => {
    console.log('Render WS closed, reconnecting...');
    setTimeout(connectRemote, 2000);
  });

  remoteWS.on('error', console.error);
}

connectRemote();

wss.on('connection', (client) => {
  console.log('Arduino connected');

  client.on('message', (data) => {
    const parsedData = JSON.parse(data)
    parsedData.data = parsedData.data
    console.log('From Arduino:', parsedData);

    if (remoteWS?.readyState === WebSocket.OPEN) {
      remoteWS.send(JSON.stringify(parsedData));
    }
  });

  client.on('close', () => {
    console.log('Arduino disconnected');
  });

});
