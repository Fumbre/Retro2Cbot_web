from dotenv import load_dotenv
from model import db
import os
from flask import Flask

# load .env file
load_dotenv()
DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_CONFIGURATION = os.environ.get("DB_CONFIGURATION")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}{DB_CONFIGURATION}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)

with app.app_context():
    db.create_all()