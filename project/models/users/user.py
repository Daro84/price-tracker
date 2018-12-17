import uuid
from project.common.database import Database
from project.models.users.errors import UserNotExistsError, InvalidPasswordError, \
    UserAlreadyExistsError, InvalidEmailAddressError
from project.models.alerts.alert import Alert
from project.common.utils import Utils


class User(object):
    def __init__(self, email, password, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {} with an email {}".format(self.user,self.email)

    @staticmethod
    def user_validation(email, password):
        # generate sha512 hashed password
        user_data = Database.find_one("users", {"email": email})
        if user_data is None:
            raise UserNotExistsError("Sorry, this user does not exist!")
        if not Utils.check_hashed_password(password, user_data["password"]):
            raise InvalidPasswordError("Sorry, this password is invalid!")
        return True

    @staticmethod
    def register(email, password):
        user_data = Database.find_one("users", {"email": email})
        if user_data is not None:
            raise UserAlreadyExistsError("Sorry, this user already exists!")
        if not Utils.valid_email(email):
            raise InvalidEmailAddressError("Please enter valid email address!")
        User(email, Utils.hash_password(password)).save_user_data()
        return True

    def save_user_data(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one("users", {"email": email}))

    def get_alerts(self):
        return Alert.find_by_email(self.email)

