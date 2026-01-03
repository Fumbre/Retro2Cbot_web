from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        """
        initialzie WebsocketConnectionManager instance
        
        :param self: WebsocketConnectionManager instance
        """
        self.active_connections: dict[str, list[WebSocket]] = {} # define a property, which name is active_connections. the data type is dict[], and content is empty.

    async def connect(self, websocket: WebSocket, topic: str):
        """
        build websocket connection
        
        :param self: WebsocketConnectionManager instance
        :param websocket: websocket client object
        :type websocket: WebSocket
        :param topic: websocket topic
        :type topic: str
        """
        # build websocket connection between server and client.
        await websocket.accept()
        # set values in active_connections property. 
        # eg: if this topic is exist, put this websocket client into the array, and the key is topic. 
        # if it is not exist, return an empty list.
        self.active_connections.setdefault(topic, []).append(websocket)

    def disconnect(self, websocket: WebSocket, topic: str):
        """
        Docstring for disconnect
        
        :param self: WebsocketConnectionManager instance
        :param websocket: websocket client object
        :type websocket: WebSocket
        :param topic: websocket topic
        :type topic: str
        """
        # remove current websocket client from current topic
        self.active_connections[topic].remove(websocket)

    async def send_message(self, message: dict, topic: str):
        """
        send messages to websocket client.
        
        :param self: WebsocketConnectionManager instance
        :param message: response data
        :type message: dict
        :param topic: websocket topic
        :type topic: str
        """
        for connection in self.active_connections.get(topic, []):
            await connection.send_json(message) # send json messages to websocket clients that is in this topic.