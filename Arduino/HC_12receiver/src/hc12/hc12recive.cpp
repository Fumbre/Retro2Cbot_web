#include "hc12recive.h"

#define HC12_RX 0
#define HC12_TX 1

SoftwareSerial hc12(HC12_RX, HC12_TX);

void buildHC12Connection()
{
    hc12.begin(9600);
}

String receiveDataFromHC12()
{
    String data = "";
    if (hc12.available())
    {
        data = hc12.readStringUntil('\n');
    }
    return data;
}