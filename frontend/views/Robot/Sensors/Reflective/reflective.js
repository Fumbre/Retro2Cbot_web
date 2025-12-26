import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';
import { ROBOTS, isRobot } from '../../../../assets/scripts/constants.js';

export function getReflectiveData(robotId) {
    if (!isRobot(robotId))
        return;

    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            event: "rs",
            method: "GET",
            robotCode: robotId
        }));
    }

    // ws.send(JSON.stringify({ test: "test" }))
}
