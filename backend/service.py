from helper import getSnowFlakeId
from model import Robot,select
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


def selectRobots():
    data =  db.session.scalars(select(Robot)).fetchall()
    resultList = []
    for robot in data:
        resultList.append({
            "id":robot.id,
            "robotName":robot.robotName,
            "robotCode":robot.robotCode
        })
    return Result.success(data=resultList,message="Success!")    