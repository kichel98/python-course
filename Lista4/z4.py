# author: Piotr Andrzejewski
import math
from inspect import getfullargspec


class OverloadedFunction:
    declr_func = {}

    def __init__(self, fn):
        self.name = fn.__name__
        func_args = getfullargspec(fn).args
        OverloadedFunction.declr_func[(self.name, len(func_args))] = fn

    def __call__(self, *args, **kwargs):
        key = (self.name, len(args))
        return OverloadedFunction.declr_func[key](*args, **kwargs)


def overload(fn):
    return OverloadedFunction(fn)


@overload
def norm(x, y):
    return math.sqrt(x*x + y*y)


@overload
def norm(x, y, z):
    return abs(x) + abs(y) + abs(z)


print(f"norm(2,4) = {norm(2, 4)}")

print(f"norm(2,3,4) = {norm(2, 3, 4)}")
