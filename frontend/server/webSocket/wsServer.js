import { WebSocketServer } from 'ws';
import { wsApi } from "./wsClient.js"
import bus from './bus.js';

export const clients = new Map();

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

    ws.on('message', function message(data) {
      const dataParsed = JSON.parse(data)
      console.log("frontend data:", dataParsed);
      // wsApi.send(JSON.stringify(dataParsed));
    });

    ws.send(JSON.stringify({ ping: 'connected for first time' }));
  });

  bus.on('apiResponse', (data) => {
    const dataParsed = JSON.parse(data)
    console.log("node.js send data to front: ", dataParsed)
    wss.clients.forEach(ws => ws.send(JSON.stringify(dataParsed)));
  });
}



