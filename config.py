class Config:
    SECRET_KEY = "attendance-system-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:system%40123@localhost/attendance_system"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False