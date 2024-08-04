from eel.base import RTResult
from eel.errors import RTError
from eel.module_utils import EelModule, eel_function, eel_variable
import json

from eel.values import Number, Null, Dictionary, String, Boolean


class JsonModule(EelModule):
    @staticmethod
    @eel_function
    def load(text):
        return RTResult().success(Dictionary(json.loads(text)))

    @staticmethod
    @eel_function
    def dump(dict_):
        py_dict = {}

        for key, value in dict_.items.items():
            if isinstance(key, String) or isinstance(key, Number) or isinstance(key, Boolean):
                safe_key = key.value

            elif isinstance(key, Null):
                safe_key = None

            else:
                return RTResult().failure(
                    RTError(
                        "Invalid Json Serializable Key",
                        None, None
                    )
                )

            py_dict[safe_key] = value

        return RTResult().success(String(json.dumps(py_dict)))


JsonModule.initialize()
