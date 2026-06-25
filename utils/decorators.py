from functools import wraps
from flask_login import current_user
from flask import abort

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if current_user.role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper