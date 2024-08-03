from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import time

from eel.values import Number, Null


class TimeModule(EelModule):
    @staticmethod
    @eel_variable
    def curr_time():
        return Number(time.time())

    @staticmethod
    @eel_function
    def pause(duration_ms):
        time.sleep(duration_ms.value)
        return RTResult().success(Null())


TimeModule.initialize()
