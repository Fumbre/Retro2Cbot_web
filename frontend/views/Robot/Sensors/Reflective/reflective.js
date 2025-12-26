import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';


export function getReflectiveData() {
    ws.onopen = () => {
        ws.send(JSON.stringify({ type: 'hello' }));
    };

    ws.onopen = () => {
        const data = {
            robotCode: "BB016",
            method: "GET",
            event: "gripper"
        }

        ws.send(JSON.stringify(data))
    }


}
