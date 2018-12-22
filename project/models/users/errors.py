class UserErrors(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(UserErrors):
    pass


class InvalidPasswordError(UserErrors):
    pass


class UserAlreadyExistsError(UserErrors):
    pass


class InvalidEmailAddressError(UserErrors):
    pass