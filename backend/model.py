from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


class Robot(Base):
    __tablename__ = "robots"
    id:Mapped[int] = mapped_column(BigInteger,primary_key=True)
    name:Mapped[str] = mapped_column(nullable=True)