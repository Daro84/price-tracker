from flask import Flask, render_template
from project.common.database import Database
import os


app = Flask(__name__)
app.config.from_object("project.config")
app.secret_key = os.environ.get("app.secret_key")


@app.before_first_request
def database_init():
    Database.initialize()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


from project.models.users.views import user_blueprint
from project.models.alerts.views import alert_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")