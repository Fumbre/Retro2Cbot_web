from database import db,app
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    app.run(host=SERVER_IP,port=SERVER_PORT,debug=True)