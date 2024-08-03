import importlib.util
import inspect
import os
import pathlib
import sys

from eel.errors import RTError
from eel.module_utils import EelModule, EelModuleMeta, EelVariable, EelFunction
from eel.values import Number, Function, String, List, Null, Dictionary
from eel.tokens import *
from eel.base import RTResult


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise NotImplementedError(f"No visit method defined: 'visit_{type(node).__name__}'")

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_DictNode(self, node, context):
        res = RTResult()
        items = {}

        for k, v in node.items.items():
            k = res.register(self.visit(k, context))
            items[k] = res.register(self.visit(v, context))
            if res.should_return():
                return res

        return res.success(
            Dictionary(items).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        right = res.register(self.visit(node.right_node, context))

        result, error = None, None

        t = node.op_tok.type
        if t == TT_PLUS:
            result, error = left.added_to(right)

        elif t == TT_MINUS:
            result, error = left.subtracted_by(right)

        elif t == TT_MUL:
            result, error = left.multiplied_by(right)

        elif t == TT_DIV:
            result, error = left.divided_by(right)

        elif t == TT_MOD:
            result, error = left.mod_div_by(right)

        elif t == TT_POW:
            result, error = left.powered_by(right)

        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)

        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)

        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)

        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)

        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)

        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)

        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.and_with(right)

        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.or_with(right)

        elif node.op_tok.matches(TT_KEYWORD, "XOR"):
            result, error = left.xor_with(right)

        if error:
            return res.failure(error)
        else:
            return res.success(
                result.set_pos(node.pos_start, node.pos_end)
            )

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res

        error = None

        t = node.op_tok.type
        if t == TT_MINUS:
            number, error = number.multiplied_by(Number(-1))

        elif node.op_tok.matches(TT_KEYWORD, "NOT"):
            number, error = number.notted()

        if error:
            return res.failure(error)

        else:
            return res.success(
                number.set_pos(node.pos_start, node.pos_end)
            )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                f"'{var_name}' is not defined",
                node.pos_start, node.pos_end, context
            ))

        if isinstance(value, EelVariable):
            value = value()

        if isinstance(value, EelFunction):
            return res.success(value)

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return():
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return():
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return():
                    return res
                return res.success(Null() if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(self.visit(expr, context))
            if res.should_return():
                return res
            return res.success(Null() if should_return_null else else_value)

        return res.success(Null())

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return():
            return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return():
            return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return():
                return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value > 0:
            condition = lambda: i < end_value.value
        elif step_value.value < 0:
            condition = lambda: i > end_value.value
        else:
            condition = lambda: False

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null() if node.should_return_null else
            List(elements).set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return():
                return res

            if not condition.is_true():
                break

            value = res.register(self.visit(node.body_node, context))

            if res.should_return() and res.loop_should_continue is False and res.loop_should_break is False:
                return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            Null() if node.should_return_null else  # FIXME
            List(elements).set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return():
            return res

        if isinstance(value_to_call, EelFunction):
            for arg_node in node.arg_nodes:
                args.append(res.register(self.visit(arg_node, context)))
                if res.should_return():
                    return res

            return_value = res.register(value_to_call(*args))
            if res.should_return():
                return res
            return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

            return res.success(return_value)

        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return():
                return res
        else:
            value = Null()

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()

    def visit_ImportNode(self, node, context):
        res = RTResult()

        if node.fn_node:
            value = res.register(self.visit(node.fn_node, context))
            if res.should_return():
                return res
        else:
            value = Null()

        if isinstance(value, String):
            from eel import run

            fn = value.value + ".eel"

            if not os.path.isfile(fn):
                fn = os.path.join(pathlib.Path(__file__).parent.resolve(), "Libs", fn)

            if not os.path.isfile(fn):
                name = "_" + value.value + ".py"
                fn = os.path.join(pathlib.Path(__file__).parent.resolve(), "Libs", name)
                if os.path.isfile(fn):
                    # Handle python library

                    spec = importlib.util.spec_from_file_location(name, fn)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    classes = [
                        name for name, obj in mod.__dict__.items()
                        if isinstance(obj, type) and obj.__module__ == mod.__name__
                    ]

                    for class_name in classes:
                        obj = getattr(mod, class_name)

                        if isinstance(obj, EelModuleMeta):
                            eel_module = obj

                            prefix = value.value + "::"
                            for name, symbol_value in eel_module.variables.items():
                                c = symbol_value
                                context.symbol_table.set(prefix + name, c)

                            for name, symbol_value in eel_module.functions.items():
                                c = symbol_value
                                context.symbol_table.set(prefix + name, c)

                        return res.success(value)

                else:
                    return res.failure(RTError(f"Import Error: No module or local file named '{value.value}'", node.pos_start, node.pos_end, context))

            result, error = run(fn, open(fn).read(), True)
            prefix = value.value + "::"
            for name, symbol_value in result.context.symbol_table.symbols.items():
                c = symbol_value.copy()
                context.symbol_table.set(prefix + name, c)
                """if isinstance(node, Function):
                    context.symbol_table.set(prefix + name, c)
                elif isinstance(node, Number) or isinstance(node, String):
                    name = [name for name, val in node.context.symbol_table.symbols.items() if val == node]
                    if len(name) > 0:
                        name = name[0]
                    else:
                        return res.failure(RTError("Unknown Import Error", node.pos_start, node.pos_end, context))
                    context.symbol_table.set(prefix + name, c)"""

        return res.success(value)
