import WebSocket from 'ws';
import bus from './bus.js';


export let wsApi = null;
let intervalId = null;

export function connectToRobotApi() {
	if (wsApi) return wsApi;

	wsApi = new WebSocket(`ws://${process.env.API_IP}:${process.env.API_PORT}/ws/robot`);

	wsApi.on("open", () => {
		console.log("im here")
		if (intervalId != null) {
			clearInterval(intervalId);
		}
	})

	wsApi.on('message', function message(data) {
		const dataParsed = JSON.parse(data);
		console.log("I got from python", dataParsed);

		bus.emit('apiResponse', JSON.stringify(dataParsed));
	})


	wsApi.on('close', () => {
		console.log('WS closed, reconnecting...');
		wsApi = null;

		// clear interval
		if (intervalId != null) {
			clearInterval(intervalId);
		}

		intervalId = setInterval(connectToRobotApi, 2000);
	});

	wsApi.on('error', (err) => {
		console.error('WS error:', err);
	});

	return wsApi;
}

// ws.on('error', console.error);

// ws.on('open', () => {
// 	const data = JSON.stringify({
// 		"event": 'gripper',
// 		"method": 'GET',
// 		"robotCode": "BB016"
// 	});

// 	ws.send(data);
// });

// ws.on('message', (data) => {
// 	console.log(JSON.parse(data))
// });
