import { WebSocketServer } from 'ws';
import { wsApi } from "./wsClient.js"
import bus from './bus.js';

export const clients = new Map();
let apiSubscribed = false;

export function initWSS(server) {

  const wss = new WebSocketServer({ server, path: '/ws' });

  wss.on('connection', (ws, req) => {
    // todo:
    // jwt
    // const sessionId = req.headers['x-session-id'];

    // if (!sessionId) {
    //   ws.close(1008, "Unauthorized"); // 1008 code for ws connection "Policy Violation"
    //   return;
    // }

    // clients.set(sessionId, ws);

    ws.on('error', console.error);

    // only clients with key can send data
    if (req.url === "/ws?password=36asgdv246sdgvf237uy5sdgb5") {
      ws.on('message', function message(data) {
        const dataParsed = JSON.parse(data)
        console.log("Arduino send data:", dataParsed);
        bus.emit('apiResponse', JSON.stringify(dataParsed));
      });
    }


    ws.send(JSON.stringify({ ping: 'connected for first time' }));
  });

  if (!apiSubscribed) {
    apiSubscribed = true;

    bus.on('apiResponse', (data) => {
      const dataParsed = JSON.parse(data);
      console.log("node.js send data to front:", dataParsed);

      wss.clients.forEach(ws => {
        if (ws.readyState === ws.OPEN) {
          ws.send(JSON.stringify(dataParsed));
        }
      });
    });
  }

}



