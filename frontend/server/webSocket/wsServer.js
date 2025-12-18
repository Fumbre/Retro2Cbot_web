import { WebSocketServer } from 'ws';
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
      console.log('received: %s', data);
    });

    ws.send('something');
  });

  bus.on('sensors', (data) => {
    wss.clients.forEach(ws => ws.send(data));
  });
}



