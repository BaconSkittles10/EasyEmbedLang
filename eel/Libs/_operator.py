from eel.base import RTResult
from eel.errors import RTError
from eel.module_utils import EelModule, eel_function, eel_variable
import operator

from eel.values import Number, Null, Dictionary, String, Boolean


class OperatorModule(EelModule):
    @staticmethod
    @eel_function
    def lt(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_lt(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)

    @staticmethod
    @eel_function
    def gt(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_gt(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)

    @staticmethod
    @eel_function
    def lte(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_lte(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)

    @staticmethod
    @eel_function
    def gte(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_gte(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)

    @staticmethod
    @eel_function
    def eq(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_eq(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)

    @staticmethod
    @eel_function
    def ne(left, right):
        res = RTResult()
        comp_res, error = left.get_comparison_ne(right)
        if error:
            return res.failure(error)
        return res.success(comp_res)


OperatorModule.initialize()
