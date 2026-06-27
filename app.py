from flask import Flask

from config import Config
from extensions import db, login_manager
from flask_login import login_required
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.student import student_bp
from models.user import User
from flask import render_template
from routes.attendance import attendance_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = "auth.login"


@app.route("/")
def home():
    return render_template("index.html")

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)

if __name__ == "__main__":
    app.run(debug=True)