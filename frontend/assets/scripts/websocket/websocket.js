import wsBus from "./wsBus.js";

export let ws;
let timeout;

export function nodeWebsocket() {
  if (!ws || ws.readyState === WebSocket.CLOSED) {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";

    ws = new WebSocket(`${protocol}://${window.location.host}/ws`);

    ws.onmessage = (e) => {
      const dataParsed = JSON.parse(e.data)
      console.log('got it: ', dataParsed);
      wsBus.emit(`${dataParsed.event}`, JSON.stringify(dataParsed))
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
