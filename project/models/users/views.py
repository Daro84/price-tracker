from flask import Blueprint, render_template, request, session, redirect, url_for
from project.models.users.user import User
import project.models.users.errors as Errors
import project.models.users.decorators as decorators

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            if User.register(email, password):
                session["email"] = email
                return redirect(url_for(".user_alerts"))
        except Errors.UserErrors as e:
            return e.message

    return render_template("users/register.html")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            if User.user_validation(email, password):
                session["email"] = email
                return redirect(url_for(".user_alerts"))
        except Errors.UserErrors as e:
            return e.message

    return render_template("users/login.html")


@user_blueprint.route("/alerts")
@decorators.login_required
def user_alerts():
    user = User.find_by_email(session["email"])
    alerts = user.get_alerts()
    return render_template("users/alerts.html", alerts=alerts)


@user_blueprint.route("/alerts_list/<string:user_id>")
def alerts_list(user_id):
    pass


@user_blueprint.route("/logout")
def logout():
    session["email"] = None
    return redirect(url_for("home"))


