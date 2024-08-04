from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import webbrowser

from eel.values import Number, Null, String, BaseType, List, Boolean


class WebBrowserModule(EelModule):
    @staticmethod
    @eel_function
    def open(url: String, new=Number(0), autoraise=Boolean(True)):
        webbrowser.open(url.value, new.value, bool(autoraise.value))
        return RTResult().success(Null())

    @staticmethod
    @eel_function
    def open_new(url: String):
        webbrowser.open_new(url.value)
        return RTResult().success(Null())

    @staticmethod
    @eel_function
    def open_new_tab(url: String):
        webbrowser.open_new_tab(url.value)
        return RTResult().success(Null())


WebBrowserModule.initialize()
