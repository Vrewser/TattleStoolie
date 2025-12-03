from .generic_incident import GenericIncident


class IncidentFactory:
    """Factory used by the UI to create incidents dynamically."""

    def create_incident(self, tip_id, tip_name, incident_type, location, description, urgency, created_by):
        return GenericIncident(
            tip_id=tip_id,
            tip_name=tip_name,
            incident_type=incident_type,
            location=location,
            description=description,
            urgency=urgency,
            created_by=created_by
        )

    def create_incident_from_row(self, row):
        return GenericIncident(
            tip_id=row["id"],
            tip_name=row["tip_name"],
            incident_type=row["incident_type"],
            location=row["location"],
            description=row["description"],
            urgency=row["urgency"],
            created_by=row.get("created_by")
        )