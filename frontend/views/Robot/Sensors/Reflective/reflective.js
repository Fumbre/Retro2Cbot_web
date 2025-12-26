import './reflective.sass'
import { ws } from '../../../../assets/scripts/main.js';


export function getReflectiveData() {
    ws.onopen = () => {
        ws.send(JSON.stringify({ type: 'hello' }));
    };
}
