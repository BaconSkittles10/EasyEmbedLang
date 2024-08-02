from eel.nodes import NumberNode, BinOpNode, UnaryOpNode, VarAccessNode, VarAssignNode, IfNode, ForNode, WhileNode, \
    FuncDefNode, CallNode, StringNode, ListNode, ReturnNode, ContinueNode, BreakNode, ImportNode, DictNode
from .tokens import *
from .errors import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if 0 <= self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                "Token cannot appear after previous token",
                self.current_tok.pos_start, self.current_tok.pos_end,
            ))
        return res

    ###########################################################################

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advance()
                self.advance()
                newline_count += 1

            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break

            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start, self.current_tok.pos_end.copy()
        ))

    # FIXME: For future debugging: see below
    """
        - Errors are not being shown
          This is possibly do to try_register returning None, and an action being done if the result is None
          Possibly check res.error after try_register like I would after register
    """

    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, "RETURN"):
            res.register_advance()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "CONTINUE"):
            res.register_advance()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "BREAK"):
            res.register_advance()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "IMPORT"):
            res.register_advance()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ImportNode(expr, pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
               "Expected 'RETURN', 'IMPORT', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                pos_start, self.current_tok.pos_end
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "VAR"):
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    "Expected Identifier",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            var_name = self.current_tok
            res.register_advance()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    "Expected '='",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res

            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"), (TT_KEYWORD, "XOR"))))
        if res.error:
            return res.failure(InvalidSyntaxError(
                "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))
        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, "NOT"):
            op_tok = self.current_tok
            res.register_advance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                "Expected int, float, identifier, '+', '-', 'NOT', '[', or '('",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in [TT_PLUS, TT_MINUS]:
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (TT_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()

            arg_nodes = []

            if self.current_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                        self.current_tok.pos_start, self.current_tok.pos_end
                    ))

                while self.current_tok.type == TT_COMMA:
                    res.register_advance()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        "Expected ',' or ')'",
                        self.current_tok.pos_start, self.current_tok.pos_end
                    ))

                res.register_advance()
                self.advance()

            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in [TT_INT, TT_FLOAT]:
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            pos_start = tok.pos_start
            res.register_advance()
            self.advance()

            if self.current_tok.type == TT_DUBCOL:
                res.register_advance()
                self.advance()
                if self.current_tok.type == TT_IDENTIFIER:
                    tok.value += "::" + self.current_tok.value
                    self.advance()

                else:
                    return res.failure(RTError("Expected identifier after '::'", pos_start, self.current_tok.pos_end))

            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    "Expected ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        elif tok.type == TT_LBRACKET:
            list_expr = res.register(self.list_expr())
            if res.error:
                return res

            return res.success(list_expr)

        elif tok.type == TT_LCURLY:
            dict_expr = res.register(self.dict_expr())
            if res.error:
                return res

            return res.success(dict_expr)

        elif tok.matches(TT_KEYWORD, "IF"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, "FOR"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, "WHILE"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, "FN"):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(

            "Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', or 'FN'",
            tok.pos_start, tok.pos_end,
        ))

    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LBRACKET:
            return res.failure(InvalidSyntaxError(
                "Expected '['",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_RBRACKET:
            res.register_advance()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                   "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.current_tok.type != TT_RBRACKET:
                return res.failure(InvalidSyntaxError(
                    "Expected ',' or ']'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            res.register_advance()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pos_start, self.current_tok.pos_end.copy()
        ))

    def dict_expr(self):
        res = ParseResult()
        items = {}
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LCURLY:
            return res.failure(InvalidSyntaxError(
                "Expected '{'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_RCURLY:
            res.register_advance()
            self.advance()
        else:
            k = res.register(self.expr())
            # res.register_advance()
            # self.advance()

            if self.current_tok.type == TT_COLON:
                res.register_advance()
                self.advance()
                v = res.register(self.expr())
                if res.error:
                    return res

            else:
                return res.failure(InvalidSyntaxError(
                    "Expected ':'",
                    pos_start, self.current_tok.pos_end
                ))

            items[k] = v

            if res.error:
                return res.failure(InvalidSyntaxError(
                    "Expected '}', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                k = res.register(self.expr())
                res.register_advance()
                self.advance()

                if self.current_tok.type == TT_COLON:
                    res.register_advance()
                    self.advance()
                    v = res.register(self.expr())
                    if res.error:
                        return res

                else:
                    return res.failure(InvalidSyntaxError(
                        "Expected ':'",
                        pos_start, self.current_tok.pos_end
                    ))

                items[k] = v

        if self.current_tok.type != TT_RCURLY:
            return res.failure(InvalidSyntaxError(
                "Expected ',' or '}'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        return res.success(DictNode(
            items,
            pos_start, self.current_tok.pos_end.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases("IF"))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_elif(self):
        return self.if_expr_cases("ELIF")

    def if_expr_else(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, "ELSE"):
            res.register_advance()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advance()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, "END"):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            "Expected 'END'",
                            self.current_tok.pos_start, self.current_tok.pos_end
                        )
                    )
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_elif_or_else(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, "ELIF"):
            all_cases = res.register(self.if_expr_elif())
            if res.error:
                return res
            cases, else_case = all_cases

        else:
            else_case = res.register(self.if_expr_else())
            if res.error:
                return res

        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                f"Expected '{case_keyword}'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "THEN"):
            return res.failure(InvalidSyntaxError(
                "Expected 'THEN'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, "END"):
                res.register_advance()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_elif_or_else())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_elif_or_else())
            if res.error:
                return res

            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FOR"):
            return res.failure(InvalidSyntaxError(
                "Expected 'FOR'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                "Expected identifier",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        var_name = self.current_tok
        res.register_advance()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                "Expected '='",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "TO"):
            return res.failure(InvalidSyntaxError(
                "Expected 'TO'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORD, "STEP"):
            res.register_advance()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, "THEN"):
            return res.failure(InvalidSyntaxError(
                "Expected 'THEN'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "END"):
                return res.failure(InvalidSyntaxError(
                    "Expected 'END'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            res.register_advance()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "WHILE"):
            return res.failure(InvalidSyntaxError(
                "Expected 'WHILE'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "THEN"):
            return res.failure(InvalidSyntaxError(
                "Expected 'THEN'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, "END"):
                return res.failure(InvalidSyntaxError(
                    "Expected 'END'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

            res.register_advance()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, body, False))

    def func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FN"):
            return res.failure(InvalidSyntaxError(
                "Expected 'FN'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advance()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    "Expected '('",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))
        else:
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    "Expected identifier or '('",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        res.register_advance()
        self.advance()
        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advance()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advance()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        "Expected identifier",
                        self.current_tok.pos_start, self.current_tok.pos_end
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advance()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    "Expected ',' or ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    "Expected identifier or ')'",
                    self.current_tok.pos_start, self.current_tok.pos_end
                ))

        res.register_advance()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advance()
            self.advance()

            body = res.register(self.expr())
            if res.error:
                return res

            return res.success(FuncDefNode(
                var_name_tok, arg_name_toks, body, True
            ))

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                "Expected '->' or NEWLINE",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, "END"):
            return res.failure(InvalidSyntaxError(
                "Expected 'END'",
                self.current_tok.pos_start, self.current_tok.pos_end
            ))

        res.register_advance()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok, arg_name_toks, body, False
        ))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.to_reverse_count = 0

    def register(self, res: "ParseResult"):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def register_advance(self):
        self.advance_count += 1

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
