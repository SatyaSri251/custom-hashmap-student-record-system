class Node:
    """Linked-list node used for separate chaining."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    """
    Custom hash table implementation.
    No Python dictionary is used for storage.
    Collision handling: separate chaining with linked lists.
    """

    LOAD_FACTOR_LIMIT = 0.75

    def __init__(self, capacity=8):
        self.capacity = max(4, capacity)
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        # Polynomial rolling-style hash. We intentionally do not use hash()
        # so the algorithm is deterministic for the demonstration.
        value = 0
        for char in str(key):
            value = (value * 31 + ord(char)) % self.capacity
        return value

    def put(self, key, value):
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                current.value = value
                return False  # updated

            current = current.next

        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

        if self.load_factor() > self.LOAD_FACTOR_LIMIT:
            self._resize()

        return True  # inserted

    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def contains(self, key):
        return self.get(key) is not None

    def remove(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        previous = None

        while current is not None:
            if current.key == key:
                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next
                self.size -= 1
                return current.value

            previous = current
            current = current.next

        return None

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity

        old_nodes = []
        for bucket in old_buckets:
            current = bucket
            while current is not None:
                old_nodes.append((current.key, current.value))
                current = current.next

        self.size = 0
        for key, value in old_nodes:
            self.put(key, value)

    def load_factor(self):
        return self.size / self.capacity

    def values(self):
        for bucket in self.buckets:
            current = bucket
            while current is not None:
                yield current.value
                current = current.next

    def bucket_snapshot(self):
        result = []
        for i in range(self.capacity):
            entries = []
            current = self.buckets[i]
            while current is not None:
                entries.append({
                    "key": current.key,
                    "name": getattr(current.value, "name", str(current.value))
                })
                current = current.next
            result.append({"index": i, "entries": entries})
        return result

    def hash_explanation(self, key):
        steps = []
        value = 0
        for char in str(key):
            previous = value
            value = (value * 31 + ord(char)) % self.capacity
            steps.append({
                "character": char,
                "ascii": ord(char),
                "previous": previous,
                "result": value
            })

        return {
            "key": str(key),
            "bucket": value,
            "capacity": self.capacity,
            "steps": steps,
            "collision_handling": "Separate chaining: multiple records in one bucket are connected through linked nodes."
        }
