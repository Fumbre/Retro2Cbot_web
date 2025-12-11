from database import app
from flask import request
from dotenv import load_dotenv
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
    selectNeopixelList
)
import os
from flask_socketio import SocketIO, emit

load_dotenv()

socketIO = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")


@app.route("/robots", methods=["POST"])
def insertRobot():
    params = request.get_json()
    return insertRobots(params["robotName"], params["robotCode"])


@app.route("/robots", methods=["GET"])
def robotList():
    return selectRobots()


@app.route("/rs", methods=["POST"])
def insertRS():
    list = request.get_json()
    return insertReflectiveSensors(list)


@socketIO.on("rs")
def reflectiveSensorList(msg):
    robotId = int(msg.get("robotId"))
    emit("rs", selectReflectSensorList(robotId))


@app.route("/sonar", methods=["POST"])
def insertSonars():
    params = request.get_json()
    return insertRobotSonarData(params)


@socketIO.on("sonar")
def sonarList(msg):
    robotId = int(msg.get("robotId"))
    emit("sonar", selectSonarList(robotId))


@app.route("/pulses", methods=["POST"])
def insertPulsesList():
    params = request.get_json()
    return insertRobotPulses(params)

@socketIO.on('pulses')
def selectPulses(msg):
    robotId = int(msg.get("robotId"))
    emit("pulses",selectPulsesList(robotId))

@app.route("/neopixels", methods=["POST"])
def insertNeopixelList():
    params = request.get_json()
    return insertNeopixels(params)

@socketIO.on('neopixels')
def selectNeopixels(msg):
    robotId = int(msg.get("robotId"))
    emit("neopixels",selectNeopixelList(robotId))

if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    socketIO.run(app, host=SERVER_IP, port=SERVER_PORT, debug=True)
