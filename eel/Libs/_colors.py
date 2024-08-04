from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import colorsys

from eel.values import Number, Null, String, BaseType, List


class ColorsModule(EelModule):
    @staticmethod
    @eel_function
    def rgb_to_yiq(r, g, b):
        return RTResult().success(List(colorsys.rgb_to_yiq(r.value, g.value, b.value)))

    @staticmethod
    @eel_function
    def yiq_to_rgb(y, i, q):
        return RTResult().success(List(colorsys.yiq_to_rgb(y.value, i.value, q.value)))

    @staticmethod
    @eel_function
    def rgb_to_hls(r, g, b):
        return RTResult().success(List(colorsys.rgb_to_hls(r.value, g.value, b.value)))

    @staticmethod
    @eel_function
    def hls_to_rgb(h, l, s):
        return RTResult().success(List(colorsys.hls_to_rgb(h.value, l.value, s.value)))

    @staticmethod
    @eel_function
    def rgb_to_hsv(r, g, b):
        return RTResult().success(List(colorsys.rgb_to_hsv(r.value, g.value, b.value)))

    @staticmethod
    @eel_function
    def hsv_to_rgb(h, s, v):
        return RTResult().success(List(colorsys.hsv_to_rgb(h.value, s.value, v.value)))


ColorsModule.initialize()
