import './reflective.sass'


export async function getReflectiveData() {
    const ws = new WebSocket('ws://localhost:3000/ws');

    ws.onmessage = (e) => {
        console.log('got it: ', e.data);
    };
}
