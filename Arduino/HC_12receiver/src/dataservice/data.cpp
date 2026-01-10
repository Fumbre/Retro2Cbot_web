#include "data.h"

JsonDocument doc;

StringSplitter splitter;

String dealwithData(String data)
{
    doc.clear();
    splitter.split(data, ',');
    if (splitter.get(0) != "o")
    {
        return "";
    }
    doc["method"] = "POST";
    if (splitter.get(1) == "rs")
    {
        doc["event"] = "rs";
        JsonArray data = doc.createNestedArray("data");
        JsonObject rs = data.createNestedObject();
        rs["robotCode"] = "BB0" + splitter.get(2);
        for (int i = 3; i <= 10; i++)
        {
            char buffer[3];
            snprintf(buffer, sizeof(buffer), "a%d", i - 3);
            rs[buffer] = splitter.get(i).toInt();
        }

        String status = splitter.get(splitter.size() - 1);
        status.trim();
        rs["currentStatus"] = status;
    }
    else if (splitter.get(1) == "so")
    {
        doc["event"] = "sonar";
        String robotCode = "BB0" + splitter.get(2);
        JsonArray data = doc.createNestedArray("data");
        JsonObject frontSonar = data.createNestedObject();
        frontSonar["robotCode"] = robotCode;
        frontSonar["direction"] = splitter.get(3);
        frontSonar["sonarDistance"] = splitter.get(4).toFloat();
        JsonObject rightSonar = data.createNestedObject();
        rightSonar["robotCode"] = robotCode;
        rightSonar["direction"] = splitter.get(5);
        rightSonar["sonarDistance"] = splitter.get(6).toFloat();
        JsonObject leftSonar = data.createNestedObject();
        leftSonar["robotCode"] = robotCode;
        leftSonar["direction"] = splitter.get(7);
        leftSonar["sonarDistance"] = splitter.get(8).toFloat();
    }
    else if (splitter.get(1) == "n")
    {
        doc["event"] = "neopixels";
        String robotCode = "BB0" + splitter.get(2);
        JsonArray data = doc.createNestedArray("data");
        JsonObject neopixel0 = data.createNestedObject();
        neopixel0["robotCode"] = robotCode;
        neopixel0["neopixelIndex"] = splitter.get(3).toInt();
        neopixel0["r"] = splitter.get(4).toInt();
        neopixel0["g"] = splitter.get(5).toInt();
        neopixel0["b"] = splitter.get(6).toInt();
        JsonObject neopixel1 = data.createNestedObject();
        neopixel1["robotCode"] = robotCode;
        neopixel1["neopixelIndex"] = splitter.get(7).toInt();
        neopixel1["r"] = splitter.get(8).toInt();
        neopixel1["g"] = splitter.get(9).toInt();
        neopixel1["b"] = splitter.get(10).toInt();
        JsonObject neopixel2 = data.createNestedObject();
        neopixel2["robotCode"] = robotCode;
        neopixel2["neopixelIndex"] = splitter.get(11).toInt();
        neopixel2["r"] = splitter.get(12).toInt();
        neopixel2["g"] = splitter.get(13).toInt();
        neopixel2["b"] = splitter.get(14).toInt();
        JsonObject neopixel3 = data.createNestedObject();
        neopixel3["robotCode"] = robotCode;
        neopixel3["neopixelIndex"] = splitter.get(15).toInt();
        neopixel3["r"] = splitter.get(16).toInt();
        neopixel3["g"] = splitter.get(17).toInt();
        neopixel3["b"] = splitter.get(18).toInt();
    }
    else if (splitter.get(1) == "g")
    {
        doc["event"] = "gripper";
        String robotCode = "BB0" + splitter.get(2);
        JsonArray data = doc.createNestedArray("data");
        JsonObject gripper = data.createNestedObject();
        gripper["robotCode"] = robotCode;
        if (splitter.get(3) == "0")
        {
            gripper["gripperStatus"] = false;
        }
        else
        {
            gripper["gripperStatus"] = true;
        }
    }
    String outcome;
    serializeJson(doc, outcome);
    return outcome;
}