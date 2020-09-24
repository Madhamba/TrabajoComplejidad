import time


def measure_time(f):
    start = time.time()
    f()
    end = time.time()
    return end - start
