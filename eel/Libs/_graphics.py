from threading import Thread

from eel.base import RTResult
from eel.errors import RTError
from eel.module_utils import EelModule, eel_function, eel_variable
import tkinter as tk

from eel.values import Number, Null, Dictionary, String, Boolean


class GraphicsModule(EelModule):
    main_win = None
    running = False

    @staticmethod
    @eel_function
    def init_win(title):
        win = Window()
        win.title(title)
        GraphicsModule.main_win = win
        return RTResult().success(Null())

    @staticmethod
    @eel_function
    def mainloop():
        if GraphicsModule.main_win and not GraphicsModule.running:
            GraphicsModule.running = True
            Thread(target=GraphicsModule.main_win.mainloop()).start()
        return RTResult().success(Null())


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


GraphicsModule.initialize()
