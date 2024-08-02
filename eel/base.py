# region Imports
import string

from .errors import *
from .tokens import *

# endregion

# region Constants

DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
IDENTIFIER_CHARS = LETTERS_DIGITS + "_"

# endregion

# region Position


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col

        self.fn = fn
        self.ftxt = ftxt

    def advance(self, curr_char=None):
        self.idx += 1
        self.col += 1

        if curr_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# endregion

# region Lexer


class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.fn = fn
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            curr_char = self.current_char
            match curr_char:
                case curr_char if curr_char in " \t":
                    self.advance()

                case "#":
                    self.skip_comment()

                case '"':
                    tokens.append(self.make_string())

                case "+":
                    tokens.append(Token(TT_PLUS, pos_start=self.pos))
                    self.advance()

                case "-":
                    tok_type = TT_MINUS
                    pos_start = self.pos.copy()
                    self.advance()

                    if self.current_char == ">":
                        self.advance()
                        tok_type = TT_ARROW

                    tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))

                case "*":
                    self.advance()
                    if self.current_char == "*":
                        tokens.append(Token(TT_POW, pos_start=self.pos))
                    else:
                        tokens.append(Token(TT_MUL, pos_start=self.pos))

                    self.advance()

                case "/":
                    tokens.append(Token(TT_DIV, pos_start=self.pos))
                    self.advance()

                case "^":
                    tokens.append(Token(TT_POW, pos_start=self.pos))
                    self.advance()

                case "%":
                    tokens.append(Token(TT_MOD, pos_start=self.pos))
                    self.advance()

                case "(":
                    tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                    self.advance()

                case ")":
                    tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                    self.advance()

                case "[":
                    tokens.append(Token(TT_LBRACKET, pos_start=self.pos))
                    self.advance()

                case "]":
                    tokens.append(Token(TT_RBRACKET, pos_start=self.pos))
                    self.advance()

                case "{":
                    tokens.append(Token(TT_LCURLY, pos_start=self.pos))
                    self.advance()

                case "}":
                    tokens.append(Token(TT_RCURLY, pos_start=self.pos))
                    self.advance()

                case "!":
                    tok, error = self.make_not_equals()
                    if error:
                        return [], error
                    tokens.append(tok)

                case "=":
                    tokens.append(self.make_equals())

                case "<":
                    tokens.append(self.make_less_than())

                case ">":
                    tokens.append(self.make_greater_than())

                case ",":
                    tokens.append(Token(TT_COMMA, pos_start=self.pos))
                    self.advance()

                case ":":
                    pos_start = self.pos
                    self.advance()

                    if self.current_char == ":":
                        tokens.append(Token(TT_DUBCOL, pos_start=pos_start, pos_end=self.pos))
                        self.advance()

                    else:
                        tokens.append(Token(TT_COLON, pos_start=pos_start))
                        # return [], IllegalCharError(f"'{self.current_char}'", pos_start, self.pos)

                case curr_char if curr_char in ";\n":
                    tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                    self.advance()

                case curr_char if curr_char in DIGITS:
                    tokens.append(self.make_number())

                case curr_char if curr_char in LETTERS:
                    tokens.append(self.make_identifier())

                case other:
                    pos_start = self.pos.copy()
                    self.advance()
                    return [], IllegalCharError(f"'{other}'", pos_start, self.pos)

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_string(self):
        str_ = ""
        pos_start = self.pos.copy()
        escape_char = False
        self.advance()

        escape_chars = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "b": "\b",
            "f": "\f",
        }

        while self.current_char is not None and (self.current_char != '"' or escape_char):
            if escape_char:
                str_ += escape_chars.get(self.current_char, self.current_char)
                escape_char = False
            else:
                if self.current_char == "\\":
                    escape_char = True
                else:
                    str_ += self.current_char
            self.advance()

        self.advance()
        return Token(TT_STRING, str_, pos_start, self.pos)

    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while (self.current_char is not None and
               self.current_char in DIGITS + "."):
            if self.current_char == ".":
                if dot_count == 1:
                    raise Exception("Too many dots in number")
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ""
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in IDENTIFIER_CHARS:
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError("Expected '=' after '!'",
                                       pos_start, self.pos)

    def make_equals(self):
        pos_start = self.pos.copy()
        tok_type = TT_EQ
        self.advance()

        if self.current_char == "=":  # Double Equals
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        pos_start = self.pos.copy()
        tok_type = TT_LT
        self.advance()

        if self.current_char == "=":  # Less Than / Equals
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        pos_start = self.pos.copy()
        tok_type = TT_GT
        self.advance()

        if self.current_char == "=":  # Greater Than / Equals
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.advance()

        while self.current_char != "\n":
            self.advance()

        self.advance()

# endregion

# region Misc


class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    """
        calc > FN multiline (a, b); VAR c = a + b; RETURN c * a * b;
        ERROR: Invalid Syntax: Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'
        File: <stdin>, line: 1
        
        FN multiline (a, b); VAR c = a + b; RETURN c * a * b;
                                                             ^
                                                             
        calc > FN multiline (a, b); VAR c = a + b; RETURN c * a * b; END
        ERROR: Invalid Syntax: Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FN', int, float, identifier, '+', '-', '(', '[' or 'NOT'
        File: <stdin>, line: 1
        
        FN multiline (a, b); VAR c = a + b; RETURN c * a * b; END
                                                              ^^^
        calc > multiline (1, 2)
        6
        
        So, I need END. If I use END, I get the syntax error, but the function still works.
    """

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        # Note: this will allow you to continue and break outside the current function
        return (
            self.error or
            self.func_return_value or
            self.loop_should_continue or
            self.loop_should_break
        )

# endregion
