from datetime import datetime, timedelta

from routing import all_deadlines_met
from simulation import build_simulation, total_mileage


def parse_query_time(value):
    """Convert user input such as 10:15 AM into a timedelta."""
    parsed = datetime.strptime(value, "%I:%M %p")
    return timedelta(hours=parsed.hour, minutes=parsed.minute)


def format_time(value):
    if value is None:
        return "--"
    total_seconds = int(round(value.total_seconds()))
    hours = (total_seconds // 3600) % 24
    minutes = (total_seconds % 3600) // 60
    suffix = "AM" if hours < 12 else "PM"
    display_hour = hours % 12 or 12
    return f"{display_hour}:{minutes:02d} {suffix}"


def print_package(package, query_time):
    status = package.status_at(query_time)
    delivered = format_time(package.delivery_time) if status == "Delivered" else "--"
    print(
        f"ID {package.package_id:>2} | Truck {package.truck_id} | "
        f"{package.address:<20} | Deadline {package.deadline:<8} | "
        f"Status: {status:<10} | Delivered: {delivered}"
    )


def run_cli():
    package_table, trucks, _, _ = build_simulation()

    print("\nDelivery Route Optimizer")
    print("------------------------")
    for truck in trucks:
        print(
            f"Truck {truck.truck_id}: {truck.mileage:.1f} miles | "
            f"Departed {format_time(truck.departure_time)} | "
            f"Returned {format_time(truck.return_time)}"
        )

    print(f"Total mileage: {total_mileage(trucks):.1f} miles")
    print(f"All deadlines met: {all_deadlines_met(package_table)}")

    while True:
        print("\n1. Look up one package")
        print("2. View all packages at a time")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "3":
            break

        try:
            query_time = parse_query_time(input("Enter time (example: 10:15 AM): ").strip())
        except ValueError:
            print("Please use a time such as 10:15 AM.")
            continue

        if choice == "1":
            try:
                package_id = int(input("Enter package ID: ").strip())
            except ValueError:
                print("Package ID must be a number.")
                continue

            package = package_table.lookup(package_id)
            if package is None:
                print("Package not found.")
            else:
                print_package(package, query_time)

        elif choice == "2":
            for package in sorted(
                package_table.all_packages(),
                key=lambda item: item.package_id,
            ):
                print_package(package, query_time)
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    run_cli()
