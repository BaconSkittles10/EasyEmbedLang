class EelModuleMeta(type):

    def __new__(cls, name, bases, attrs):
        # Create the class
        new_class = super().__new__(cls, name, bases, attrs)

        # Apply decorators to methods after class creation
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                # Apply the eel_function decorator here
                attrs[attr_name] = eel_function(attr_value)

        # Ensure no instances can be created
        # new_class.__new__ = lambda s, *args, **kwargs: None
        return new_class


class EelModule(metaclass=EelModuleMeta):
    variables = {}
    functions = {}

    @classmethod
    def initialize(cls):
        for thing in dir(cls):
            thing = getattr(cls, thing)
            inst = None

            if hasattr(thing, "_eel_type"):
                match thing._eel_type:
                    case "var":
                        inst = EelVariable(thing)
                        cls.variables[thing.__name__] = inst

                    case "func":
                        inst = EelFunction(thing)
                        cls.functions[thing.__name__] = inst


def eel_function(func):
    func._eel_type = "func"
    return func


def eel_variable(func):
    func._eel_type = "var"
    return func


class EelFunction:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def set_context(self, _):
        pass


class EelVariable:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()
