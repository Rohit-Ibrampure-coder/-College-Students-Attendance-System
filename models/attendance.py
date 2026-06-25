from extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "attendance_date",
            name="unique_attendance"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )

    marked_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )