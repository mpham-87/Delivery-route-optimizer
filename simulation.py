from datetime import timedelta
from pathlib import Path

from data_loader import load_distances, load_packages
from hash_table import HashTable
from routing import deliver_truck
from truck import Truck


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


TRUCK_1_PACKAGES = [1, 4, 12, 17, 26, 27, 29, 38]
TRUCK_2_PACKAGES = [2, 3, 5, 6, 7, 8, 10, 11, 13, 14, 15, 20, 23, 28, 32, 37]
TRUCK_3_PACKAGES = [9, 16, 18, 19, 21, 22, 24, 25, 30, 31, 33, 34, 35, 36, 39, 40]


def build_simulation():
    """Load data, run the three-truck simulation, and return all simulation objects."""
    package_table = HashTable(capacity=20)
    load_packages(DATA_DIR / "sample_packages.csv", package_table)
    addresses, distance_matrix = load_distances(DATA_DIR / "sample_distances.csv")

    truck1 = Truck(1, TRUCK_1_PACKAGES, timedelta(hours=8))
    truck2 = Truck(2, TRUCK_2_PACKAGES, timedelta(hours=8))

    deliver_truck(truck1, package_table, addresses, distance_matrix)
    deliver_truck(truck2, package_table, addresses, distance_matrix)

    # There are only two drivers. Truck 3 waits for the first returning driver
    # and also waits until the delayed packages are available at 9:05 AM.
    truck3_departure = max(
        min(truck1.return_time, truck2.return_time),
        timedelta(hours=9, minutes=5),
    )
    truck3 = Truck(3, TRUCK_3_PACKAGES, truck3_departure)
    deliver_truck(truck3, package_table, addresses, distance_matrix)

    trucks = [truck1, truck2, truck3]
    return package_table, trucks, addresses, distance_matrix


def total_mileage(trucks):
    return sum(truck.mileage for truck in trucks)
