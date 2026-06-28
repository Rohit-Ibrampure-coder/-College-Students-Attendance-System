from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from models.student import Student
from models.attendance import Attendance

student_portal_bp = Blueprint(
    "student_portal",
    __name__
)

from utils.pdf_generator import generate_student_attendance_pdf


@student_portal_bp.route(
    "/student/dashboard"
)
@login_required
def student_dashboard():

    student = Student.query.filter_by(
        email=current_user.email
    ).first_or_404()

    total_classes = Attendance.query.filter_by(
        student_id=student.id
    ).count()

    present_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Present"
    ).count()

    absent_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Absent"
    ).count()

    percentage = 0

    if total_classes > 0:

        percentage = round(
            (present_days / total_classes) * 100,
            2
        )

    if percentage >= 75:

        attendance_status = "Good Attendance"

    else:

        attendance_status = "Low Attendance"

    return render_template(

        "student/dashboard.html",

        student=student,

        total_classes=total_classes,

        present_days=present_days,

        absent_days=absent_days,

        percentage=percentage,

        attendance_status=attendance_status

    )

@student_portal_bp.route(
    "/student/my-attendance",
    methods=["GET", "POST"]
)
@login_required
def my_attendance():

    student = Student.query.filter_by(
        email=current_user.email
    ).first_or_404()

    records = Attendance.query.filter_by(
        student_id=student.id
    )

    from_date = ""
    to_date = ""

    if request.method == "POST":

        from_date = request.form["from_date"]
        to_date = request.form["to_date"]

        if from_date:

            records = records.filter(
                Attendance.attendance_date >= from_date
            )

        if to_date:

            records = records.filter(
                Attendance.attendance_date <= to_date
            )

    records = records.order_by(
        Attendance.attendance_date.desc()
    ).all()

    return render_template(

        "student/my_attendance.html",

        records=records,

        from_date=from_date,

        to_date=to_date

    )

@student_portal_bp.route(
    "/student/attendance-summary"
)
@login_required
def attendance_summary():

    student = Student.query.filter_by(
        email=current_user.email
    ).first_or_404()

    total_classes = Attendance.query.filter_by(
        student_id=student.id
    ).count()

    present_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Present"
    ).count()

    absent_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Absent"
    ).count()

    percentage = 0

    if total_classes > 0:

        percentage = round(
            (present_days / total_classes) * 100,
            2
        )

    status = (
        "Good Attendance"
        if percentage >= 75
        else "Low Attendance"
    )

    return render_template(

        "student/attendance_summary.html",

        student=student,

        total_classes=total_classes,

        present_days=present_days,

        absent_days=absent_days,

        percentage=percentage,

        status=status

    )

@student_portal_bp.route(
    "/student/download-attendance-pdf"
)
@login_required
def download_attendance_pdf():

    student = Student.query.filter_by(
        email=current_user.email
    ).first_or_404()

    return generate_student_attendance_pdf(
        student
    )

@student_portal_bp.route(
    "/student/profile"
)
@login_required
def student_profile():

    student = Student.query.filter_by(
        email=current_user.email
    ).first_or_404()

    return render_template(

        "student/profile.html",

        student=student

    )