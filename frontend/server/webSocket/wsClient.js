import WebSocket from 'ws';

export let wsApi = null;
let intervalId = null;

export function connectToRobotApi() {
	if (wsApi) return wsApi;

	wsApi = new WebSocket(`ws://${process.env.API_IP}:${process.env.API_PORT}/ws/robot`);

	wsApi.on("open", () => {
		if (intervalId != null) {
			clearInterval(intervalId);
		}
	})

	wsApi.on('message', function message(data) {
		console.log("where: is data?: %s", data);
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
