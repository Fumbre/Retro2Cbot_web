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
from response import Result
from sqlalchemy.orm import Session
from helper import orm_dict


def getRobotInformation(robotCode:str,db:Session):
    return db.scalar(select(Robot).where(Robot.robotCode == robotCode))

def selectNewRSData(db:Session,robotCode:str):
    # get robot information
    robot = getRobotInformation(db=db,robotCode=robotCode)
    # get maxTime 
    maxTimeSQL = (select(func.max(ReflectiveSensor.createTime)).where(ReflectiveSensor.robotId == robot.id)
                  .scalar_subquery())
    rs = db.scalar(select(ReflectiveSensor).where(
        and_(
            ReflectiveSensor.robotId == robot.id,
            ReflectiveSensor.createTime == maxTimeSQL
        )
    ))
    return Result.success(data=orm_dict(rs),message="select successfully!")

def selectNewSonarData(db:Session,robotCode:str):
    # get robot information
    robot = getRobotInformation(db=db,robotCode=robotCode)
    # get maxTime 
    maxTimeSQL = (select(func.max(RobotSonar.createTime)).where(RobotSonar.robotId == robot.id)
                  .scalar_subquery())
    sonarList = db.scalars(select(RobotSonar).where(
        and_(
            RobotSonar.robotId == robot.id,
            RobotSonar.createTime == maxTimeSQL
        )
    )).all()
    result = []
    for sonar in sonarList:
        result.append(orm_dict(sonar))
    return Result.success(data=result,message="select successfully!")


def selectNewPulsesData(db:Session,robotCode:str):
    # get robot information
    robot = getRobotInformation(db=db,robotCode=robotCode)
    # get maxTime 
    maxTimeSQL = (select(func.max(RobotPulses.createTime)).where(RobotPulses.robotId == robot.id)
                  .scalar_subquery())
    pulses = db.scalar(select(RobotPulses).where(
        and_(
            RobotPulses.robotId == robot.id,
            RobotPulses.createTime == maxTimeSQL
        )
    ))
    return Result.success(data=orm_dict(pulses),message="select successfully!")


def selectNewGripperData(db:Session,robotCode:str):
    # get robot information
    robot = getRobotInformation(db=db,robotCode=robotCode)
    # get maxTime 
    maxTimeSQL = (select(func.max(RobotGripper.createTime)).where(RobotGripper.robotId == robot.id)
                  .scalar_subquery())
    gripper = db.scalar(select(RobotGripper).where(
        and_(
            RobotGripper.robotId == robot.id,
            RobotGripper.createTime == maxTimeSQL
        )
    ))
    return Result.success(data=orm_dict(gripper),message="select successfully!")

def selectNewNeopixelData(db:Session,robotCode:str):
    # get robot information
    robot = getRobotInformation(db=db,robotCode=robotCode)
    # get maxTime 
    maxTimeSQL = (select(func.max(RobotNeopxiel.createTime)).where(RobotNeopxiel.robotId == robot.id)
                  .scalar_subquery())
    neopixels = db.scalars(select(RobotNeopxiel).where(
        and_(
            RobotNeopxiel.robotId == robot.id,
            RobotNeopxiel.createTime == maxTimeSQL
        )
    ).order_by(RobotNeopxiel.neopixelIndex.asc())).all()
    result = []
    for led in neopixels:
        result.append(orm_dict(led))
    return Result.success(data=result,message="select successfully!")


