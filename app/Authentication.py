import bcrypt
from flask import request


class ROLE:
    ADMIN = 1
    USER = 10


class User:
    username = None
    _password = None
    role = ROLE.USER

    def __init__(self, username, password, role=ROLE.USER):
        self.password = hash(password)
        self.username = username
        self.role = role

    def is_equal(self, user):
        if user.username == self.username:
            if user.password == self.password:
                return True
            else:
                return False
        else:
            return False


class Auth:
    _USERS = []
    _min_authorized_role = ROLE.ADMIN

    def __init__(self, min_authorized_role):
        self._min_authorized_role = min_authorized_role
        self._USERS.append(User('s.mahmoudi', '34443444', ROLE.ADMIN))
        self._USERS.append(User('h.azizabadi', 'ha12345678', ROLE.USER))

    def is_authenticated(self):
        username = request.args.get("username")
        password = request.args.get("password")
        stranger = User(username, password)

        for user in self._USERS:
            if user.is_equal(stranger) and user.role <= self._min_authorized_role:
                return True

        return False
