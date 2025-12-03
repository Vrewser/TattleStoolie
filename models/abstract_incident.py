from abc import ABC, abstractmethod


class AbstractIncident(ABC):
    """Abstract base class for ANY kind of incident."""

    def __init__(self, tip_id, tip_name, incident_type, location, description, urgency, created_by=None):
        self._id = tip_id
        self._tip_name = tip_name
        self._incident_type = incident_type
        self._location = location
        self._description = description
        self._urgency = urgency
        self._created_by = created_by

    # ---------- Encapsulation ----------
    @property
    def tip_name(self):
        return self._tip_name

    @tip_name.setter
    def tip_name(self, value):
        if len(value.strip()) < 3:
            raise ValueError("Tip name must be at least 3 characters.")
        self._tip_name = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if value.strip() == "":
            raise ValueError("Location cannot be empty.")
        self._location = value

    @abstractmethod
    def validate(self, incident_rules: dict) -> bool:
        """Validate based on rules loaded from Database."""
        pass

    @abstractmethod
    def display_summary(self) -> str:
        """Polymorphic display text."""
        pass

    def to_dict(self):
        return {
            "tip_name": self._tip_name,
            "incident_type": self._incident_type,
            "location": self._location,
            "description": self._description,
            "urgency": self._urgency,
            "created_by": self._created_by
        }