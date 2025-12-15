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


@app.post("/rs")
async def insertRS(request:Request):
    list  = await request.json() if hasattr(request, "json") else []
    return insertReflectiveSensors(request=request, list = list)


@app.post("/sonar")
async def insertSonars(request:Request):
    list = await request.json() if hasattr(request, "json") else []
    return insertRobotSonarData(request=request,list=list)


@app.post("/pulses")
async def insertPulsesList(request:Request):
    list = await request.json() if hasattr(request, "json") else []
    return insertRobotPulses(request=request,list=list)


@app.post("/neopixels")
async def insertNeopixelList(request:Request):
    list = await request.json() if hasattr(request, "json") else []
    return insertNeopixels(request=request,data_list=list)


@app.post("/gripper")
async def insertGrippers(request:Request):
    list = await request.json() if hasattr(request, "json") else []
    return insertGripperList(request=request,data_list=list)

@app.websocket("/ws/robot")
async def websocket_endpoint(websocket: WebSocket):
    db = SessionLocal()
    await manager.connect(websocket, "robot")
    try:
     while True:
        data = await websocket.receive_json()
        robotId = int(data.get("robotId"))
        event = data.get("event")
        if event == "rs":
            result = selectReflectSensorList(request=None, robotId=robotId)
        elif event == "sonar":
            result = selectSonarList(db=db, robotId=robotId)
        elif event == "pulses":
            result = selectPulsesList(db=db, robotId=robotId)
        elif event == "neopixels":
            result = selectNeopixelList(db=db, robotId=robotId)
        elif event == "gripper":
            result = selectCurrentGripper(db=db, robotId=robotId)
        else:
            result = {"error": "unknown topic"}
        await websocket.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket,topic="robot")
    finally:
        db.close()    
        


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    uvicorn.run("app:app", host=SERVER_IP, port=SERVER_PORT, reload=True)
