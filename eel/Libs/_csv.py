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

    @staticmethod
    @eel_function
    def write(contents: List, delimiter: String = String(",")):
        with StringIO() as file:
            writer = csv.writer(file, delimiter=delimiter.value)
            friendly_contents = [[elem.value for elem in row.elements] for row in contents.elements]
            writer.writerows(friendly_contents)
            return RTResult().success(String(file.getvalue()))


CSVModule.initialize()
