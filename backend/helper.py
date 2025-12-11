from snowflake import SnowflakeGenerator
import os
from dotenv import load_dotenv
from typing import Any

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

def orm_dict(obj:Any) ->dict:
    result = {}
    for attr in dir(obj):
        if attr.startswith("_") or callable(getattr(obj, attr)):
            continue
        result[attr] = getattr(obj, attr)
    return result
