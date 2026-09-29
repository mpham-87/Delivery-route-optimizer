from datetime import datetime, timedelta

from data_loader import distance_between


TRUCK_SPEED_MPH = 18


def deadline_to_timedelta(deadline):
    """
    Convert a deadline string such as '09:00 AM'
    into a timedelta measured from midnight.

    EOD packages return None because they do not
    have a specific clock deadline.
    """
    if deadline == "EOD":
        return None

    deadline_clock = datetime.strptime(
        deadline,
        "%I:%M %p"
    )

    return timedelta(
        hours=deadline_clock.hour,
        minutes=deadline_clock.minute
    )


def route_priority(package, truck, addresses, distance_matrix):
    """
    Calculate the priority of a package.

    Packages with a specific deadline are handled before
    EOD packages.

    Among deadline packages, the algorithm calculates
    how much time would remain before the deadline if
    the truck delivered that package next.

    A smaller amount of remaining time means the package
    is more urgent.

    Distance is used as a tie-breaker.
    """

    distance = distance_between(
        truck.current_address,
        package.address,
        addresses,
        distance_matrix
    )

    travel_time = timedelta(
        hours=distance / TRUCK_SPEED_MPH
    )

    # EOD packages are lower priority than packages that have a specific delivery deadline.
    if package.deadline == "EOD":
        return (
            1,
            timedelta.max,
            distance
        )

    deadline = deadline_to_timedelta(
        package.deadline
    )

    estimated_arrival = (
        truck.current_time + travel_time
    )

    # Slack is the amount of time remaining before the deadline after arriving.
    slack = deadline - estimated_arrival

    return (
        0,
        slack,
        distance
    )


def deliver_truck(
    truck,
    package_table,
    addresses,
    distance_matrix
):
    """
    Deliver all packages assigned to one truck.

    Routing strategy:
    1. Load package objects from their package IDs.
    2. Start the truck at the hub.
    3. Prioritize deadline-sensitive packages.
    4. Among urgent packages, prefer the route with
       the smallest deadline slack.
    5. Use distance as a tie-breaker.
    6. Update package delivery times, truck mileage,
       route history, and truck time.
    7. Return the truck to the hub when complete.
    """

    undelivered_packages = []

    # Load package objects onto the truck.
  
    for package_id in truck.package_ids:
        package = package_table.lookup(
            package_id
        )

        if package is not None:
            undelivered_packages.append(
                package
            )

            # Record when the package leaves the hub.
            package.departure_time = (
                truck.departure_time
            )

 
    # Reset truck state before routing.
    truck.current_address = "HUB"
    truck.current_time = truck.departure_time
    truck.mileage = 0.0
    truck.route = ["HUB"]
    truck.return_time = None


    # Deliver all assigned packages.
    while undelivered_packages:

        # Choose the package with the highest urgency.
        next_package = min(
            undelivered_packages,
            key=lambda package: route_priority(
                package,
                truck,
                addresses,
                distance_matrix
            )
        )

        # Find the mileage to the selected address.
        distance = distance_between(
            truck.current_address,
            next_package.address,
            addresses,
            distance_matrix
        )

        # Add the mileage to the truck total.
        truck.mileage += distance

        # Convert distance into travel time.
        travel_time = timedelta(
            hours=distance / TRUCK_SPEED_MPH
        )

        # Advance the truck's simulated clock.
        truck.current_time += travel_time

        # Move the truck to the new address.
        truck.current_address = (
            next_package.address
        )

        # Record the route stop.
        truck.route.append(
            next_package.address
        )


        # Deliver every package at this address.
        packages_at_stop = []

        for package in undelivered_packages:
            if (
                package.address
                == next_package.address
            ):
                packages_at_stop.append(
                    package
                )

        for package in packages_at_stop:
            package.delivery_time = (
                truck.current_time
            )

            undelivered_packages.remove(
                package
            )


    # Return the truck to the hub.
    if truck.current_address != "HUB":

        return_distance = distance_between(
            truck.current_address,
            "HUB",
            addresses,
            distance_matrix
        )

        truck.mileage += return_distance

        return_travel_time = timedelta(
            hours=(
                return_distance
                / TRUCK_SPEED_MPH
            )
        )

        truck.current_time += (
            return_travel_time
        )

        truck.current_address = "HUB"
        truck.route.append("HUB")

    # Save the time the truck returned.
    truck.return_time = truck.current_time


def all_deadlines_met(package_table):
    """
    Return True if every non-EOD package
    was delivered on or before its deadline.
    """

    for package in package_table.all_packages():

        # EOD packages do not have a specific clock deadline.
        if package.deadline == "EOD":
            continue

        # A missing delivery time means the package was never delivered.
        if package.delivery_time is None:
            return False

        deadline_time = (
            deadline_to_timedelta(
                package.deadline
            )
        )

        if (
            package.delivery_time
            > deadline_time
        ):
            return False

    return True


def late_packages(package_table):
    """
    Return a list of packages that were
    delivered after their required deadline.

    This helper is useful for debugging
    and testing.
    """

    late = []

    for package in package_table.all_packages():

        if package.deadline == "EOD":
            continue

        if package.delivery_time is None:
            late.append(package)
            continue

        deadline_time = (
            deadline_to_timedelta(
                package.deadline
            )
        )

        if (
            package.delivery_time
            > deadline_time
        ):
            late.append(package)

    return late