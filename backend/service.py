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
from datetime import date, timedelta, datetime
from sqlalchemy.orm import Session
import asyncio


def insertRobots(request: Request, robotName: str, robotCode: str):
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


def selectRobots(request: Request):
    db = request.state.db
    data = db.scalars(select(Robot)).fetchall()
    resultList = []
    for robot in data:
        resultList.append(
            {
                "id": str(robot.id),
                "robotName": robot.robotName,
                "robotCode": robot.robotCode,
            }
        )
    return Result.success(data=resultList, message="Success!")


def insertReflectiveSensors(db: Session, sensor_list: list[dict]):
    try:
        if sensor_list is None or len(sensor_list) == 0:
            return Result.error(message="data input is empty")
        robotCode = sensor_list[0].get("robotCode")
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        sensors = []
        id = getSnowFlakeId()
        for sensor in sensor_list:
            rs = ReflectiveSensor(id=id, robotId=robot.id)
            dict_orm(sensor, rs)
            sensors.append(rs)
        db.add_all(sensors)
        db.commit()
        out =  db.scalar(select(ReflectiveSensor).where(ReflectiveSensor.id == id))
        return orm_dict(out)
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectReflectSensorList(db: Session, robotCode: str):
    startDate = datetime.combine(date.today(), datetime.min.time())
    endDate = startDate + timedelta(days=1)
    dataList = db.scalars(
        select(ReflectiveSensor)
        .join(Robot, Robot.id == ReflectiveSensor.robotId)
        .where(
            and_(
                Robot.robotCode == robotCode,
                ReflectiveSensor.createTime >= startDate,
                ReflectiveSensor.createTime < endDate,
            )
        )
        .order_by(ReflectiveSensor.createTime.asc())
    ).fetchall()
    resultList = []
    for reflectiveSensor in dataList:
        re = orm_dict(reflectiveSensor)
        resultList.append(re)
    return Result.success_ws(data=resultList, message="select successfully!")


def insertRobotSonarData(db: Session, list: list[dict]):
    try:
        if list is None or len(list) == 0:
            return Result.error(message="data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        sonars = []
        for sonar in list:
            id = getSnowFlakeId()
            data = RobotSonar(id=id, robotId=robot.id)
            dict_orm(sonar, data)
            sonars.append(data)
        db.add_all(sonars)
        db.commit()
        out = db.scalar(select(RobotSonar).where(RobotSonar.id == id))
        return orm_dict(out)
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectSonarList(db: Session, robotCode: str):
    startDate = datetime.combine(date.today(), datetime.min.time())
    endDate = startDate + timedelta(days=1)
    endDate = startDate + timedelta(days=1)
    sonarList = []
    list = db.scalars(
        select(RobotSonar)
        .join(Robot, Robot.id == RobotSonar.robotId)
        .where(
            and_(
                Robot.robotCode == robotCode,
                RobotSonar.createTime >= startDate,
                RobotSonar.createTime < endDate,
            )
        )
        .order_by(RobotSonar.createTime.asc())
    ).fetchall()

    for sonar in list:
        data = orm_dict(sonar)
        sonarList.append(data)
    return Result.success_ws(data=sonarList, message="select success!")


def insertRobotPulses(db: Session, list: list[dict]):
    try:
        if list is None or len(list) == 0:
            return Result.error("data input is empty")
        robotCode = list[0].get("robotCode")
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        pulsesList = []
        id = getSnowFlakeId()
        for data in list:
            pulses = RobotPulses(id=id, robotId=robot.id)
            dict_orm(data, pulses)
            pulsesList.append(pulses)
        db.add_all(pulsesList)
        db.commit()
        out = db.scalar(select(RobotPulses).where(RobotPulses.id == id))
        return orm_dict(out)
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectPulsesList(db: Session, robotCode: str):
    startDate = datetime.combine(date.today(), datetime.min.time())
    endDate = startDate + timedelta(days=1)
    dataList = []
    # this part represent this SQL:
    # select robot_pulses.id, robot_pulses.robot_id, robot_pulses.left_wheel_pulse, 
    # robot_pulses.right_wheel_pulses, robot_pulses.create_time
    # from robot_pulses
    # inner join robots on robots.id = robot_pulses.robot_id
    # where robot_pulses.create_time >= #{startDate} and robot_pulses.create_time < #{endDate} and robots.robot_code = #{robotCode}
    # order by robot_pulses.create_time asc;
    result = db.scalars(
        select(RobotPulses)
        .join(Robot, Robot.id == RobotPulses.robotId)
        .where(
            and_(
                RobotPulses.createTime >= startDate,
                RobotPulses.createTime < endDate,
                Robot.robotCode == robotCode,
            )
        )
        .order_by(RobotPulses.createTime.asc())
    ).fetchall()
     
    for data in result:
        pulse = orm_dict(data)
        dataList.append(pulse)
    return Result.success_ws(data=dataList, message="select successfully!")


def insertNeopixels(db: Session, data_list: list[dict]):
    try:
        if data_list is None or len(data_list) == 0:
            return Result.error(message="data input is Empty")
        print(data_list)
        neopexielList = []
        robotCode = data_list[0].get("robotCode")
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        for data in data_list:
            id = getSnowFlakeId() # get snowflake id
            neopixel = RobotNeopxiel(id=id, robotId=robot.id)
            dict_orm(data, neopixel)
            neopexielList.append(neopixel)
        db.add_all(neopexielList) # insert data, which data type is list[RobotNeopxiel]
        db.commit() # submit transactions to the database (insert data into database really)
        out = db.scalar(select(RobotNeopxiel).where(RobotNeopxiel.id == id))
        return orm_dict(out)
    except Exception as e:
        db.rollback() # if there exists errors, it rollbacks the transaction for avoiding data of trush.
        return Result.error(message=e)


def selectNeopixelList(db: Session, robotCode: str):
    startDate = datetime.combine(date.today(), datetime.min.time())
    endDate = startDate + timedelta(days=1)
    dataList = []
    result = db.scalars(
        select(RobotNeopxiel)
        .join(Robot, Robot.id == RobotNeopxiel.robotId)
        .where(
            and_(
                RobotNeopxiel.createTime >= startDate,
                RobotNeopxiel.createTime < endDate,
                Robot.robotCode == robotCode,
            )
        )
        .order_by(RobotNeopxiel.createTime.asc())
    ).fetchall()
    for data in result:
        neopixel = orm_dict(data)
        dataList.append(neopixel)
    return Result.success_ws(data=dataList, message="select successfully!")


def insertGripperList(db: Session, data_list: list[dict]):
    try:
        if data_list is None or len(data_list) == 0:
            return Result.error(message="data input is Empty!")
        robotCode = data_list[0].get("robotCode")
        gripperList = []
        robot = db.scalars(select(Robot).where(Robot.robotCode == robotCode)).first()
        id = getSnowFlakeId()
        for data in data_list:
            robotGripper = RobotGripper(id=id, robotId=robot.id)
            dict_orm(data, robotGripper)
            gripperList.append(robotGripper)
        db.add_all(gripperList)
        db.commit()
        out = db.scalar(select(RobotGripper).where(RobotGripper.id == id))
        return orm_dict(out)
    except Exception as e:
        db.rollback()
        return Result.error(message=e)


def selectCurrentGripper(db: Session, robotCode: str):
    robot = db.scalar(select(Robot).where(Robot.robotCode == robotCode))
    # subquery SQL:
    # select max(create_time) from robot_gripper where robot_id = #{robotId}
    maxTimeSQL = (
        select(func.max(RobotGripper.createTime))
        .where(RobotGripper.robotId == robot.id)
        .scalar_subquery()
    )

    #final SQL:
    # select 
    # * 
    # from robot_gripper 
    # where create_time = (select max(create_time)
    # from robot_gripper 
    # where robot_id = #{robotId})
    #  and 
    # robot_id = #{robotId}
    robotGripper = db.scalar(
        select(RobotGripper).where(
            and_(
                RobotGripper.robotId == robot.id, RobotGripper.createTime == maxTimeSQL
            )
        )
    )
    result = orm_dict(robotGripper)
    return Result.success_ws(data=result, message="select sucessfully!")


async def push_data_loop(websocket, db_factory, robotCode, event):
    while True:
        await asyncio.sleep(1) # async wait 1 second.
        db = db_factory()
        try:
            if event == "rs":
                result = selectReflectSensorList(db, robotCode)
            elif event == "sonar":
                result = selectSonarList(db, robotCode)
            elif event == "pulses":
                result = selectPulsesList(db, robotCode)
            elif event == "neopixels":
                result = selectNeopixelList(db, robotCode)
            elif event == "gripper":
                result = selectCurrentGripper(db, robotCode)
            else:
                continue

            await websocket.send_json({**result, "event": event})
        except asyncio.CancelledError:
            print("data_push_loop task is canceled!")
            raise    
        except Exception as e:
            print(e)   
        finally:
            db.close()
        