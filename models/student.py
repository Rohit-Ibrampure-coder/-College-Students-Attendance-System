from extensions import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    roll_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100)
    )

    phone = db.Column(
        db.String(10)
    )

    course = db.Column(
        db.String(50),
        nullable=False
    )

    year = db.Column(
        db.String(50),
        nullable=False
    )

    attendance_records = db.relationship(
        "Attendance",
        backref="student",
        lazy=True
    )
    
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )