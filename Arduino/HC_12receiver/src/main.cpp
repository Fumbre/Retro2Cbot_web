#include <Arduino.h>
#include "wifi/Wificonnector.h"
#include "websocket/websocket.h"
#include "hc12/hc12recive.h"
#include <ArduinoJson.h>

// JsonDocument doc;

StaticJsonDocument<256> doc;

void buildReflectiveJson()
{
  doc.clear();

  doc["event"] = "rs";
  doc["method"] = "POST";

  JsonObject data = doc.createNestedObject("data");

  data["robotCode"] = "BB016";

  data["a0"] = random(0, 1024);
  data["a1"] = random(0, 1024);
  data["a2"] = random(0, 1024);
  data["a3"] = random(0, 1024);
  data["a4"] = random(0, 1024);
  data["a5"] = random(0, 1024);
  data["a6"] = random(0, 1024);
  data["a7"] = random(0, 1024);

  data["currentStatus"] = "10011001";
}

void setup()
{
  Serial.begin(9600);
  buildHC12Connection();
  connectWifi();
  connectWebsocket();
}

char buffer[256];

unsigned long lastSend = 0;

void loop()
{
  websocketLoop();

  if (millis() - lastSend > 1000)
  {
    lastSend = millis();

    buildReflectiveJson();

    serializeJson(doc, buffer);

    sendData(buffer);
  }

  // String data = receiveDataFromHC12();

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