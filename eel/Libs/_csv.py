from io import StringIO

from eel.base import RTResult
from eel.module_utils import EelModule, eel_function, eel_variable
import csv

from eel.values import Number, Null, String, BaseType, List, File


class CSVModule(EelModule):
    @staticmethod
    @eel_function
    def read(contents: String, delimiter: String = String(",")):
        file = StringIO(contents.value)
        res = []
        reader = csv.reader(file, delimiter=delimiter.value)
        for row in reader:
            new_row = []
            for thing in row:
                new_row.append(String(thing))

            res.append(List(new_row))

        res = List(res)
        return RTResult().success(res)


CSVModule.initialize()
