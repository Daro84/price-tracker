from flask import redirect, url_for, session, request
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session.keys() or session["email"] is None:
            return redirect(url_for("users.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function
