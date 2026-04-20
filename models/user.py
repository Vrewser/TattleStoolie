class BaseUser:
    """Base repr for all users."""
    
    def __init__(self, row):
        self._id = row["id"]
        self._username = row["username"]
        self._email = row.get("email", "")
        self._role = row.get("role", "reporter")

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def role(self):
        return self._role

    def is_admin(self):
        return self._role == "admin"

    def is_reporter(self):
        return self._role == "reporter"

    def is_viewer(self):
        return self._role == "viewer"


class Admin(BaseUser):
    """Admin user with full system access."""
    
    def __init__(self, row):
        super().__init__(row)
        if not self.is_admin():
            raise ValueError(f"User {self._username} is not an admin")


class Reporter(BaseUser):
    """Reporter user who can submit tips."""
    
    def __init__(self, row):
        super().__init__(row)
        if not self.is_reporter():
            raise ValueError(f"User {self._username} is not a reporter")


class Viewer(BaseUser):
    """Viewer user with read-only access."""
    
    def __init__(self, row):
        super().__init__(row)
        if not self.is_viewer():
            raise ValueError(f"User {self._username} is not a viewer")


# Backward compatibility alias
User = BaseUser