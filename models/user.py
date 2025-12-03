class User:
    def __init__(self, row):
        self._id = row["id"]
        self._username = row["username"]
        self._role = row.get("role", "reporter")

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def role(self):
        return self._role

    def is_admin(self):
        return self._role == "admin"

    def is_reporter(self):
        return self._role == "reporter"

    def is_viewer(self):
        return self._role == "viewer"


class Admin(User):
    pass


class Reporter(User):
    pass


class Viewer(User):
    pass