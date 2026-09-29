from datetime import datetime, timedelta

from data_loader import distance_between


def time_to_timedelta(value):
    """Convert a 12-hour clock string to a timedelta from midnight."""
    parsed = datetime.strptime(value, "%I:%M %p")
    return timedelta(hours=parsed.hour, minutes=parsed.minute)


def deadline_value(package):
    """Convert a package deadline to a sortable simulated time."""
    if package.deadline.upper() == "EOD":
        return timedelta(hours=17)
    return time_to_timedelta(package.deadline)


def choose_next_package(truck, packages, addresses, distance_matrix):
    """
    Choose the next package with a deadline-aware nearest-neighbor heuristic.

    Earlier deadlines are considered first. When multiple packages share the
    same deadline, the closest address to the truck is selected.
    """
    return min(
        packages,
        key=lambda package: (
            deadline_value(package),
            distance_between(
                truck.current_address,
                package.address,
                addresses,
                distance_matrix,
            ),
        ),
    )


def deliver_truck(truck, package_table, addresses, distance_matrix):
    """Simulate deliveries until the truck has delivered every assigned package."""
    undelivered = [package_table.lookup(pid) for pid in truck.package_ids]

    for package in undelivered:
        package.truck_id = truck.truck_id
        package.departure_time = truck.departure_time

    while undelivered:
        next_package = choose_next_package(
            truck,
            undelivered,
            addresses,
            distance_matrix,
        )
        destination = next_package.address
        distance = distance_between(
            truck.current_address,
            destination,
            addresses,
            distance_matrix,
        )
        truck.travel(distance, destination)

        # Deliver every package on this truck that shares the destination.
        delivered_here = [
            package for package in undelivered if package.address == destination
        ]
        for package in delivered_here:
            package.delivery_time = truck.current_time
            undelivered.remove(package)

    return_distance = distance_between(
        truck.current_address,
        "HUB",
        addresses,
        distance_matrix,
    )
    truck.travel(return_distance, "HUB")
    truck.return_time = truck.current_time


def all_deadlines_met(package_table):
    """Return True only when every non-EOD package is delivered by its deadline."""
    for package in package_table.all_packages():
        if package.deadline.upper() == "EOD":
            continue
        if package.delivery_time is None or package.delivery_time > deadline_value(package):
            # A few floating-point seconds can appear from distance/time math.
            if package.delivery_time is None:
                return False
            difference = package.delivery_time - deadline_value(package)
            if difference.total_seconds() > 1:
                return False
    return True
