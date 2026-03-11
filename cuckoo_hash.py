#!/usr/bin/env python3
"""cuckoo_hash — Cuckoo hashing with two hash functions. Zero deps."""
import hashlib

class CuckooHash:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.table1 = [None] * capacity
        self.table2 = [None] * capacity
        self.size = 0
        self.max_kicks = 500

    def _h1(self, key): return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.capacity
    def _h2(self, key): return int(hashlib.sha1(str(key).encode()).hexdigest(), 16) % self.capacity

    def insert(self, key, value):
        if self.get(key) is not None:
            # Update
            i1 = self._h1(key)
            if self.table1[i1] and self.table1[i1][0] == key:
                self.table1[i1] = (key, value); return True
            i2 = self._h2(key)
            if self.table2[i2] and self.table2[i2][0] == key:
                self.table2[i2] = (key, value); return True
        item = (key, value)
        for _ in range(self.max_kicks):
            i1 = self._h1(item[0])
            if self.table1[i1] is None:
                self.table1[i1] = item; self.size += 1; return True
            item, self.table1[i1] = self.table1[i1], item
            i2 = self._h2(item[0])
            if self.table2[i2] is None:
                self.table2[i2] = item; self.size += 1; return True
            item, self.table2[i2] = self.table2[i2], item
        self._rehash()
        return self.insert(item[0], item[1])

    def get(self, key):
        i1 = self._h1(key)
        if self.table1[i1] and self.table1[i1][0] == key: return self.table1[i1][1]
        i2 = self._h2(key)
        if self.table2[i2] and self.table2[i2][0] == key: return self.table2[i2][1]
        return None

    def delete(self, key):
        i1 = self._h1(key)
        if self.table1[i1] and self.table1[i1][0] == key:
            self.table1[i1] = None; self.size -= 1; return True
        i2 = self._h2(key)
        if self.table2[i2] and self.table2[i2][0] == key:
            self.table2[i2] = None; self.size -= 1; return True
        return False

    def _rehash(self):
        old1, old2 = self.table1, self.table2
        self.capacity *= 2
        self.table1 = [None] * self.capacity
        self.table2 = [None] * self.capacity
        self.size = 0
        for item in old1 + old2:
            if item: self.insert(item[0], item[1])

    def load_factor(self): return self.size / (2 * self.capacity)

def main():
    ch = CuckooHash(8)
    for i in range(20):
        ch.insert(f"key{i}", i * 10)
    print(f"Cuckoo Hash (cap={ch.capacity}, size={ch.size}, load={ch.load_factor():.1%}):")
    for i in range(0, 20, 5):
        print(f"  get(key{i}) = {ch.get(f'key{i}')}")
    ch.delete("key5")
    print(f"  After delete key5: {ch.get('key5')}")
    print(f"  Lookup O(1) guaranteed — max 2 table probes")

if __name__ == "__main__":
    main()
