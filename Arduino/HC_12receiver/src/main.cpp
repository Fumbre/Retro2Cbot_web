#include <Arduino.h>
#include "wifi/Wificonnector.h"
#include "websocket/websocket.h"
#include "hc12/hc12recive.h"
#include <ArduinoJson.h>

JsonDocument doc;

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
  // if(!data.isEmpty()){
  //   Serial.println(data);
  //   //deal with data
  //   deserializeJson(doc,data);
  //   if(doc["type"] == "outside"){
  //     doc.remove("type");
  //     String newData;
  //     serializeJson(doc,newData);
  //     sendData(newData);
  //   }
  // }
}