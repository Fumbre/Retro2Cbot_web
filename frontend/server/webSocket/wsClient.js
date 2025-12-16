import WebSocket from 'ws';

let ws = null;

export function connectToRobotApi() {
	if (ws) return ws;

	ws = new WebSocket(`ws://${process.env.API_IP}:${process.env.API_PORT}/ws/robot`);

	ws.on('close', () => {
		console.log('WS closed, reconnecting...');
		ws = null;
		setTimeout(connectToPython, 2000);
	});

	ws.on('error', (err) => {
		console.error('WS error:', err);
	});

	return ws;
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
