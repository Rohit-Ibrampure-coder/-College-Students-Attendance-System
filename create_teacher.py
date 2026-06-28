from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db
from models.user import User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():

    existing_teacher = User.query.filter_by(
        email="teacher@gmail.com"
    ).first()

    if existing_teacher:
        print("Teacher already exists!")
    else:
        teacher = User(
            name="Teacher",
            email="teacher@gmail.com",
            password=generate_password_hash("teacher123"),
            role="teacher"
        )

        db.session.add(teacher)
        db.session.commit()

        print("Teacher created successfully!")