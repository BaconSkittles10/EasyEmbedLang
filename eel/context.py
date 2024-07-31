class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable = SymbolTable()


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent is not None:
            return self.parent.symbols.get(name, None)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

    def copy(self):
        new = SymbolTable()
        new.parent = self
        return new


"""

calc > 1 * MATH_PI
3.141592653589793
calc > VAR pi = MATH_PI
3.141592653589793
calc > IS_NUM(pi)
true
calc > FN times_pi (num) -> num * MATH_PI
<function 'times_pi'>
calc > VAR ipt = INPUT_FLOAT
<built-in function input_float>
calc > VAR ipt = INPUT_FLOAT()"""
