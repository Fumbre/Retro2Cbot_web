import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';


export function getReflectiveData() {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            event: "rs",
            method: "GET",
            robotCode: "BB016"
        }));
    }

    // ws.send(JSON.stringify({ test: "test" }))
}
