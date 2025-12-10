from snowflake import SnowflakeGenerator
import os
from dotenv import load_dotenv
import serial
import time

load_dotenv()

instance = int(os.environ.get("SNOWFLAKE_INSTANCE"))
SERIAL_PORT = os.environ.get("SERIAL_PORT")
BAUDRATE = int(os.environ.get("BAUDRATE"))
RECONNECT_DELAY = int(os.environ.get("RECONNECT_DELAY"))

ser = None

gen = SnowflakeGenerator(instance=instance)

def getSnowFlakeId():
    return next(gen)

def buildConnectionWithHC12():
    global ser
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT,BAUDRATE, timeout=1)
            print("build HC-12 connection successfully!")
            print(f"serial_port: {SERIAL_PORT}, baudrate: {BAUDRATE}")
            break
        except serial.SerialException:
            print(f"Can't connect to HC-12, Serial port: {SERIAL_PORT}, retry after {RECONNECT_DELAY} seconds....")
            time.sleep(RECONNECT_DELAY)