from helper import getSnowFlakeId, dict_orm, orm_dict
from model import Robot, ReflectiveSensor, RobotSonar, select, and_
from database import db
from response import Result
from datetime import date, timedelta


def insertRobots(robotName: str, robotCode: str):
    try:
        id = getSnowFlakeId()
        robot = Robot(id=id, robotName=robotName, robotCode=robotCode)
        db.session.add(robot)
        db.session.commit()
        return Result.success(message="insert Success!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=str(e))


def selectRobots():
    data = db.session.scalars(select(Robot)).fetchall()
    resultList = []
    for robot in data:
        resultList.append(
            {"id": robot.id, "robotName": robot.robotName, "robotCode": robot.robotCode}
        )
    return Result.success(data=resultList, message="Success!")


def insertReflectiveSensors(sensor_list: list[dict]):
    try:
        sensors = []
        for sensor in sensor_list:
            id = getSnowFlakeId()
            rs = ReflectiveSensor(id=id)
            dict_orm(sensor, rs)
            sensors.append(rs)
        db.session.add_all(sensors)
        db.session.commit()
        return Result.success(message="insert sucess!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)


def selectReflectSensorList(robotId: int):
    startDate = date.today()
    endDate = startDate + timedelta(days=1)
    dataList = db.session.scalars(
        select(ReflectiveSensor).where(
            and_(
                ReflectiveSensor.robotId == robotId,
                ReflectiveSensor.create_time >= startDate,
                ReflectiveSensor < endDate,
            )
        )
    ).fetchall()
    resultList = []
    for reflectiveSensor in dataList:
        re = orm_dict(reflectiveSensor)
        resultList.append(re)
    return Result.success_ws(data=resultList, message="select successfully!")


def insertRobotSonarData(list: list[dict]):
    try:
        sonars = []
        for sonar in list:
            id = getSnowFlakeId()
            data = RobotSonar(id=id)
            dict_orm(sonar, data)
            sonars.append(data)
        db.session.add_all(data)
        db.session.commit()
        return Result.success(message="insert success!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)


def selectSonarList(robotId: int):
    sonarList = []
    startDate = date.today()
    endDate = startDate + timedelta(days=1)
    list = db.session.scalars(
        select(RobotSonar).where(
            and_(
                RobotSonar.robotId == robotId,
                RobotSonar.createTime >= startDate,
                RobotSonar.createTime < endDate,
            )
        )
    ).fetchall()

    for sonar in list:
        data = orm_dict(sonar)
        sonarList.append(data)
    return Result.success_ws(data=sonarList,message="select success!")