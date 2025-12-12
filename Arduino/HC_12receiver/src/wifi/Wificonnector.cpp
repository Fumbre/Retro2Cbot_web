#include "Wificonnector.h"

const char* ssid = "weatherStation";
const char* password = "Whszxc1223??";

int count  = 0;

void connectWifi(){
    Serial.print("try to connect Wi-Fi: ");
    Serial.println(ssid);
    WiFi.begin(ssid,password);

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        count++;
        delay(500);
        if(count >= 2000){
            Serial.println("Wifi connected failed!!");
            return;
        }
    }

    Serial.println("");
    Serial.println("WIFI connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
}