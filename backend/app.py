from database import app
from flask import request
from dotenv import load_dotenv
from service import insertRobots
import os

load_dotenv()

@app.route("/insertRobots",methods = ["POST"])
def insertRobot():
    params = request.get_json()
    return insertRobots(params["robotName"],params["robotCode"])


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    app.run(host=SERVER_IP,port=SERVER_PORT,debug=True)