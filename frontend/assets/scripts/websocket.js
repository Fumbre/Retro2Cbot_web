import wsBus from "./wsBus.js";

let ws;
let timeout;

export function nodeWebsocket() {
  if (!ws || ws.readyState === WebSocket.CLOSED) {
    ws = new WebSocket('ws://localhost:3000/ws');

    ws.onmessage = (e) => {
      console.log('got it: ', JSON.parse(e.data));
    };

    ws.onclose = (e) => {
      console.log('WS closed, reconnecting...');
      ws = null;

      // clear interval
      if (timeout != null) {
        clearTimeout(timeout);
      }

      timeout = setTimeout(() => {
        nodeWebsocket();
      }, 2000);
    }
  }

  return ws;
}
