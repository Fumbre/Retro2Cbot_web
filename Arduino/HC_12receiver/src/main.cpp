#include <Arduino.h>
#include "wifi/Wificonnector.h"
#include "websocket/websocket.h"
#include "hc12/hc12recive.h"
#include "dataservice/data.h"

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
  if (!data.isEmpty())
  {
    String newData = dealwithData(data);
    if (data.length() != 0)
    {
      Serial.println(newData);
      sendData(newData);
    }
  }
}