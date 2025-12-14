from helper import getSnowFlakeId, dict_orm, orm_dict
from model import (
    Robot,
    ReflectiveSensor,
    RobotSonar,
    RobotPulses,
    RobotNeopxiel,
    select,
    and_,
)
from database import db
from response import Result
from datetime import date, timedelta,datetime


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
            {"id": str(robot.id), "robotName": robot.robotName, "robotCode": robot.robotCode}
        )
    return Result.success(data=resultList, message="Success!")


def insertReflectiveSensors(sensor_list: list[dict]):
    try:
        if sensor_list is None or len(sensor_list) == 0:
            return Result.error(message="data input is empty")
        robotCode = sensor_list[0].get("robotCode")
        robot = db.session.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        sensors = []
        for sensor in sensor_list:
            id = getSnowFlakeId()
            rs = ReflectiveSensor(id=id, robotId=robot.id)
            dict_orm(sensor, rs)
            sensors.append(rs)
        db.session.add_all(sensors)
        db.session.commit()
        return Result.success(message="insert sucess!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)


def selectReflectSensorList(robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = db.session.scalars(
        select(ReflectiveSensor).where(
            and_(
                ReflectiveSensor.robotId == robotId,
                ReflectiveSensor.createTime >= startDate,
                ReflectiveSensor.createTime < endDate,
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
        if list is None or len(list) == 0:
            return Result.error(message="data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.session.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        sonars = []
        for sonar in list:
            id = getSnowFlakeId()
            data = RobotSonar(id=id, robotId=robot.id)
            dict_orm(sonar, data)
            sonars.append(data)
        db.session.add_all(sonars)
        db.session.commit()
        return Result.success(message="insert success!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)


def selectSonarList(robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    endDate = startDate + timedelta(days=1)
    sonarList = []
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
    return Result.success_ws(data=sonarList, message="select success!")


def insertRobotPulses(list: list[dict]):
    try:
        if list is None or len(list) == 0:
            return Result.error("data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.session.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        pulsesList = []
        for data in list:
            id = getSnowFlakeId()
            pulses = RobotPulses(id=id, robotId=robot.id)
            dict_orm(data, pulses)
            pulsesList.append(pulses)
        db.session.add_all(pulsesList)
        db.session.commit()
        return Result.success(message="insert successfully!")
    except Exception as e:
        db.session().rollback()
        return Result.error(message=e)


def selectPulsesList(robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = []
    result = db.session.scalars(
        select(RobotPulses).where(
            and_(
                RobotPulses.createTime >= startDate,
                RobotPulses.createTime < endDate,
                RobotPulses.robotId == robotId,
            )
        )
    ).fetchall()

    for data in result:
        pulse = orm_dict(data)
        dataList.append(pulse)
    return Result.success_ws(data=dataList, message="select successfully!")

def insertNeopixels(data_list:list[dict]):
    try:
        if data_list is None or len(data_list) == 0:
            return Result.error(message="data input is Empty")
        print(data_list)
        neopexielList = []
        robotCode = data_list[0].get("robotCode")
        robot = db.session.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        for data in data_list:
            id = getSnowFlakeId()
            neopixel = RobotNeopxiel(id = id, robotId = robot.id)
            dict_orm(data,neopixel)
            neopexielList.append(neopixel)    
        db.session.add_all(neopexielList) 
        db.session.commit()
        return Result.success(message="insert successfully!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)

def selectNeopixelList(robotId:int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = []
    result = db.session.scalars(select(RobotNeopxiel).where(
        and_(
            RobotNeopxiel.createTime >= startDate,
            RobotNeopxiel.createTime < endDate,
            RobotNeopxiel.robotId == robotId
        )
    )).fetchall()
    for data in result:
        neopixel = orm_dict(data)
        dataList.append(neopixel)
    return Result.success_ws(data=dataList,message="select successfully!")    