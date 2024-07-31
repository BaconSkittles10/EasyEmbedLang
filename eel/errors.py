from .utils import string_with_arrows

__all__ = [
    "Error",
    "IllegalCharError",
    "InvalidSyntaxError",
    "RTError",
    "ExpectedCharError"
]


class Error:
    def __init__(self, pos_start, pos_end, error_name, details, terminate=True):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.terminate = terminate

    def as_string(self):
        result = f"ERROR: {self.error_name}: {self.details}"
        result += f"\nFile: {self.pos_start.fn}, line: {self.pos_start.ln + 1}"
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def alert(self):
        if self.terminate:
            print(self.as_string())
            if self.pos_start.fn != "<stdin>":
                quit()
        else:
            print(self.as_string())


class IllegalCharError(Error):
    def __init__(self, details, start, end):
        super().__init__(start, end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    def __init__(self, details, start, end):
        super().__init__(start, end, "Invalid Syntax", details)


class RTError(Error):
    def __init__(self, details, start, end, context=None):
        super().__init__(start, end, "Runtime Error", details)

        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}\n'
        result += '\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result


class ExpectedCharError(RTError):
    def __init__(self, details, start, end, context=None):
        super().__init__(details, start, end, context)
        self.error_name = "Expected Char Error"


class ConversionError(RTError):
    def __init__(self, details, start, end, context=None):
        super().__init__(details, start, end, context)
        self.error_name = "Conversion Error"
