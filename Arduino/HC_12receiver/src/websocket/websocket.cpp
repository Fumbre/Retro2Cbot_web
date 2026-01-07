#include "websocket.h"

WebSocketsClient websocketClient;
char *serverIP = "https://retro2cbot-web-dugz.onrender.com";
int port = 8080;
char *url = "/ws/robot";
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