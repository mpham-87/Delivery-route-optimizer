from datetime import timedelta


class Truck:
    """Stores the state of one delivery truck during the simulation."""

    SPEED_MPH = 18
    CAPACITY = 16

    def __init__(self, truck_id, package_ids, departure_time):
        if len(package_ids) > self.CAPACITY:
            raise ValueError(f"Truck {truck_id} exceeds the {self.CAPACITY}-package capacity.")

        self.truck_id = truck_id
        self.package_ids = list(package_ids)
        self.departure_time = departure_time
        self.current_time = departure_time
        self.current_address = "HUB"
        self.mileage = 0.0
        self.route = ["HUB"]
        self.return_time = None

    def travel(self, distance, destination):
        """Move the truck to a destination and update mileage and simulated time."""
        self.mileage += distance
        hours = distance / self.SPEED_MPH
        self.current_time += timedelta(hours=hours)
        self.current_address = destination
        self.route.append(destination)
