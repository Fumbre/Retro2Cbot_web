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

load_dotenv()

manager = WebsocketConnectionManager()

@app.post("/robots")
async def insertRobot(request:Request):
    params = await request.json() if hasattr(request, "json") else {}
    return insertRobots(request=request,robotName=params.get("robotName"),robotCode=params.get("robotCode"))


@app.get("/robots")
def robotList(request:Request):
    return selectRobots(request=request)


@app.websocket("/ws/robot")
async def websocket_endpoint(websocket: WebSocket):
    db = SessionLocal()
    await manager.connect(websocket, "robot")
    try:
     while True:
        data = await websocket.receive_json()
        print(data)
        method = data.get("method")
        if method == "GET":
            robotCode = data.get("robotCode")
            event = data.get("event")
            if event == "rs":
              result = selectReflectSensorList(db=db, robotCode=robotCode)
            elif event == "sonar":
              result = selectSonarList(db=db, robotCode=robotCode)
            elif event == "pulses":
              result = selectPulsesList(db=db, robotCode=robotCode)
            elif event == "neopixels":
              result = selectNeopixelList(db=db, robotCode=robotCode)
            elif event == "gripper":
              result = selectCurrentGripper(db=db, robotCode=robotCode)
            else:
              result = {"error": "unknown event"}
            await websocket.send_json(result)
        else:
           event = data.get("event")
           data_list = list(data.get("data"))
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
           await websocket.send_json(result)          
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket,topic="robot")
    finally:
        db.close()    
        


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    uvicorn.run("app:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
