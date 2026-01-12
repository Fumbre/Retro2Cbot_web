const WebSocket = require('ws');

const wss = new WebSocket.Server({
  port: 8081,
  path: '/ws'
});

const REMOTE_WS_URL = 'wss://retro2cbot-web-dugz.onrender.com/ws/robot';
const REMOTE_WS_FRONT_URL = 'wss://retro2cbot-web.onrender.com/ws?password=36asgdv246sdgvf237uy5sdgb5';
let remoteWS = null;
let remoteFrontWS = null;
try {

  // send data to database
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

  //send data to frontend
  function connectRemoteFront() {
    remoteFrontWS = new WebSocket(REMOTE_WS_FRONT_URL);

    remoteFrontWS.on('open', () => {
      console.log('Connected to Render FRONT WSS');
    });

    remoteFrontWS.on('close', () => {
      console.log('Render FRONT WS closed, reconnecting...');
      setTimeout(connectRemoteFront, 2000);
    });

    remoteFrontWS.on('error', console.error);
  }

  connectRemote();
  connectRemoteFront();

  wss.on('connection', (client) => {
    console.log('Arduino connected');

    client.on('message', (data, isBinary) => {
      try {
        const text = isBinary ? data.toString('utf8') : data;
        const parsedData = JSON.parse(text);

        console.log('From Arduino:', parsedData);

        if (remoteWS) sendIfOpen(remoteWS, parsedData);
        if (remoteFrontWS) sendIfOpen(remoteFrontWS, parsedData);

      } catch (e) {
        console.error('Invalid message from Arduino:', e);
      }
    });

    client.on('close', () => {
      console.log('Arduino disconnected');
    });

  });

  function sendIfOpen(ws, data) {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data));
    }
  }

} catch (e) {
  return e
}