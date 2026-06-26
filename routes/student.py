from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from flask_login import login_required

from extensions import db
from models.student import Student

student_bp = Blueprint(
    "student",
    __name__
)


# View Students
@student_bp.route("/students")
@login_required
def students():

    search = request.args.get(
        "search",
        ""
    )

    year = request.args.get(
        "year",
        ""
    )

    query = Student.query.filter(

        Student.name.contains(search)
        |
        Student.roll_no.contains(search)

    )

    if year:

        query = query.filter_by(
            year=year
        )

    students = query.all()

    return render_template(
        "students.html",
        students=students,
        search=search,
        year = year
    )


# Add Student
@student_bp.route(
    "/add-student",
    methods=["GET", "POST"]
)
@login_required
def add_student():

    if request.method == "POST":
        phone = request.form["phone"]
        if (
            not phone.isdigit()
            or len(phone) != 10
            or phone[0] not in "6789"
        ):
            return "Enter a valid Indian mobile number."

        student = Student(
            roll_no=request.form["roll_no"],
            name=request.form["name"],
            email=request.form["email"],
            phone=phone,
            course=request.form["course"],
            year=request.form["year"]
        )

        db.session.add(student)
        db.session.commit()

        return redirect(
            url_for("student.students")
        )

    return render_template(
        "add_student.html"
    )


# Edit Student
@student_bp.route(
    "/edit-student/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        phone = request.form["phone"]

        if (
            not phone.isdigit()
            or len(phone) != 10
            or phone[0] not in "6789"
        ):
            return "Enter a valid Indian mobile number."

        student.roll_no = request.form["roll_no"]
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.phone = phone
        student.course = request.form["course"]
        student.year = request.form["year"]

        db.session.commit()

        return redirect(
            url_for("student.students")
        )

    return render_template(
        "edit_student.html",
        student=student
    )

@student_bp.route(
    "/delete-student/<int:id>"
)
@login_required
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return redirect(
        url_for("student.students")
    )