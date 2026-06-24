from flask import Flask

from config import Config
from extensions import db

from models.user import User
from models.student import Student
from models.attendance import Attendance

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")