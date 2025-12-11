from database import app
from flask import request
from dotenv import load_dotenv
from service import insertRobots,selectRobots,selectReflectSensorList,insertReflectiveSensors
import os
from flask_socketio import SocketIO,emit

load_dotenv()

socketIO = SocketIO(app,async_mode="eventlet",cors_allowed_origins="*")

@app.route("/robots",methods = ["POST"])
def insertRobot():
    params = request.get_json()
    return insertRobots(params["robotName"],params["robotCode"])

@app.route("/robots",methods = ["GET"])
def robotList():
    return selectRobots()


@app.route("/rs",methods = ["POST"])
def insertRS():
    list = request.get_json()
    print(list)
    return insertReflectiveSensors(list)

@socketIO.on('RS')
def reflectiveSensorList(msg):
    robotId = int(msg.get("robotId"))
    emit("RS",selectReflectSensorList(robotId=robotId))


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    socketIO.run(app,host=SERVER_IP,port=SERVER_PORT,debug=True)