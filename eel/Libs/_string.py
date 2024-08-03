from eel.base import RTResult
from eel.errors import RTError
from eel.module_utils import EelModule, eel_function, eel_variable
import string

from eel.values import Number, Null, Dictionary, String, Boolean


class StringModule(EelModule):
    @staticmethod
    @eel_variable
    def ascii_letters(text):
        return RTResult().success(String(string.ascii_letters))

    @staticmethod
    @eel_variable
    def ascii_lowercase(text):
        return RTResult().success(String(string.ascii_lowercase))

    @staticmethod
    @eel_variable
    def ascii_uppercase(text):
        return RTResult().success(String(string.ascii_uppercase))

    @staticmethod
    @eel_variable
    def digits(text):
        return RTResult().success(String(string.digits))

    @staticmethod
    @eel_variable
    def hex_digits(text):
        return RTResult().success(String(string.hexdigits))

    @staticmethod
    @eel_variable
    def oct_digits(text):
        return RTResult().success(String(string.octdigits))

    @staticmethod
    @eel_variable
    def punctuation(text):
        return RTResult().success(String(string.punctuation))

    @staticmethod
    @eel_variable
    def printable(text):
        return RTResult().success(String(string.printable))

    @staticmethod
    @eel_variable
    def hex_digits(text):
        return RTResult().success(String(string.whitespace))


StringModule.initialize()
