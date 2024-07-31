TT_INT          = "TT_INT"
TT_FLOAT        = "FLOAT"
TT_STRING       = "STRING"
TT_IDENTIFIER   = "IDENTIFIER"
TT_KEYWORD      = "KEYWORD"
TT_PLUS         = "PLUS"
TT_MINUS        = "MINUS"
TT_MUL          = "MUL"
TT_DIV          = "DIV"
TT_POW          = "POW"
TT_LPAREN       = "LPAREN"
TT_RPAREN       = "RPAREN"
TT_LBRACKET     = "LBRACKET"
TT_RBRACKET     = "RBRACKET"
TT_EQ           = "EQ"
TT_NE           = "NE"           # Not Equals
TT_EE           = "EE"           # Double Equals
TT_LT           = "LT"
TT_GT           = "GT"
TT_LTE          = "LTE"
TT_GTE          = "GTE"
TT_COMMA        = "COMMA"
TT_ARROW        = "ARROW"
TT_NEWLINE      = "NEWLINE"
TT_EOF          = "EOF"

KEYWORDS = [
    "VAR",

    "AND",
    "OR",
    "XOR",
    "NOT",

    "IF",
    "THEN",
    "ELIF",
    "ELSE",

    "FOR",
    "TO",
    "STEP",
    "WHILE",
    "CONTINUE",
    "BREAK",

    "FN",
    "RETURN",

    "IMPORT",

    "END"
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        self.pos_start = None
        self.pos_end = None

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
