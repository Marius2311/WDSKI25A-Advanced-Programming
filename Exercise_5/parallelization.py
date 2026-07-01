import time

# Demo 1: Baseline

def cpu_task(n=50_000_000):
    """CPU-bound: pure computation, keeps a core 100% busy."""
    total = 0
    for i in range(n):
        total += i * i
    return total

def io_task(seconds=1):
    """I/O-bound: just waiting (simulates a network/DB call)."""
    time.sleep(seconds)

def timed(label, func, repeats):
    start = time.perf_counter()
    for _ in range(repeats):
        func()
    print(f"{label:<28}: {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    timed("4x CPU task (sequential)", cpu_task, 4)
    timed("4x I/O task (sequential)", io_task, 4)


# Demo 2: Threading for I/O

from concurrent.futures import ThreadPoolExecutor

def io_task(seconds=1):
    time.sleep(seconds)

if __name__ == "__main__":
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        pool.map(io_task, [1, 1, 1, 1])
    print(f"4x I/O with threads: {time.perf_counter() - start:.2f}s")


# Demo 3: Multiprocessing

from concurrent.futures import ProcessPoolExecutor

def cpu_task(n=50_000_000):
    total = 0
    for i in range(n):
        total += i * i
    return total

if __name__ == "__main__":
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(cpu_task, [50_000_000] * 4))
    print(f"4x CPU with processes: {time.perf_counter() - start:.2f}s")