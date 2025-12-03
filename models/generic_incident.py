from .abstract_incident import AbstractIncident


class GenericIncident(AbstractIncident):
    """Flexible incident type that adapts based on rules in DB."""

    def validate(self, incident_rules: dict) -> bool:
        """
        incident_rules example:
        {
           "min_description_length": 20
        }
        """
        min_len = incident_rules.get("min_description_length", 10)
        return len(self._description.strip()) >= min_len

    def display_summary(self) -> str:
        return f"[{self._incident_type.upper()}] {self._tip_name} — {self._location} ({self._urgency})"