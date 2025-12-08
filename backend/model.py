from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

