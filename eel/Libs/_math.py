import math
from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
from eel.values import Number, List


class MathModule(EelModule):
    @staticmethod
    @eel_variable
    def e():
        return Number(math.e)

    @staticmethod
    @eel_variable
    def inf():
        return Number(math.inf)

    @staticmethod
    @eel_variable
    def nan():
        return Number(math.nan)

    @staticmethod
    @eel_variable
    def pi():
        return Number(math.pi)

    @staticmethod
    @eel_variable
    def tau():
        return Number(math.tau)

    ######################################################################################

    @staticmethod
    @eel_function
    def acos(val: Number):
        return RTResult().success(Number(math.acos(val.value)))

    @staticmethod
    @eel_function
    def acosh(val: Number):
        return RTResult().success(Number(math.acosh(val.value)))

    @staticmethod
    @eel_function
    def asin(val: Number):
        return RTResult().success(Number(math.asin(val.value)))

    @staticmethod
    @eel_function
    def asinh(val: Number):
        return RTResult().success(Number(math.asinh(val.value)))

    @staticmethod
    @eel_function
    def atan(val: Number):
        return RTResult().success(Number(math.atan(val.value)))

    @staticmethod
    @eel_function
    def atan2(y: Number, x: Number):
        return RTResult().success(Number(math.atan2(y.value, x.value)))

    @staticmethod
    @eel_function
    def atanh(val: Number):
        return RTResult().success(Number(math.atanh(val.value)))

    @staticmethod
    @eel_function
    def ceil(val: Number):
        return RTResult().success(Number(math.ceil(val.value)))

    @staticmethod
    @eel_function
    def comb(n: Number, k: Number):
        return RTResult().success(Number(math.comb(n.value, k.value)))

    @staticmethod
    @eel_function
    def copysign(x: Number, y: Number):
        return RTResult().success(Number(math.copysign(x.value, y.value)))

    @staticmethod
    @eel_function
    def cos(val: Number):
        return RTResult().success(Number(math.cos(val.value)))

    @staticmethod
    @eel_function
    def cosh(val: Number):
        return RTResult().success(Number(math.cosh(val.value)))

    @staticmethod
    @eel_function
    def degrees(val: Number):
        return RTResult().success(Number(math.degrees(val.value)))

    @staticmethod
    @eel_function
    def dist(p: List, q: List):
        return RTResult().success(Number(math.dist(p.elements, q.elements)))

    @staticmethod
    @eel_function
    def double(val: Number):
        return RTResult().success(Number(val.value * 2))

    @staticmethod
    @eel_function
    def erf(val: Number):
        return RTResult().success(Number(math.erf(val.value)))

    @staticmethod
    @eel_function
    def erfc(val: Number):
        return RTResult().success(Number(math.erfc(val.value)))

    @staticmethod
    @eel_function
    def exp(val: Number):
        return RTResult().success(Number(math.exp(val.value)))

    @staticmethod
    @eel_function
    def expm1(val: Number):
        return RTResult().success(Number(math.expm1(val.value)))

    @staticmethod
    @eel_function
    def fabs(val: Number):
        return RTResult().success(Number(math.fabs(val.value)))

    @staticmethod
    @eel_function
    def factorial(val: Number):
        return RTResult().success(Number(math.factorial(val.value)))

    @staticmethod
    @eel_function
    def floor(val: Number):
        return RTResult().success(Number(math.floor(val.value)))

    @staticmethod
    @eel_function
    def fmod(x: Number, y: Number):
        return RTResult().success(Number(math.fmod(x.value, y.value)))

    @staticmethod
    @eel_function
    def frexp(val: Number):
        return RTResult().success(List(math.frexp(val.value)))

    @staticmethod
    @eel_function
    def fsum(val: List):
        return RTResult().success(Number(math.fsum(val.elements)))

    @staticmethod
    @eel_function
    def gamma(val: Number):
        return RTResult().success(Number(math.gamma(val.value)))

    @staticmethod
    @eel_function
    def gcd(num1: Number, num2: Number):
        return RTResult().success(Number(math.gcd(num1.value, num2.value)))

    @staticmethod
    @eel_function
    def hypot(*vals: Number):
        return RTResult().success(Number(math.hypot(*vals)))

    @staticmethod
    @eel_function
    def isclose(a: Number, b: Number):
        # TODO: Add optional args rel_tol, abs_tol
        # https://www.w3schools.com/python/ref_math_isclose.asp
        return RTResult().success(Number(math.isclose(a.value, b.value)))

    @staticmethod
    @eel_function
    def isfinite(val: Number):
        return RTResult().success(Number(math.isfinite(val.value)))

    @staticmethod
    @eel_function
    def isinf(val: Number):
        return RTResult().success(Number(math.isinf(val.value)))

    @staticmethod
    @eel_function
    def isnan(val):
        return RTResult().success(Number(math.isnan(val.value)))

    @staticmethod
    @eel_function
    def isqrt(val: Number):
        return RTResult().success(Number(math.isqrt(val.value)))

    @staticmethod
    @eel_function
    def ldexp(x: Number, i: Number):
        return RTResult().success(Number(math.ldexp(x.value, i.value)))

    @staticmethod
    @eel_function
    def lgamma(val: Number):
        return RTResult().success(Number(math.lgamma(val.value)))

    @staticmethod
    @eel_function
    def log(val: Number):
        return RTResult().success(Number(math.log(val.value)))

    @staticmethod
    @eel_function
    def log10(val: Number):
        return RTResult().success(Number(math.log10(val.value)))

    @staticmethod
    @eel_function
    def log1p(val: Number):
        return RTResult().success(Number(math.log1p(val.value)))

    @staticmethod
    @eel_function
    def log2(val: Number):
        return RTResult().success(Number(math.log2(val.value)))

    @staticmethod
    @eel_function
    def perm(val: Number):
        return RTResult().success(Number(math.perm(val.value)))

    @staticmethod
    @eel_function
    def pow(x: Number, y: Number):
        return RTResult().success(Number(math.pow(x.value, y.value)))

    @staticmethod
    @eel_function
    def prod(sequence: List):
        return RTResult().success(Number(math.prod(sequence.elements)))

    @staticmethod
    @eel_function
    def radians(val: Number):
        return RTResult().success(Number(math.radians(val.value)))

    @staticmethod
    @eel_function
    def remainder(x: Number, y: Number):
        return RTResult().success(Number(math.remainder(x.value, y.value)))

    @staticmethod
    @eel_function
    def root(r, val):
        return RTResult().success(Number(math.pow(val.value, (1 / r.value))))

    @staticmethod
    @eel_function
    def sin(val: Number):
        return RTResult().success(Number(math.sin(val.value)))

    @staticmethod
    @eel_function
    def sinh(val: Number):
        return RTResult().success(Number(math.sinh(val.value)))

    @staticmethod
    @eel_function
    def sqrt(val: Number):
        return RTResult().success(Number(math.sqrt(val.value)))

    @staticmethod
    @eel_function
    def tan(val: Number):
        return RTResult().success(Number(math.tan(val.value)))

    @staticmethod
    @eel_function
    def tanh(val: Number):
        return RTResult().success(Number(math.tanh(val.value)))

    @staticmethod
    @eel_function
    def trunc(val: Number):
        return RTResult().success(Number(math.trunc(val.value)))


MathModule.initialize()
