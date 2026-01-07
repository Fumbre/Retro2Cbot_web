from fastapi import APIRouter,WebSocket,WebSocketDisconnect
from WebsocketManager import WebsocketConnectionManager
from database import SessionLocal
from service import (
    selectReflectSensorList,
    insertReflectiveSensors,
    insertRobotSonarData,
    selectSonarList,
    insertRobotPulses,
    selectPulsesList,
    insertNeopixels,
    selectNeopixelList,
    insertGripperList,
    selectCurrentGripper
)

router = APIRouter()

# Set to hold connected clients
clients = set()

#create websocket manager
manager = WebsocketConnectionManager()

@router.websocket("/ws/robot")
async def websocket_endpoint(websocket: WebSocket):
    """
    websocket request
    It depends on different events, it selects differnt data or insert different data.
    :param websocket: websocket client
    :type websocket: WebSocket
    """
    clients.add(websocket)
    db = SessionLocal()
    await manager.connect(websocket, "robot") # build connection between server and clients
    try:
     while True:
        data = await websocket.receive_json()
        print(data)
        method = data.get("method")
        if method == "GET": # select differnt data
            robotCode = data.get("robotCode") # get robot code
            event = data.get("event") # get event name
            if event == "rs": # reflective sensor
              result = selectReflectSensorList(db=db, robotCode=robotCode)
              myResult = {
                 **result,
                 "event": event
              }
            elif event == "sonar": # sonar
              result = selectSonarList(db=db, robotCode=robotCode)
              myResult = {
                 **result,
                 "event": event
              }
            elif event == "pulses": # pulses
              result = selectPulsesList(db=db, robotCode=robotCode)
              myResult = {
                 **result,
                 "event": event
              }
            elif event == "neopixels": # leds
              result = selectNeopixelList(db=db, robotCode=robotCode)
              myResult = {
                 **result,
                 "event": event
              }
            elif event == "gripper": # gripper
              result = selectCurrentGripper(db=db, robotCode=robotCode)
              myResult = {
                 **result,
                 "event": event
              }
            else:
              result = {"error": "unknown event"}
            await websocket.send_json(myResult)

        if method == "POST" : # insert data.
           event = data.get("event")
           data_list = list(data.get("data"))

           for client in clients.copy():
             try:
               await client.send_json(data)
             except websocket.ConnectionClosed:
               clients.remove(client)  

           if event == "rs":
              result = insertReflectiveSensors(db=db, sensor_list=data_list)
           elif event == "sonar":
              result = insertRobotSonarData(db=db, list=data_list)
           elif event == "pulses":
              result = insertRobotPulses(db=db, list=data_list)
           elif event == "neopixels":
              result = insertNeopixels(db=db, data_list=data_list)
           elif event == "gripper":
              result = insertGripperList(db=db, data_list=data_list)
           else:
              result = {"error": "unknown event"}

      
           
         #   await websocket.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket,topic="robot")
    finally:
        db.close()    
        clients.remove(websocket)
