from flask import Blueprint, render_template, request, session, redirect, url_for
from project.models.alerts.alert import Alert
from project.models.items.item import Item
import project.models.alerts.errors as Errors
import project.models.users.decorators as decorators

alert_blueprint = Blueprint("alerts", __name__)


@alert_blueprint.route("/add", methods=["GET", "POST"])
@decorators.login_required
def add_alert():
    if request.method == "POST":
        name = request.form["name"]
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        try:
            if Item.url_validation(url):
                item = Item(name, url)
                item.save_item_data()
                alert = Alert(session['email'], item._id, price_limit)
                alert.check_price()
                return redirect(url_for("users.user_alerts"))
        except Errors.AlertErrors as e:
            return e.message

    return render_template("alerts/new_alert.html")


@alert_blueprint.route("/<string:alert_id>")
@decorators.login_required
def check_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.html", alert=alert)


@alert_blueprint.route("/check_price/<string:alert_id>")
@decorators.login_required
def check_actual_price(alert_id):
    Alert.find_by_id(alert_id).check_price()
    return redirect(url_for('.check_alert', alert_id=alert_id))


@alert_blueprint.route("/edit/<string:alert_id>", methods=["GET", "POST"])
@decorators.login_required
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == "POST":
        price_limit = float(request.form["price_limit"])

        alert.price_limit = price_limit
        alert.save_alert_data()
        return redirect(url_for('users.user_alerts'))

    return render_template("alerts/edit_alert.html", alert=alert)


@alert_blueprint.route("/activate/<string:alert_id>")
@decorators.login_required
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route("/deactivate/<string:alert_id>")
@decorators.login_required
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route("/delete/<string:alert_id>")
@decorators.login_required
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))