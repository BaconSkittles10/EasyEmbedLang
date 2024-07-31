import os

from eel.base import RTResult
from eel.context import SymbolTable, Context
from eel.errors import RTError, ConversionError


class BaseType:
    def __init__(self):
        self.set_pos()
        self.set_context()
        self.type = "Type"

    def set_context(self, context=None):
        self.context = context
        return self

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subtracted_by(self, other):
        return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        return None, self.illegal_operation(other)

    def divided_by(self, other):
        return None, self.illegal_operation(other)

    def powered_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def and_with(self, other):
        return None, self.illegal_operation(other)

    def or_with(self, other):
        return None, self.illegal_operation(other)

    def xor_with(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def copy(self):
        raise NotImplementedError("No copy method defined")

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other:
            other = self

        return RTError(
            "Illegal Operation",
            self.pos_start, other.pos_end, self.context
        )


class Number(BaseType):
    def __init__(self, value: float | int):
        super().__init__()
        self.value = value
        self.type = "Number"

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    "Division by zero",
                    other.pos_start, other.pos_end,
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None

        else:
            return None, self.illegal_operation(other)

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value > other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def and_with(self, other):
        if isinstance(other, Number):
            return Boolean(self.value and other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def or_with(self, other):
        if isinstance(other, Number):
            return Boolean(self.value or other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def xor_with(self, other):
        if isinstance(other, Number):
            return Boolean(bool(self.value) + bool(other.value) == 1).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def notted(self):
        return Boolean(True if self.value == 0 else False).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


class Null(BaseType):
    def __init__(self):
        super().__init__()
        self.type = "Null"

    def copy(self):
        return Null().set_context(self.context).set_pos(self.pos_start, self.pos_end)

    def get_comparison_eq(self, other):
        return Boolean(True if isinstance(other, Null) else False).set_context(self.context), None

    def get_comparison_ne(self, other):
        return Boolean(True if not isinstance(other, Null) else False).set_context(self.context), None

    def __repr__(self):
        return "null"


class Boolean(Number):
    def __init__(self, value):
        super().__init__(bool(value))
        self.type = "Boolean"

    def copy(self):
        return Boolean(self.value).set_context(self.context).set_pos(self.pos_start, self.pos_end)

    def __repr__(self):
        return str(self.value).lower()


class String(BaseType):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.type = "String"

    def ord_sum(self):
        return sum([ord(c) for c in self.value])

    def added_to(self, other):
        if isinstance(other, String) or isinstance(other, Number):
            other_val = str(other.value)
            return String(self.value + other_val).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, String) or isinstance(other, Number):
            return Boolean(str(self.value) == str(other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, String) or isinstance(other, Number):
            return Boolean(str(self.value) != str(other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        if isinstance(other, String):
            return Boolean(self.ord_sum() < other.ord_sum()).set_context(self.context), None
        elif isinstance(other, Number):
            return Boolean(self.ord_sum() < other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        if isinstance(other, String):
            return Boolean(self.ord_sum() > other.ord_sum()).set_context(self.context), None
        elif isinstance(other, Number):
            return Boolean(self.ord_sum() > other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        if isinstance(other, String):
            return Boolean(self.ord_sum() <= other.ord_sum()).set_context(self.context), None
        elif isinstance(other, Number):
            return Boolean(self.ord_sum() <= other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        if isinstance(other, String):
            return Boolean(self.ord_sum() >= other.ord_sum()).set_context(self.context), None
        elif isinstance(other, Number):
            return Boolean(self.ord_sum() >= other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{str(self.value)}"'


class List(BaseType):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        self.type = "List"

    def added_to(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
        else:
            new_list = self.copy()
            new_list.elements.append(other)

        return new_list, None

    def subtracted_by(self, other):
        new_list = self.copy()
        new_list.elements = []
        for i, elem in enumerate(self.elements):
            if not (elem.type == other.type and elem.value == other.value):
                new_list.elements.append(elem)

        return new_list, None

    def multiplied_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            original_elements = self.copy().elements
            for i in range(other.value - 1):
                new_list.elements.extend(original_elements)

            return new_list, None
        else:
            return None, self.illegal_operation(other)

    def powered_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except IndexError:
                return None, RTError(
                    "Index Out of Bounds",
                    other.pos_start, other.pos_end, self.context
                )

        else:
            return None, self.illegal_operation(other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        self.set_context(self.context)
        return copy

    def __str__(self):
        return f"{', '.join([str(x) for x in self.elements])}"


    def __repr__(self):
        return f"[{', '.join([str(x) for x in self.elements])}]"


class BaseFunction(BaseType):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"
        self.type = "Function"

    def generate_new_context(self):
        local_context = Context(self.name, self.context, self.pos_start)
        local_context.symbol_table = SymbolTable(local_context.parent.symbol_table)
        return local_context

    def check_args(self, arg_names, args):
        from eel.base import RTResult
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                f"Too many args ({len(args) - len(arg_names)}) passed into '{self.name}'",
                self.pos_start, self.pos_end,
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                f"Too few args ({len(arg_names) - len(args)}) passed into '{self.name}'",
                self.pos_start, self.pos_end,
                self.context
            ))

        return res.success(Null())

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        from eel.base import RTResult
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, exec_ctx)

        return res.success(Null())

    def __repr__(self):
        return f"<function '{self.name}'>"


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        from eel.base import RTResult
        from eel.interpreter import Interpreter
        res = RTResult()
        interpreter = Interpreter()

        exec_ctx = self.generate_new_context()
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value is None:
            return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Null()
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return():
            return res

        return_value = res.register(method(exec_ctx))
        if res.should_return():
            return res

        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise NotImplementedError(f"No 'execute_{self.name}' method defined")

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    @staticmethod
    def add_builtin(arg_names: list | None = None, opt_arg_names: dict | None = None):
        if arg_names is None:
            arg_names = []

        if opt_arg_names is None:
            opt_arg_names = {}

        def decorator(func):
            def wrapper(exec_ctx):
                kwargs = {name: exec_ctx.get_value(name) for name in arg_names}
                for arg_name, default_value in opt_arg_names.items():
                    kwargs[arg_name] = exec_ctx.symbol_table.get(arg_name, default_value)

                kwargs["__exec_ctx__"] = exec_ctx

                return func(**kwargs)

            # Attach argument names to the function
            func.arg_names = arg_names
            return wrapper

        return decorator

    ##################################################
    # Built-In Function Execute Methods
    # Note: kwargs contains the values passed, and exec_ctx
    ##################################################

    def execute_print(self, exec_ctx):
        print(exec_ctx.symbol_table.get("value"))
        return RTResult().success(Null())
    execute_print.arg_names = ["value"]

    def execute_input(self, exec_ctx):
        user_input = input("")
        return RTResult().success(String(user_input))
    execute_input.arg_names = []

    def execute_input_int(self, exec_ctx):
        while True:
            try:
                user_input = int(input())
                break
            except ValueError:
                print("Input must be an integer")
        return RTResult().success(Number(user_input))
    execute_input_int.arg_names = []

    def execute_input_float(self, exec_ctx):
        while True:
            try:
                user_input = float(input())
                break
            except ValueError:
                print("Input must be a float")
        return RTResult().success(Number(user_input))
    execute_input_float.arg_names = []

    def execute_clear(self, exec_ctx):
        os.system("cls" if os.name == "nt" else "clear")
        return RTResult().success(Null())
    execute_clear.arg_names = []

    def execute_is_num(self, exec_ctx):
        return RTResult().success(Boolean(isinstance(exec_ctx.symbol_table.get("value"), Number)))
    execute_is_num.arg_names = ["value"]

    def execute_is_str(self, exec_ctx):
        return RTResult().success(Boolean(isinstance(exec_ctx.symbol_table.get("value"), String)))
    execute_is_str.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        return RTResult().success(Boolean(isinstance(exec_ctx.symbol_table.get("value"), List)))
    execute_is_list.arg_names = ["value"]

    def execute_is_func(self, exec_ctx):
        return RTResult().success(Boolean(isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)))
    execute_is_func.arg_names = ["value"]

    def execute_ls_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")
        index = -1  # kwargs.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "First argument of 'append' must be a list",
                self.pos_start, self.pos_end, exec_ctx
            ))

        list_.elements.append(value)

        return RTResult().success(Null())

    execute_ls_append.arg_names = ["list", "value"]

    def execute_ls_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "First argument of 'pop' must be a list",
                self.pos_start, self.pos_end, exec_ctx
            ))

        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                "Second argument of 'pop' must be a number",
                self.pos_start, self.pos_end, exec_ctx
            ))

        try:
            element = list_.elements.pop(index)
        except IndexError:
            return RTResult().failure(RTError(
                "Index out of bounds",
                self.pos_start, self.pos_end, exec_ctx
            ))

        return RTResult().success(element)
    execute_ls_pop.arg_names = ["list", "index"]

    def execute_ls_extend(self, exec_ctx):
        list1 = exec_ctx.symbol_table.get("list1")
        list2 = exec_ctx.symbol_table.get("list2")

        if not isinstance(list1, List):
            return RTResult().failure(RTError(
                "First argument of 'extend' must be a list",
                self.pos_start, self.pos_end, exec_ctx
            ))

        if not isinstance(list2, List):
            return RTResult().failure(RTError(
                "Second argument of 'extend' must be a list",
                self.pos_start, self.pos_end, exec_ctx
            ))

        list1.elements.extend(list2.elements)
        return RTResult().success(Null())

    execute_ls_extend.arg_names = ["list1", "list2"]

    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                "Argument must be list",
                self.pos_start, self.pos_end, exec_ctx
            ))

        return RTResult().success(Number(len(list_.elements)))

    execute_len.arg_names = ["list"]

    def execute_run(self, exec_ctx):  # TODO: Use this as a basis for import
        fn = exec_ctx.symbol_table.get("fn")

        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                "Argument must be string",
                self.pos_start, self.pos_end, exec_ctx
            ))

        fn = fn.value

        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                f"Failed to load script \"{fn}\"\n" + str(e),
                self.pos_start, self.pos_end, exec_ctx
            ))

        from eel.main import run
        _, error = run(fn, script)
        if error:
            return RTResult().failure(RTError(
                f"Failed to finish executing sscript \"{fn}\"\n" + error.as_string(),
                self.pos_start, self.pos_end, exec_ctx
            ))

        return RTResult().success(Null())

    execute_run.arg_names = ["fn"]


BuiltInFunction.print =         BuiltInFunction("print")
BuiltInFunction.input =         BuiltInFunction("input")
BuiltInFunction.input_int =     BuiltInFunction("input_int")
BuiltInFunction.input_float =   BuiltInFunction("input_float")
BuiltInFunction.clear =         BuiltInFunction("clear")
BuiltInFunction.is_num =        BuiltInFunction("is_num")
BuiltInFunction.is_str =        BuiltInFunction("is_str")
BuiltInFunction.is_list =       BuiltInFunction("is_list")
BuiltInFunction.is_func =       BuiltInFunction("is_func")
BuiltInFunction.ls_append =     BuiltInFunction("ls_append")
BuiltInFunction.ls_pop =        BuiltInFunction("ls_pop")
BuiltInFunction.ls_extend =     BuiltInFunction("ls_extend")
BuiltInFunction.len =        BuiltInFunction("len")
BuiltInFunction.run =           BuiltInFunction("run")
