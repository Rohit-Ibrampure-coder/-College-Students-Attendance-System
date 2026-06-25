from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)
from models.student import Student
from models.attendance import Attendance

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    total_students = Student.query.count()

    total_attendance = Attendance.query.count()

    low_attendance_students = 0

    students = Student.query.all()

    for student in students:

        total_days = Attendance.query.filter_by(
            student_id=student.id
        ).count()

        present_days = Attendance.query.filter_by(
            student_id=student.id,
            status="Present"
        ).count()

        if total_days > 0:

            percentage = (
                present_days / total_days
            ) * 100

            if percentage < 75:

                low_attendance_students += 1

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        low_attendance_students=low_attendance_students
    )