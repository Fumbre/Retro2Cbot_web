from database import app,SessionLocal
from fastapi import FastAPI,Request,WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from WebsocketManager import WebsocketConnectionManager
import uvicorn
from service import (
    insertRobots,
    selectRobots,
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
import os

# load value of configurations from .env file
load_dotenv()

# Set to hold connected clients
clients = set()

#create websocket manager
manager = WebsocketConnectionManager()

@app.post("/robots")
async def insertRobot(request:Request):
    """
   insert robot information into database
    
    :param request: http request
    :type request: Request
    """
    params = await request.json() if hasattr(request, "json") else {}
    return insertRobots(request=request,robotName=params.get("robotName"),robotCode=params.get("robotCode"))


@app.get("/robots")
def robotList(request:Request):
    """
    get robots inforamtion
    
    :param request: http request
    :type request: Request
    """
    return selectRobots(request=request)

# @app.get("/robot/{robot_id}/{event}")
# def robot_sensor_list(
#     robot_id: str,
#     event: Literal["sonar", "reflective"]
# ):

@app.get("/robot/BB016/sonar")
def robotSonarList(request:Request):
   db = SessionLocal()

   robotCode = "BB016"
   event = "sonar"

   result = selectSonarList(db=db, robotCode=robotCode)

   myResult = {
      **result,
      "event": event
   }
   
   return myResult


@app.websocket("/ws/robot")
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

        


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    # Uvicorn is a async web service framework. it can support normal and async Http request and websockets
    uvicorn.run("app:app", host=SERVER_IP, port=SERVER_PORT, reload=True)