import uuid, requests
from project.models.items.item import Item
import project.models.alerts.constants as AlertConst
from project.common.database import Database
import datetime


class Alert(object):
    def __init__(self, user_email, item_id, price_limit, active=True, last_check=None, _id=None):
        self.user_email = user_email
        self.item = Item.get_by_id(item_id)
        self.price_limit = price_limit
        self.last_check = datetime.datetime.utcnow() if last_check is None else last_check
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "Price alert for user {} on item {} with limit {}".format(self.user_email, self.item.name,
                                                                         self.price_limit)

    def send_email(self):
        return requests.post(
            AlertConst.URL,
            auth=("api", AlertConst.API_KEY),
            data={"from": AlertConst.FROM,
                  "to": self.user_email,
                  "subject": "Price alert for {}".format(self.item.name),
                  "text": "{} now is available for {} PLN! Link here: {}".format(self.item.name, self.item.price,
                                                                                 self.item.url)
                  }
        )

    @classmethod
    def find_alerts_to_update(cls, minutes_since_update=AlertConst.TIME):
        update_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**e) for e in Database.find("alerts",
                                                {"last_check": {"$lte": update_limit},
                                                 "active": True
                                                 })]

    def save_alert_data(self):
        Database.update("alerts", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_check": self.last_check,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def check_price(self):
        self.item.load_price()
        self.last_check = datetime.datetime.utcnow()
        self.item.save_item_data()
        self.save_alert_data()
        return self.item.price

    def send_email_alert(self):
        if self.item.price < self.price_limit:
            self.send_email()

    @classmethod
    def find_by_email(cls, user_email):
        alerts_data = Database.find("alerts", {"user_email": user_email})
        return [cls(**alert) for alert in alerts_data]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one("alerts", {"_id": alert_id}))

    def deactivate(self):
        self.active = False
        self.save_alert_data()

    def activate(self):
        self.active = True
        self.save_alert_data()

    def delete(self):
        Database.remove("alerts", {"_id": self._id})
