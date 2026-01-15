from snowflake import SnowflakeGenerator
import os
from dotenv import load_dotenv
from typing import Any
from datetime import datetime

# load value of configurations from .env file
load_dotenv()
# get machine id from .env file
instance = int(os.environ.get("SNOWFLAKE_INSTANCE"))
# create snowflake id generator
gen = SnowflakeGenerator(instance=instance)


def getSnowFlakeId():
    """
    generate snowflake id
    """
    return next(gen)


def dict_orm(src: dict, dest):
    """
    copy value from dict to class instance properties
    
    :param src: source data
    :type src: dict
    :param dest: class instance
    """
    for k, v in src.items(): # loop dict, k:key, v:value
        if hasattr(dest, k): # if dest contains this property, which name is same with k.
            setattr(dest, k, v) # update the value of properties in dest instance.      

def orm_dict(obj: Any) -> dict:
    """
    class instance transfers to dict.
    
    :param obj: class instance
    :type obj: Any
    :return: target dict
    :rtype: dict
    """
    result = {}
    if obj is None:
        return result
    for attr in obj.__mapper__.attrs: # loop object properties.
        try:
            value = getattr(obj, attr.key) # get value from property
            if isinstance(value, datetime): # check this data type of property whether it is datetime.
                result[attr.key] = value.strftime("%Y-%m-%d %H:%M:%S") # this value convert to string, which format is yyyy-MM-dd HH:mm:ss. eg: 2026-01-03 20:19.
            elif isinstance(value,int) and (attr.key.endswith("Id") or attr.key == "id"): #check this data type of property whether it is integer, and check name of key whther contains id or Id
                result[attr.key] = str(value) # put this data into result.
            else:
                result[attr.key] = value #  put this data into result. eg: {"id":15465656,name:"Diamond dog","robotCode":"BB046"}
        except AttributeError:
            continue
    return result
