from eel.base import RTResult
from eel.errors import RTError
from eel.module_utils import EelModule, eel_function, eel_variable
import os

from eel.values import Number, Null, Dictionary, String, Boolean


class OSModule(EelModule):
    # TODO: OS Module is under development

    @staticmethod
    @eel_variable
    def load(text):
        return RTResult().success(String(os.name))

    @staticmethod
    @eel_function
    def get_uid():
        return RTResult().success(String(os.getuid()))

    @staticmethod
    @eel_function
    def system(command):
        return RTResult().success(String(os.system(command.value)))


OSModule.initialize()
