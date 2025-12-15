from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, topic: str):
        await websocket.accept()
        self.active_connections.setdefault(topic, []).append(websocket)

    def disconnect(self, websocket: WebSocket, topic: str):
        self.active_connections[topic].remove(websocket)

    async def send_message(self, message: dict, topic: str):
        for connection in self.active_connections.get(topic, []):
            await connection.send_json(message)