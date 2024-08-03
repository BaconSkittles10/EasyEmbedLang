import math
from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
from eel.values import Number


class MathModule(EelModule):
    @staticmethod
    @eel_variable
    def pi():
        return Number(math.pi)

    @staticmethod
    @eel_function
    def log(value):
        return RTResult().success(Number(math.log(value)))

    @staticmethod
    @eel_function
    def double(val: Number):
        return RTResult().success(Number(val.value * 2))

    @staticmethod
    @eel_function
    def square(val):
        return RTResult().success(Number(val.value ** 2))

    @staticmethod
    @eel_function
    def cube(val):
        return RTResult().success(Number(val.value ** 3))

    @staticmethod
    @eel_function
    def sqrt(val):
        return RTResult().success(Number(math.sqrt(val.value)))

    @staticmethod
    @eel_function
    def root(r, val):
        return RTResult().success(Number(math.pow(val.value, (1/r.value))))


MathModule.initialize()
