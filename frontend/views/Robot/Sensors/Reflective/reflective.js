import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';
import { ROBOTS, isRobot } from '../../../../assets/scripts/constants.js';
import wsBus from '../../../../assets/scripts/wsBus.js';

export function getReflectiveData(robotId) {
    if (!isRobot(robotId))
        return;

    if (ws.readyState === WebSocket.OPEN) {
        wsBus.on('rs', (data) => {
            const dataParsed = JSON.parse(data)
            console.log("ws bus got rs data", dataParsed)
            // updateReflectiveSensors(data);
        })
        // ws.send(JSON.stringify({
        //     event: "rs",
        //     method: "GET",
        //     robotCode: robotId
        // }));
    }

    // ws.send(JSON.stringify({ test: "test" }))
}



function updateReflectiveSensors(data) {

}