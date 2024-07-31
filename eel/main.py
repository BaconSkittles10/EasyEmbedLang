import math

from eel.context import Context, SymbolTable
from eel.values import Number, BuiltInFunction, Null
from .base import Lexer
from .parser import Parser
from .interpreter import Interpreter

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("true", Number(1))
global_symbol_table.set("false", Number(0))

global_symbol_table.set("MATH_PI", Number(math.pi))

global_symbol_table.set("PRINT", BuiltInFunction.print)
global_symbol_table.set("INPUT", BuiltInFunction.input)
global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
global_symbol_table.set("INPUT_FLOAT", BuiltInFunction.input_float)
global_symbol_table.set("CLEAR", BuiltInFunction.clear)
global_symbol_table.set("IS_NUM", BuiltInFunction.is_num)
global_symbol_table.set("IS_STR", BuiltInFunction.is_str)
global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
global_symbol_table.set("IS_FUNC", BuiltInFunction.is_func)
global_symbol_table.set("LS_APPEND", BuiltInFunction.ls_append)
global_symbol_table.set("LS_POP", BuiltInFunction.ls_pop)
global_symbol_table.set("LS_EXTEND", BuiltInFunction.ls_extend)
global_symbol_table.set("LEN", BuiltInFunction.len)
global_symbol_table.set("RUN", BuiltInFunction.run)


def run(fn, text, _import=False):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error:
        return None, error

    # generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # run program
    interpreter = Interpreter()
    if _import:
        context = Context("<_importer_>")
        context.symbol_table = global_symbol_table.copy()
    else:
        context = Context("<program>")
        context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error


def shell():
    while True:
        text = input("calc > ")
        if text.strip() == "":
            continue

        result, error = run("<stdin>", text)
        if error:
            error.alert()
        elif len(result.elements) == 1:
            if not isinstance(result.elements[0], Null):
                print(repr(result.elements[0]))
        else:
            print(repr(result))


if __name__ == "__main__":
    shell()
