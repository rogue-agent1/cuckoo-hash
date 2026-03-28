#!/usr/bin/env python3
"""cuckoo_hash - Cuckoo hashing implementation."""
import sys,hashlib
class CuckooHash:
    def __init__(s,size=16):s.size=size;s.t1=[None]*size;s.t2=[None]*size;s.count=0
    def _h1(s,key):return hash(key)%s.size
    def _h2(s,key):return int(hashlib.md5(str(key).encode()).hexdigest(),16)%s.size
    def insert(s,key,val):
        for _ in range(s.size):
            i=s._h1(key)
            if s.t1[i] is None:s.t1[i]=(key,val);s.count+=1;return True
            key,val,s.t1[i]=(s.t1[i][0],s.t1[i][1],(key,val))
            i=s._h2(key)
            if s.t2[i] is None:s.t2[i]=(key,val);s.count+=1;return True
            key,val,s.t2[i]=(s.t2[i][0],s.t2[i][1],(key,val))
        s._rehash();return s.insert(key,val)
    def get(s,key):
        i=s._h1(key)
        if s.t1[i] and s.t1[i][0]==key:return s.t1[i][1]
        i=s._h2(key)
        if s.t2[i] and s.t2[i][0]==key:return s.t2[i][1]
        return None
    def _rehash(s):
        old=[(k,v) for t in[s.t1,s.t2] for x in t if x for k,v in[x]]
        s.size*=2;s.t1=[None]*s.size;s.t2=[None]*s.size;s.count=0
        for k,v in old:s.insert(k,v)
if __name__=="__main__":
    ch=CuckooHash(8)
    for i in range(20):ch.insert(f"key{i}",i*10)
    for i in range(20):print(f"  key{i} → {ch.get(f'key{i}')}")
    print(f"Size: {ch.count}, Table size: {ch.size}")
