from flask import Flask
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db

from models.user import User

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():

    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password=generate_password_hash("admin123"),
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin created successfully!")