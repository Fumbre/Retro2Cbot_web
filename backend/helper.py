from snowflake import SnowflakeGenerator
import os
from dotenv import load_dotenv
from typing import Any
from datetime import datetime

load_dotenv()

instance = int(os.environ.get("SNOWFLAKE_INSTANCE"))

ser = None

gen = SnowflakeGenerator(instance=instance)


def getSnowFlakeId():
    return next(gen)


def dict_orm(src: dict, dest):
    for k, v in src.items():
        if hasattr(dest, k):
            setattr(dest, k, v)        

def orm_dict(obj: Any) -> dict:
    result = {}
    for attr in obj.__mapper__.attrs:
        try:
            value = getattr(obj, attr.key)
            if isinstance(value, datetime):
                result[attr.key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                result[attr.key] = value
        except AttributeError:
            continue
    return result
