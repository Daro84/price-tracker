import requests
from bs4 import BeautifulSoup
from project.common.database import Database
from project.common.utils import Utils
from project.models.alerts.errors import InvalidUrlError
import uuid


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "Item: {} with URL: {}".format(self.name, self.url)

    def load_price(self):
        r = requests.get(self.url)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        elements_value = soup.find_all("span", {"class": "value"})
        elements_penny = soup.find_all("span", {"class": "penny"})
        price_list = []
        for v, p in zip(elements_value, elements_penny):
            price_list.append(float((v.text.strip() + p.text.strip().replace(",", "."))))
        self.price = min(price_list)
        return self.price

    def save_item_data(self):
        Database.update("items", {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one("items", {"_id": item_id}))

    @staticmethod
    def url_validation(url):
        if not Utils.valid_url(url):
            raise InvalidUrlError("Please enter valid URL in format: https://www.ceneo.pl/XXXXXXXX")
        return True
