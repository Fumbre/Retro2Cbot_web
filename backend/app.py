from database import app,SessionLocal
from fastapi import FastAPI,Request,WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from WebsocketManager import WebsocketConnectionManager
import uvicorn
from service import (
    insertRobots,
    selectRobots,
    insertReflectiveSensors,
    insertRobotSonarData,
    insertRobotPulses,
    insertNeopixels,
    insertGripperList,
    push_data_loop
)
import os
import asyncio

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
    push_task = None
    try:
     while True:
        data = await websocket.receive_json()
        method = data.get("method")
        if method == "GET":
            robotCode = data.get("robotCode")
            event = data.get("event")
            if push_task:
               push_task.cancel()

            push_task = asyncio.create_task(push_data_loop(websocket=websocket,db_factory=SessionLocal,robotCode=robotCode,event=event)) 
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
        if push_task:
         push_task.cancel() 
         try:
            await push_task
         except asyncio.CancelledError:
            print("Push task fully stopped")
    finally:
        db.close()    
        



if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    uvicorn.run("app:app", host=SERVER_IP, port=SERVER_PORT, reload=True)