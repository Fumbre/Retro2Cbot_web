from snowflake import SnowflakeGenerator
import os
from dotenv import load_dotenv

load_dotenv()

instance = int(os.environ.get("SNOWFLAKE_INSTANCE"))
SERIAL_PORT = os.environ.get("SERIAL_PORT")
BAUDRATE = int(os.environ.get("BAUDRATE"))
RECONNECT_DELAY = int(os.environ.get("RECONNECT_DELAY"))

ser = None

gen = SnowflakeGenerator(instance=instance)

def getSnowFlakeId():
    return next(gen)