#include "websocket.h"

WebSocketsClient websocketClient;
// char *serverIP = "192.168.137.1";
char *serverIP = "192.168.137.148";

int port = 8081;
char *url = "/ws";
bool wsConnected = false;

bool connectWebsocket()
{
    websocketClient.begin(serverIP, port, url);
    websocketClient.onEvent(webSocketEvent);
    websocketClient.setReconnectInterval(2000);
    return wsConnected;
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length)
{
    switch (type)
    {
    case WStype_CONNECTED:
        wsConnected = true;
        Serial.println("WebSocket CONNECTED");
        break;

    case WStype_DISCONNECTED:
        wsConnected = false;
        Serial.println("WebSocket DISCONNECTED");
        break;
    }
}

void websocketLoop()
{
    websocketClient.loop();
}

void sendData(String data)
{
    if (data.isEmpty())
        return;
    websocketClient.sendTXT(data);
}