from datetime import timedelta
from pathlib import Path

from data_loader import load_distances, load_packages
from hash_table import HashTable
from routing import deliver_truck
from truck import Truck


# Find the folder where this Python file is located.
BASE_DIR = Path(__file__).resolve().parent

# The CSV files are stored inside the data folder.
DATA_DIR = BASE_DIR / "data"

# PACKAGE ASSIGNMENTS
TRUCK_1_PACKAGES = [
    13,
    14,
    17,
    37,
    20,
    6,
    16,
    12,
    11,
    31,
    40,
    35,
    21,
    34,
    38,
    10
]


TRUCK_2_PACKAGES = [
    23,
    4,
    28,
    2,
    1,
    29,
    3,
    26
]


TRUCK_3_PACKAGES = [
    9,
    30,
    22,
    25,
    15,
    32,
    39,
    36,
    19,
    5,
    18,
    8,
    7,
    33,
    27,
    24
]


def build_simulation():
    """
    Load the package and distance data, create the trucks,
    run all delivery routes, and return the simulation data.
    """

    # -----------------------------------------------------
    # CREATE HASH TABLE
    # -----------------------------------------------------

    package_table = HashTable(capacity=20)


    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    load_packages(
        DATA_DIR / "sample_packages.csv",
        package_table
    )

    addresses, distance_matrix = load_distances(
        DATA_DIR / "sample_distances.csv"
    )


    # -----------------------------------------------------
    # CREATE TRUCK 1 AND TRUCK 2
    # -----------------------------------------------------
    #
    # There are two drivers available at 8:00 AM,
    # so these two trucks can leave immediately.
    #

    truck1 = Truck(
        1,
        TRUCK_1_PACKAGES,
        timedelta(hours=8)
    )

    truck2 = Truck(
        2,
        TRUCK_2_PACKAGES,
        timedelta(hours=8)
    )


    # -----------------------------------------------------
    # DELIVER TRUCK 1 AND TRUCK 2
    # -----------------------------------------------------

    deliver_truck(
        truck1,
        package_table,
        addresses,
        distance_matrix
    )

    deliver_truck(
        truck2,
        package_table,
        addresses,
        distance_matrix
    )


    # -----------------------------------------------------
    # DETERMINE WHEN TRUCK 3 CAN LEAVE
    # -----------------------------------------------------
    #
    # Only two drivers are available.
    #
    # Truck 3 must therefore wait until either Truck 1
    # or Truck 2 returns to the hub.
    #
    # Truck 3 also contains packages that are delayed
    # until 9:05 AM.
    #
    # Therefore, Truck 3 leaves at whichever time is later:
    #
    # 1. the first driver's return time
    # 2. 9:05 AM
    #

    first_driver_return = min(
        truck1.return_time,
        truck2.return_time
    )

    delayed_package_time = timedelta(
        hours=9,
        minutes=5
    )

    truck3_departure = max(
        first_driver_return,
        delayed_package_time
    )


    # -----------------------------------------------------
    # CREATE AND DELIVER TRUCK 3
    # -----------------------------------------------------

    truck3 = Truck(
        3,
        TRUCK_3_PACKAGES,
        truck3_departure
    )

    deliver_truck(
        truck3,
        package_table,
        addresses,
        distance_matrix
    )


    # Store all trucks together so other parts of the
    # program can easily access them.
    trucks = [
        truck1,
        truck2,
        truck3
    ]

    return (
        package_table,
        trucks,
        addresses,
        distance_matrix
    )


def total_mileage(trucks):
    """
    Return the combined mileage traveled by all trucks.
    """

    return sum(
        truck.mileage
        for truck in trucks
    )