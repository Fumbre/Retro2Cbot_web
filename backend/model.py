from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger,String
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Robot(Base):
    __tablename__ = "robots"
    id:Mapped[int] = mapped_column(BigInteger,primary_key=True,autoincrement=False)
    robotName:Mapped[str] = mapped_column("robot_name",String,nullable=True)
    robotCode:Mapped[str] = mapped_column("robot_code",String,nullable=True)
