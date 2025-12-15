#include <Arduino.h>
#include "wifi/Wificonnector.h"
#include "websocket/websocket.h"

unsigned long lastTime = 0;

void setup()
{
  Serial.begin(9600);
  connectWifi();
  connectWebsocket();
}

void loop()
{
  websocketLoop();
  unsigned long now = millis();
  if (now - lastTime >= 2000)
  {
    String data = "{\"method\":\"POST\",\"event\":\"gripper\",\"data\":[{\"robotCode\":\"BB016\",\"gripperStatus\":true}]}";
    sendData(data);
    lastTime = now;
  }
}