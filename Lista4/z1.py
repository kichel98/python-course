# author: Piotr Andrzejewski
import time
import random


def measure_time(fn):
    def modified_fn(*args, **kwargs):
        start = time.time()
        return_val = fn(*args, **kwargs)
        end = time.time()
        print(end - start)
        return return_val
    return modified_fn


@measure_time
def foo(list_to_sort):
    return sorted(list_to_sort)


foo([random.randint(0, 74386743829) for _ in range(1000000)])
