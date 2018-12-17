from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        # hash the password given by the user with pbkdf2_sha512
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def check_hashed_password(password, hashed_password):
        # check that the password given by the user matches data in the database
        # password given by the user is encrypted with sha512
        # password in the database is encrypted with pbkdf2

        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def valid_email(email):
        email_pattern = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return True if email_pattern.match(email) else False
