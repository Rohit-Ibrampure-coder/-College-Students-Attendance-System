from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect
)
from flask_login import login_required
from models.student import Student
from flask_login import current_user
from extensions import db
from models.attendance import Attendance


attendance_bp = Blueprint(
    "attendance",
    __name__
)


@attendance_bp.route(
    "/attendance",
    methods=["GET", "POST"]
)
@login_required
def attendance():

    students = []

    if request.method == "POST":

        course = request.form["course"]
        year = request.form["year"]
        attendance_date = request.form["attendance_date"]

        students = Student.query.filter_by(
            course=course,
            year=year
        ).all()

        return render_template(
            "attendance.html",
            students=students,
            course=course,
            year=year,
            attendance_date=attendance_date
        )

    return render_template(
        "attendance.html",
        students=students
    )

@attendance_bp.route(
    "/save-attendance",
    methods=["POST"]
)
@login_required
def save_attendance():

    course = request.form["course"]

    year = request.form["year"]

    attendance_date = request.form[
        "attendance_date"
    ]

    students = Student.query.filter_by(
        course=course,
        year=year
    ).all()

    for student in students:

        existing = Attendance.query.filter_by(
            student_id=student.id,
            attendance_date=attendance_date
        ).first()

        if existing:
            continue

        status = request.form.get(
            f"status_{student.id}"
        )

        if status:

            attendance = Attendance(

                student_id=student.id,

                attendance_date=attendance_date,

                status=status,

                marked_by=current_user.id

            )

            db.session.add(
                attendance
            )

    db.session.commit()

    flash(
        "Attendance saved successfully!",
        "success"
    )

    return redirect(
        url_for(
            "attendance.attendance"
        )
    )

@attendance_bp.route(
    "/attendance-report",
    methods=["GET"]
)
@login_required
def attendance_report():

    attendance_date = request.args.get("attendance_date")
    course = request.args.get("course")
    year = request.args.get("year")

    records = Attendance.query.all()

    if attendance_date:
        records = [
            record
            for record in records
            if str(record.attendance_date) == attendance_date
        ]

    if course:
        records = [
            record
            for record in records
            if record.student.course == course
        ]

    if year:
        records = [
            record
            for record in records
            if record.student.year == year
        ]

    return render_template(
        "attendance_report.html",
        records=records,
        attendance_date=attendance_date,
        course=course,
        year=year
    )


@attendance_bp.route("/attendance-summary")
@login_required
def attendance_summary():

    course = request.args.get("course")
    year = request.args.get("year")

    students = Student.query

    if course:
        students = students.filter_by(
            course=course
        )

    if year:
        students = students.filter_by(
            year=year
        )

    students = students.all()

    report = []

    for student in students:

        total_days = Attendance.query.filter_by(
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

        if total_days > 0:

            percentage = round(
                (present_days / total_days) * 100,
                2
            )

        if percentage < 75:
            status = "Low Attendance"
        else:
            status = "Good"

        report.append({
            "student": student,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "percentage": percentage,
            "status": status
        })

    return render_template(
        "attendance_summary.html",
        report=report,
        course=course,
        year=year
    )

@attendance_bp.route(
    "/edit-attendance/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_attendance(id):

    attendance = Attendance.query.get_or_404(id)

    if request.method == "POST":

        attendance.status = request.form["status"]

        db.session.commit()

        return redirect(
            url_for(
                "attendance.attendance_report"
            )
        )

    return render_template(
        "edit_attendance.html",
        attendance=attendance
    )

@attendance_bp.route(
    "/delete-attendance/<int:id>"
)
@login_required
def delete_attendance(id):

    attendance = Attendance.query.get_or_404(
        id
    )

    db.session.delete(
        attendance
    )

    db.session.commit()

    return redirect(
        url_for(
            "attendance.attendance_report"
        )
    )