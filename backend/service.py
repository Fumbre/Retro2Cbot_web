from helper import getSnowFlakeId, dict_orm, orm_dict
from model import (
    Robot,
    ReflectiveSensor,
    RobotSonar,
    RobotPulses,
    RobotNeopxiel,
    RobotGripper,
    select,
    func,
    and_,
)
from fastapi import Request
from response import Result
from datetime import date, timedelta,datetime
from sqlalchemy.orm import Session


def insertRobots(request:Request,robotName: str, robotCode: str):
    db = request.state.db
    try:
        id = getSnowFlakeId()
        robot = Robot(id=id, robotName=robotName, robotCode=robotCode)
        db.add(robot)
        db.commit()
        return Result.success(message="insert Success!")
    except Exception as e:
        db.rollback()
        return Result.error(message=str(e))


def selectRobots(request:Request):
    db = request.state.db
    data = db.scalars(select(Robot)).fetchall()
    resultList = []
    for robot in data:
        resultList.append(
            {"id": str(robot.id), "robotName": robot.robotName, "robotCode": robot.robotCode}
        )
    return Result.success(data=resultList, message="Success!")


def insertReflectiveSensors(request:Request, sensor_list: list[dict]):
    db = request.state.db
    try:
        if sensor_list is None or len(sensor_list) == 0:
            return Result.error(message="data input is empty")
        robotCode = sensor_list[0].get("robotCode")
        robot = db.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        sensors = []
        for sensor in sensor_list:
            id = getSnowFlakeId()
            rs = ReflectiveSensor(id=id, robotId=robot.id)
            dict_orm(sensor, rs)
            sensors.append(rs)
        db.add_all(sensors)
        db.session.commit()
        return Result.success(message="insert sucess!")
    except Exception as e:
        db.session.rollback()
        return Result.error(message=e)


def selectReflectSensorList(db:Session,robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = db.scalars(
        select(ReflectiveSensor).where(
            and_(
                ReflectiveSensor.robotId == robotId,
                ReflectiveSensor.createTime >= startDate,
                ReflectiveSensor.createTime < endDate,
            )
        ).order_by(ReflectiveSensor.createTime.desc())
    ).fetchall()
    resultList = []
    for reflectiveSensor in dataList:
        re = orm_dict(reflectiveSensor)
        resultList.append(re)
    return Result.success_ws(data=resultList, message="select successfully!")


def insertRobotSonarData(request:Request,list: list[dict]):
    db = request.state.db
    try:
        if list is None or len(list) == 0:
            return Result.error(message="data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        sonars = []
        for sonar in list:
            id = getSnowFlakeId()
            data = RobotSonar(id=id, robotId=robot.id)
            dict_orm(sonar, data)
            sonars.append(data)
        db.add_all(sonars)
        db.commit()
        return Result.success(message="insert success!")
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectSonarList(db:Session,robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    endDate = startDate + timedelta(days=1)
    sonarList = []
    list = db.scalars(
        select(RobotSonar).where(
            and_(
                RobotSonar.robotId == robotId,
                RobotSonar.createTime >= startDate,
                RobotSonar.createTime < endDate,
            )
        ).order_by(RobotSonar.createTime.desc())
    ).fetchall()

    for sonar in list:
        data = orm_dict(sonar)
        sonarList.append(data)
    return Result.success_ws(data=sonarList, message="select success!")


def insertRobotPulses(request:Request,list: list[dict]):
    db = request.state.db
    try:
        if list is None or len(list) == 0:
            return Result.error("data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        pulsesList = []
        for data in list:
            id = getSnowFlakeId()
            pulses = RobotPulses(id=id, robotId=robot.id)
            dict_orm(data, pulses)
            pulsesList.append(pulses)
        db.add_all(pulsesList)
        db.commit()
        return Result.success(message="insert successfully!")
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectPulsesList(db:Session,robotId: int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = []
    result = db.scalars(
        select(RobotPulses).where(
            and_(
                RobotPulses.createTime >= startDate,
                RobotPulses.createTime < endDate,
                RobotPulses.robotId == robotId,
            )
        ).order_by(RobotPulses.createTime.desc())
    ).fetchall()

    for data in result:
        pulse = orm_dict(data)
        dataList.append(pulse)
    return Result.success_ws(data=dataList, message="select successfully!")

def insertNeopixels(request:Request,data_list:list[dict]):
    db = request.state.db
    try:
        if data_list is None or len(data_list) == 0:
            return Result.error(message="data input is Empty")
        print(data_list)
        neopexielList = []
        robotCode = data_list[0].get("robotCode")
        robot = db.scalars(
            select(Robot).where(Robot.robotCode == robotCode)
        ).first()
        for data in data_list:
            id = getSnowFlakeId()
            neopixel = RobotNeopxiel(id = id, robotId = robot.id)
            dict_orm(data,neopixel)
            neopexielList.append(neopixel)    
        db.add_all(neopexielList) 
        db.commit()
        return Result.success(message="insert successfully!")
    except Exception as e:
        db.rollback()
        return Result.error(message=e)

def selectNeopixelList(db:Session,robotId:int):
    startDate = datetime.combine(date.today(), datetime.min.time()) 
    endDate = startDate + timedelta(days=1)
    dataList = []
    result = db.scalars(select(RobotNeopxiel).where(
        and_(
            RobotNeopxiel.createTime >= startDate,
            RobotNeopxiel.createTime < endDate,
            RobotNeopxiel.robotId == robotId
        )
    ).order_by(RobotNeopxiel.createTime.desc())).fetchall()
    for data in result:
        neopixel = orm_dict(data)
        dataList.append(neopixel)
    return Result.success_ws(data=dataList,message="select successfully!")

def insertGripperList(request:Request,data_list:list[dict]):
    db = request.state.db
    try:
        if data_list is None or len(data_list) == 0:
          return Result.error(message="data input is Empty!")
        robotCode = data_list[0].get("robotCode")
        gripperList = []
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        for data in data_list:
          id = getSnowFlakeId()
          robotGripper = RobotGripper(id = id, robotId = robot.id)
          dict_orm(data,robotGripper)
          gripperList.append(robotGripper)
        db.add_all(gripperList)
        db.commit()
        return Result.success(message="insert successfully!")
    except Exception as e:
        db.rollback()
        return Result.error(message=e)

def selectCurrentGripper(db:Session,robotId:int):
    maxTimeSQL = (select(func.max(RobotGripper.createTime)).where(RobotGripper.robotId == robotId).scalar_subquery())
    robotGripper = db.scalar(select(RobotGripper).where(
        and_(
            RobotGripper.robotId == robotId,
            RobotGripper.createTime == maxTimeSQL
        )
    ))
    result = orm_dict(robotGripper)
    return Result.success_ws(data=result,message="select sucessfully!")