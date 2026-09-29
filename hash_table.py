class HashTable:
    """Custom hash table that resolves collisions with separate chaining."""

    def __init__(self, capacity=20):
        self.table = []
        for _ in range(capacity):
            self.table.append([])

    def _bucket_index(self, key):
        """Map a package ID to one bucket in the table."""
        return int(key) % len(self.table)

    def insert(self, key, package):
        """Insert a package or replace the package already stored for the key."""
        bucket = self.table[self._bucket_index(key)]

        for index, pair in enumerate(bucket):
            if pair[0] == int(key):
                bucket[index] = [int(key), package]
                return

        bucket.append([int(key), package])

    def lookup(self, key):
        """Return the package for a package ID, or None if no match exists."""
        bucket = self.table[self._bucket_index(key)]

        for stored_key, package in bucket:
            if stored_key == int(key):
                return package

        return None

    def all_packages(self):
        """Return all packages stored across all buckets."""
        result = []
        for bucket in self.table:
            for _, package in bucket:
                result.append(package)
        return result
