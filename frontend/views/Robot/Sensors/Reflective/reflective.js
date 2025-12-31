import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';
import { ROBOTS, isRobot } from '../../../../assets/scripts/constants.js';
import wsBus from '../../../../assets/scripts/wsBus.js';

let currentRobot;

export function getReflectiveData() {
    // if (!isRobot(robotId))
    //     return;

    console.log('reflect?')

    if (ws.readyState === WebSocket.OPEN) {
        wsBus.on('rs', (data) => {
            const dataParsed = JSON.parse(data)
            console.log("ws bus got rs data", dataParsed)
            updateReflectiveSensors(dataParsed.data);
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
    const rsData = data[0];
    const rsList = document.getElementById(`rsList__${rsData.robotCode}`);

    // console.log(rsList);

    for (let index = 0; index < rsList.childElementCount; index++) {
        const item = rsList.querySelector(`[data-sensor="reflective_sensor__a${index}"]`)
        const valueEl = item.querySelector('.reflective_sensor__value');

        valueEl.textContent = rsData[`a${index}`];

        valueEl.classList.remove('reflective_sensor__line_status0');
        valueEl.classList.remove('reflective_sensor__line_status1');
        valueEl.classList.add(`reflective_sensor__line_status${rsData.currentStatus.slice(index, index + 1)}`);

        console.log(item);

    }



}