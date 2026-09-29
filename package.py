from datetime import timedelta


class Package:
    """Represents one delivery package and its changing delivery state."""

    def __init__(
        self,
        package_id,
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        notes="",
    ):
        self.package_id = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = float(weight)
        self.notes = notes

        self.truck_id = None
        self.departure_time = None
        self.delivery_time = None

    def status_at(self, query_time):
        """Return this package's status at a specific simulated time."""
        if "Delayed until" in self.notes:
            delayed_time = self.notes.replace("Delayed until", "").strip()
            delayed_minutes = _time_string_to_timedelta(delayed_time)
            if query_time < delayed_minutes:
                return "Delayed"

        if self.departure_time is None or query_time < self.departure_time:
            return "At the hub"

        if self.delivery_time is None or query_time < self.delivery_time:
            return "En route"

        return "Delivered"

    def __repr__(self):
        return f"Package({self.package_id}, {self.address!r})"


def _time_string_to_timedelta(value):
    """Convert values such as '09:05 AM' into a timedelta from midnight."""
    from datetime import datetime

    parsed = datetime.strptime(value, "%I:%M %p")
    return timedelta(hours=parsed.hour, minutes=parsed.minute)
