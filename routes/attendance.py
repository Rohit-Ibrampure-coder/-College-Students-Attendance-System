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
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import (
    getSampleStyleSheet
)
from reportlab.lib import colors
from flask import send_file
from io import BytesIO

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

            flash(
                f"Attendance already exists for {attendance_date}",
                "warning"
            )

            return redirect(
                url_for("attendance.attendance")
            )

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

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    course = request.args.get("course")
    year = request.args.get("year")
    status = request.args.get("status")

    query = Attendance.query.join(Student)

    if from_date:

        query = query.filter(
            Attendance.attendance_date >= from_date
        )

    if to_date:

        query = query.filter(
            Attendance.attendance_date <= to_date
        )

    if course:

        query = query.filter(
            Student.course == course
        )

    if year:

        query = query.filter(
            Student.year == year
        )

    if status:

        query = query.filter(
            Attendance.status == status
        )

    records = query.order_by(
        Attendance.attendance_date.desc()
    ).all()

    return render_template(
        "attendance_report.html",
        records=records,
        from_date=from_date,
        to_date=to_date,
        course=course,
        year=year,
        status=status
    )

@attendance_bp.route("/attendance-summary")
@login_required
def attendance_summary():

    course = request.args.get("course")
    year = request.args.get("year")
    filter_status = request.args.get("status")

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
            attendance_status = "Low Attendance"
        else:
            attendance_status = "Good"

        report.append({
            "student": student,
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "percentage": percentage,
            "status": attendance_status
        })

    if filter_status == "Low Attendance":

        report = [

            row

            for row in report

            if row["percentage"] < 75

        ]

    return render_template(
        "attendance_summary.html",
        report=report,
        course=course,
        year=year,
        status=filter_status
    )

@attendance_bp.route(
    "/student-attendance/<int:student_id>"
)
@login_required
def student_attendance(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    records = Attendance.query.filter_by(
        student_id=student_id
    ).all()

    return render_template(
        "student_attendance.html",
        student=student,
        records=records
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

@attendance_bp.route(
    "/attendance-report/pdf"
)
@login_required
def attendance_report_pdf():

    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    course = request.args.get("course")
    year = request.args.get("year")

    query = Attendance.query.join(Student)

    if from_date:

        query = query.filter(
            Attendance.attendance_date >= from_date
        )

    if to_date:

        query = query.filter(
            Attendance.attendance_date <= to_date
        )

    if course:

        query = query.filter(
            Student.course == course
        )

    if year:

        query = query.filter(
            Student.year == year
        )

    records = query.order_by(
        Attendance.attendance_date.desc()
    ).all()

    filename = (
        f"Attendance_"
        f"{course or 'All'}_"
        f"{year or 'All'}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    elements = []

    college_name = Paragraph(
        "Dhananjayrao Gadgil College of Commerce, Satara",
        styles["Title"]
    )

    report_title = Paragraph(
        f"Student Attendance Report - {course or 'All Courses'} ({year or 'All Years'})",
        styles["Heading2"]
    )

    generated_date = Paragraph(
        f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    )

    total_records = Paragraph(
        f"Total Attendance Records: {len(records)}",
        styles["Normal"]
    )

    elements.append(college_name)

    elements.append(report_title)

    elements.append(
        Spacer(1, 10)
    )

    filter_details = Paragraph(
        f"<b>Course:</b> {course or 'All Courses'}<br/>"
        f"<b>Year:</b> {year or 'All Years'}<br/>"
        f"<b>From Date:</b> {from_date or 'All Dates'}<br/>"
        f"<b>To Date:</b> {to_date or 'All Dates'}",
        styles["Normal"]
    )

    elements.append(filter_details)

    elements.append(
        Spacer(1, 10)
    )

    elements.append(generated_date)

    elements.append(
        Spacer(1, 10)
    )

    elements.append(total_records)

    elements.append(
        Spacer(1, 15)
    )

    data = [[
        "Date",
        "Roll No",
        "Student Name",
        "Status"
    ]]

    for record in records:

        data.append([
            str(record.attendance_date),
            record.student.roll_no,
            record.student.name,
            record.status
        ])

    table = Table(data)

    table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#0F172A")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.black
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.whitesmoke,
                    colors.lightgrey
                ]
            )

        ])

    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    footer = Paragraph(
        "Generated by College Attendance Management System",
        styles["Italic"]
    )

    elements.append(footer)

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )

@attendance_bp.route(
    "/student-attendance-pdf/<int:student_id>"
)
@login_required
def student_attendance_pdf(student_id):

    student = Student.query.get_or_404(
        student_id
    )

    records = Attendance.query.filter_by(
        student_id=student_id
    ).all()

    present_days = Attendance.query.filter_by(
        student_id=student_id,
        status="Present"
    ).count()

    absent_days = Attendance.query.filter_by(
        student_id=student_id,
        status="Absent"
    ).count()

    total_days = len(records)

    percentage = 0

    if total_days > 0:

        percentage = round(
            (present_days / total_days) * 100,
            2
        )

    if percentage >= 75:

        attendance_status = "Good (Attendance ≥ 75%)"

    else:

        attendance_status = "Low Attendance (Attendance < 75%)"

    filename = (
        f"{student.roll_no}_Attendance_Report.pdf"
    )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    elements = []

    college = Paragraph(
        "Dhananjayrao Gadgil College of Commerce, Satara",
        styles["Title"]
    )

    title = Paragraph(
        "Student Attendance Report",
        styles["Heading2"]
    )

    generated = Paragraph(
        f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    )

    elements.append(college)

    elements.append(title)

    elements.append(generated)

    elements.append(
        Spacer(1, 15)
    )

    student_info = [

        ["Roll No", student.roll_no],

        ["Student Name", student.name],

        ["Course", student.course],

        ["Year", student.year]

    ]

    student_table = Table(student_info)

    student_table.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    elements.append(student_table)

    elements.append(
        Spacer(1,15)
    )

    summary_title = Paragraph(
        "Attendance Summary",
        styles["Heading2"]
    )

    elements.append(summary_title)

    elements.append(
        Spacer(1,10)
    )

    summary_data = [

        ["Present Days", present_days],

        ["Absent Days", absent_days],

        ["Total Days", total_days],

        ["Attendance %", f"{percentage}%"],

        ["Status", attendance_status]

    ]

    summary_table = Table(summary_data)

    summary_table.setStyle(

        TableStyle([

            (
                "GRID",
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),

            (
                "BACKGROUND",
                (0,0),
                (0,-1),
                colors.lightgrey
            ),

            (
                "BOTTOMPADDING",
                (0,0),
                (-1,-1),
                8
            )

        ])

    )

    elements.append(summary_table)

    elements.append(
        Spacer(1,15)
    )

    details_title = Paragraph(
        "Attendance Details",
        styles["Heading2"]
    )

    elements.append(details_title)

    elements.append(
        Spacer(1,10)
    )

    details_data = [[
        "Date",
        "Status"
    ]]

    for record in records:

        details_data.append([
            str(record.attendance_date),
            record.status
        ])

    details_table = Table(details_data)

    details_table.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#0F172A")
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "FONTNAME",
                (0,0),
                (-1,0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                1,
                colors.black
            ),

            (
                "ROWBACKGROUNDS",
                (0,1),
                (-1,-1),
                [
                    colors.whitesmoke,
                    colors.lightgrey
                ]
            )

        ])

    )

    elements.append(details_table)

    elements.append(
        Spacer(1,20)
    )

    footer = Paragraph(
        "Generated by College Attendance Management System",
        styles["Italic"]
    )

    elements.append(footer)

    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )