from dotenv import load_dotenv
import uvicorn
from database import app
import os
from weboscket import router as websocket
from api import router as api

# load value of configurations from .env file
load_dotenv()

app.include_router(api)
app.include_router(websocket)


if __name__ == "__main__":
    SERVER_IP = os.environ.get("SERVER_IP")
    SERVER_PORT = int(os.environ.get("SERVER_PORT"))
    # Uvicorn is a async web service framework. it can support normal and async Http request and websockets
    uvicorn.run("app:app", host=SERVER_IP, port=SERVER_PORT, reload=True)