from eel.module_utils import EELModule, eel_function, eel_variable
import time

from eel.values import Number


class TimeModule(EELModule):
    @eel_function
    def curr_time(self):
        return Number(time.time())
