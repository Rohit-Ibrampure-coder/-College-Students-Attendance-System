from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required
from extensions import db
from models.student import Student
from werkzeug.security import generate_password_hash
from models.user import User

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

    course = request.args.get(
        "course",
        ""
    )

    year = request.args.get(
        "year",
        ""
    )

    query = Student.query

    if search:

        query = query.filter(

            Student.name.contains(search)
            |
            Student.roll_no.contains(search)

        )

    if course:

        query = query.filter_by(
            course=course
        )

    if year:

        query = query.filter_by(
            year=year
        )

    students = query.order_by(
        Student.roll_no
    ).all()

    return render_template(

        "students.html",

        students=students,

        search=search,

        course=course,

        year=year

    )

# Add Student
@student_bp.route(
    "/add-student",
    methods=["GET", "POST"]
)
@login_required
def add_student():

    if request.method == "POST":

        roll_no = request.form["roll_no"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        course = request.form["course"]
        year = request.form["year"]

        # Validate phone number
        if (
            not phone.isdigit()
            or len(phone) != 10
            or phone[0] not in "6789"
        ):

            flash(
                "Enter a valid Indian mobile number.",
                "danger"
            )

            return redirect(
                url_for("student.add_student")
            )

        # Check duplicate Roll Number
        existing_roll = Student.query.filter_by(
            roll_no=roll_no
        ).first()

        if existing_roll:

            flash(
                "Roll number already exists.",
                "danger"
            )

            return redirect(
                url_for("student.add_student")
            )

        # Check duplicate Email
        existing_email = Student.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("student.add_student")
            )

        # Check duplicate Phone
        existing_phone = Student.query.filter_by(
            phone=phone
        ).first()

        if existing_phone:

            flash(
                "Phone number already exists.",
                "danger"
            )

            return redirect(
                url_for("student.add_student")
            )

        student = Student(

            roll_no=roll_no,
            name=name,
            email=email,
            phone=phone,
            course=course,
            year=year

        )

        user = User(

            name=name,

            email=email,

            password=generate_password_hash(
                "student"
            ),

            role="Student"

        )

        try:

            db.session.add(student)
            db.session.add(user)

            db.session.commit()

            flash(
                "Student and login account created successfully.",
                "success"
            )

            return redirect(
                url_for("student.students")
            )

        except Exception:

            db.session.rollback()

            flash(
                "Something went wrong. Please try again.",
                "danger"
            )

            return redirect(
                url_for("student.add_student")
            )

    return render_template(
        "add_student.html"
    )


@student_bp.route(
    "/edit-student/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_student(id):

    student = Student.query.get_or_404(id)
    user = User.query.filter_by(
        email=student.email
    ).first()

    if request.method == "POST":

        roll_no = request.form["roll_no"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form["phone"].strip()
        course = request.form["course"]
        year = request.form["year"]

        # Validate phone number
        if (
            not phone.isdigit()
            or len(phone) != 10
            or phone[0] not in "6789"
        ):

            flash(
                "Enter a valid Indian mobile number.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    id=id
                )
            )

        # Check duplicate Roll Number
        existing_roll = Student.query.filter(
            Student.roll_no == roll_no,
            Student.id != id
        ).first()

        if existing_roll:

            flash(
                "Roll number already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    id=id
                )
            )

        # Check duplicate Email
        existing_email = Student.query.filter(
            Student.email == email,
            Student.id != id
        ).first()

        if existing_email:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    id=id
                )
            )

        # Check duplicate Phone
        existing_phone = Student.query.filter(
            Student.phone == phone,
            Student.id != id
        ).first()

        if existing_phone:

            flash(
                "Phone number already exists.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    id=id
                )
            )

        student.roll_no = roll_no
        student.name = name
        student.email = email
        student.phone = phone
        student.course = course
        student.year = year
        
        if user:

            user.name = name

            user.email = email

        try:

            db.session.commit()

            flash(
                "Student updated successfully.",
                "success"
            )

            return redirect(
                url_for("student.students")
            )

        except Exception:

            db.session.rollback()

            flash(
                "Something went wrong. Please try again.",
                "danger"
            )

            return redirect(
                url_for(
                    "student.edit_student",
                    id=id
                )
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

    user = User.query.filter_by(
        email=student.email
    ).first()

    try:

        if user:

            db.session.delete(user)

        db.session.delete(student)

        db.session.commit()

        flash(
            "Student and login account deleted successfully.",
            "success"
        )

    except Exception:

        db.session.rollback()

        flash(
            "Something went wrong. Please try again.",
            "danger"
        )

    return redirect(
        url_for("student.students")
    )