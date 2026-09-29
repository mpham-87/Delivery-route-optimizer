from hash_table import HashTable


class DummyPackage:
    def __init__(self, package_id):
        self.package_id = package_id


def test_insert_and_lookup():
    table = HashTable(capacity=5)
    package = DummyPackage(1)
    table.insert(1, package)
    assert table.lookup(1) is package


def test_collision_separate_chaining():
    table = HashTable(capacity=5)
    first = DummyPackage(1)
    second = DummyPackage(6)  # 1 % 5 and 6 % 5 both map to bucket 1.
    table.insert(1, first)
    table.insert(6, second)
    assert table.lookup(1) is first
    assert table.lookup(6) is second
