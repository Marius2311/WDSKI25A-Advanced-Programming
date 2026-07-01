# Demo 1: Better algorithm

import timeit

data_list = list(range(1_000_000))
data_set  = set(data_list)
target = 999_999

t_list = timeit.timeit(lambda: target in data_list, number=100)
t_set  = timeit.timeit(lambda: target in data_set,  number=100)
print(f"list lookup (O(n)): {t_list:.4f}s")
print(f"set  lookup (O(1)): {t_set:.6f}s")

# Demo 2: Caching

from functools import lru_cache

def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

@lru_cache(maxsize=None)
def fib_cached(n):
    return n if n < 2 else fib_cached(n-1) + fib_cached(n-2)

print("no cache: ", timeit.timeit(lambda: fib(32), number=1))
print("lru_cache:", timeit.timeit(lambda: fib_cached(32), number=1))


# Demo 3: Generators

import sys

eager = [x*x for x in range(1_000_000)]   # builds the whole list in RAM
lazy  = (x*x for x in range(1_000_000))   # computes on demand

print(sys.getsizeof(eager), "bytes")
print(sys.getsizeof(lazy),  "bytes")