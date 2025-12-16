#include <Arduino.h>
#include "wifi/Wificonnector.h"
#include "websocket/websocket.h"
#include "hc12/hc12recive.h"


void setup()
{
  Serial.begin(9600);
  buildHC12Connection();
  connectWifi();
  connectWebsocket();
}

void loop()
{
  websocketLoop();
  String data = receiveDataFromHC12();
  if(!data.isEmpty()){
    Serial.println(data);
    sendData(data);
  }
}