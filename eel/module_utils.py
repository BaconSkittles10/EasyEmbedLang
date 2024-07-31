from eel.values import Function


class EELModule:
    pass


def eel_function(func):
    func_name = func.__name__
    # TODO: Convert python modules to eel modules
    function_instance = Function(func_name, body_node, start_pos, end_pos)

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    wrapper._eel_function = function_instance

    return wrapper


def eel_variable(func):
    def wrapper():
        func()

    return wrapper
