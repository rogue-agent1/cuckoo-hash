#!/usr/bin/env python3
"""cuckoo_hash - Cuckoo hashing with two hash functions."""
import sys
class CuckooHash:
    def __init__(self, size=16):
        self.size=size; self.t1=[None]*size; self.t2=[None]*size
    def _h1(self, key): return hash(key) % self.size
    def _h2(self, key): return (hash(key) * 2654435761) % self.size
    def insert(self, key, max_kicks=100):
        for _ in range(max_kicks):
            i=self._h1(key)
            if self.t1[i] is None: self.t1[i]=key; return True
            key, self.t1[i]=self.t1[i], key
            i=self._h2(key)
            if self.t2[i] is None: self.t2[i]=key; return True
            key, self.t2[i]=self.t2[i], key
        return False
    def lookup(self, key):
        return self.t1[self._h1(key)]==key or self.t2[self._h2(key)]==key
    def display(self):
        print("T1:", [x for x in self.t1 if x is not None])
        print("T2:", [x for x in self.t2 if x is not None])
if __name__=="__main__":
    ch=CuckooHash(8)
    for x in [10,22,31,4,15,28,17,88]: ch.insert(x)
    ch.display()
    for x in [10,99]: print(f"Lookup {x}: {ch.lookup(x)}")
