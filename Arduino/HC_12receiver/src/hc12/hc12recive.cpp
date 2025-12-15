#include "hc12recive.h"


#define HC12_RX 0
#define HC12_TX 1

SoftwareSerial serial(HC12_RX,HC12_TX);

String receiveData(){
    String data;
    if (serial.available())
    {
       data =  serial.readStringUntil('/n');
    }
    return data;
}