import csv

from package import Package


def normalize_address(address):
    """Normalize whitespace so package and distance-table addresses match."""
    return " ".join(address.strip().split())


def load_packages(filename, package_table):
    """Read package CSV rows and insert Package objects into the hash table."""
    with open(filename, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [header.strip() for header in reader.fieldnames]

        for row in reader:
            package = Package(
                package_id=row["Package ID"].strip(),
                address=normalize_address(row["Address"]),
                city=row["City"].strip(),
                state=row["State"].strip(),
                zip_code=row["Zip"].strip(),
                deadline=row["Deadline"].strip(),
                weight=row["Weight"].strip(),
                notes=row["Notes"].strip(),
            )
            package_table.insert(package.package_id, package)


def load_distances(filename):
    """Load a triangular distance matrix whose first column is the address."""
    addresses = []
    matrix = []

    with open(filename, encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row or not any(cell.strip() for cell in row):
                continue

            addresses.append(normalize_address(row[0]))
            distance_row = []

            for value in row[1:]:
                value = value.strip()
                distance_row.append(float(value) if value else None)

            matrix.append(distance_row)

    return addresses, matrix


def address_index(address, addresses):
    """Return the index of an address in the distance matrix."""
    normalized = normalize_address(address)
    return addresses.index(normalized)


def distance_between(address_a, address_b, addresses, distance_matrix):
    """Return distance between two addresses from either half of the matrix."""
    index_a = address_index(address_a, addresses)
    index_b = address_index(address_b, addresses)

    distance = distance_matrix[index_a][index_b]
    if distance is None:
        distance = distance_matrix[index_b][index_a]

    return distance
