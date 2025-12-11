from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger,Integer,String,INTEGER,DateTime,Float,func,select,and_
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Robot(Base):
    __tablename__ = "robots"
    id:Mapped[int] = mapped_column("id",BigInteger,primary_key=True,autoincrement=False)
    robotName:Mapped[str] = mapped_column("robot_name",String,nullable=True)
    robotCode:Mapped[str] = mapped_column("robot_code",String,nullable=True)

class ReflectiveSensor(Base):
    __tablename__ = "reflective_sensor"
    id:Mapped[int] = mapped_column("id",BigInteger,primary_key=True,autoincrement=False)
    robotId:Mapped[int] = mapped_column("robot_id",BigInteger,nullable=False)
    a0:Mapped[int] = mapped_column("a0",Integer,nullable=False)
    a1:Mapped[int] = mapped_column("a1",Integer,nullable=False)
    a2:Mapped[int] = mapped_column("a2",Integer,nullable=False)
    a3:Mapped[int] = mapped_column("a3",Integer,nullable=False)
    a4:Mapped[int] = mapped_column("a4",Integer,nullable=False)
    a5:Mapped[int] = mapped_column("a5",Integer,nullable=False)
    a6:Mapped[int] = mapped_column("a6",Integer,nullable=False)
    a7:Mapped[int] = mapped_column("a7",Integer,nullable=False)
    create_time:Mapped[datetime] = mapped_column("create_time",DateTime,server_default=func.now())

class RobotPulses(Base):
    __tablename__ = "robot_pulses"
    id:Mapped[int] = mapped_column("id",primary_key=True,autoincrement=False)
    robotId:Mapped[int] = mapped_column("robot_id",BigInteger,nullable=False)
    leftWheelPulses:Mapped[int] = mapped_column("left_wheel_pulse",BigInteger,nullable=False)
    rightWheelPulses:Mapped[int] = mapped_column("right_wheel_pulse",BigInteger,nullable=False)
    createTime:Mapped[datetime] = mapped_column("create_time",DateTime,server_default=func.now())

class RobotSonar(Base):
    __tablename__ = "robot_sonar"
    id:Mapped[int] = mapped_column("id",BigInteger,primary_key=True,autoincrement=False)
    robotId:Mapped[int] = mapped_column("robot_id",BigInteger,nullable=False)
    sonarDistance:Mapped[float] = mapped_column("sonar_distance",Float,nullable=False)
    createTime:Mapped[datetime] = mapped_column("create_time",DateTime,server_default=func.now())

class robotNeopxiel(Base):
    __tablename__ = "robot_neopixels"
    id:Mapped[int] = mapped_column("id",BigInteger,primary_key=True,autoincrement=False)
    robotId:Mapped[int] = mapped_column("robot_id",BigInteger,nullable=False)
    neopixelIndex:Mapped[int] = mapped_column("neopixel_index",Integer,nullable=False)
    r:Mapped[int] = mapped_column("r",Integer,nullable=False)
    g:Mapped[int] = mapped_column("g",Integer,nullable=False)
    b:Mapped[int] = mapped_column("b",Integer,nullable=False)
    createTime:Mapped[datetime] = mapped_column("create_time",DateTime,server_default=func.now())