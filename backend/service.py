from helper import getSnowFlakeId
from model import Robot
from database import db
from response import Result

def insertRobots(robotName:str,robotCode:str):
    id = getSnowFlakeId()
    robot = Robot(
        id = id,
        robotName = robotName,
        robotCode = robotCode
    )
    db.session.add(robot)
    db.session.commit()
    return Result.success(message="insert Success!")
