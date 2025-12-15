#include <WebSocketsClient.h>

bool connectWebsocket();
void webSocketEvent(WStype_t type, uint8_t* payload, size_t length);
void websocketLoop();
void sendData(String data);