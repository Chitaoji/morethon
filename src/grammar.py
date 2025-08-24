"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import TYPE_CHECKING, Callable, NamedTuple, Self

from . import error
from .tokenize import UqToken, UqTokenizer

if TYPE_CHECKING:
    from ._typing import VarType

__all__ = ["UqParser"]


class Field:
    """Uq field."""

    def __init__(self, *args):
        pass

    def record_as_factor(self) -> None:
        """Factor."""


class UqVar(NamedTuple):
    """Defines variables in uquant language."""

    name: str
    type: "VarType"
    value: Callable[[Self], Self] | Field | str | int | float | bool | None

    @classmethod
    def from_token(cls, token: UqToken) -> Self:
        """Init from token."""
        return cls("", token.type, token.value)

    @classmethod
    def default(cls) -> Self:
        """Return a default instance."""
        return cls("", "NULL", None)

    def astype(self, var_type: "VarType") -> Self:
        """As type."""
        if self.type == var_type:
            return self
        match var_type:
            case "FIELD" if self.type in {"INT", "FLOAT", "BOOL"}:
                new_value = Field(self.value)
            case "FACTOR" if self.type in {"INT", "FLOAT", "BOOL", "FIELD"}:
                new_value = Field(self.value)
                new_value.record_as_factor()
            case "STR":
                new_value = str(self.value)
            case "INT" if self.type in {"FLOAT", "BOOL"}:
                new_value = int(self.value)
            case "FLOAT" if self.type in {"INT", "BOOL"}:
                new_value = float(self.value)
            case "BOOL":
                new_value = bool(self.value)
            case _:
                error.invalid_type_trans(self, var_type)
        return UqVar(self.name, var_type, new_value)

    def is_function(self) -> bool:
        """Is self a function."""
        return self.type == "FUNCTION"

    def is_list(self) -> bool:
        """Is self a list."""
        return self.type == "LIST"

    def getres(self, arg: Self) -> Self:
        """Get value if is function."""
        if not self.is_function():
            error.not_a_function(self)
        return self.value(arg)

    def getval(self, arg: Self) -> Self:
        """Get value if is list."""
        if not self.is_list():
            error.not_a_list(self)
        return self.value(arg)


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.tokenizer = UqTokenizer()

    def exec(self, code: str) -> None:
        """Execute the code."""
        try:
            lastvar = self.open_loop(code, {})
            print(lastvar)
        except error.ErrorFromUq:
            pass

    def open_loop(self, code: str, glob: dict[str, UqVar]) -> UqVar:
        """Open-loop behaviour."""
        self.tokenizer.parse_code(code)
        local: dict[str, UqVar] = {}
        lastvar = UqVar.default()
        varinline: bool = False
        while token := self.tokenizer.next():
            area = glob | local
            match t := token.type:
                case "ID":
                    if varinline:
                        error.unexpected_token(token)
                    if token.value in area:
                        lastvar = self.eval_var(area[token.value], area)
                        varinline = True
                    else:
                        local[token.value] = lastvar = self.define_var(
                            token.value, area
                        )
                        varinline = True
                case "LPAR":
                    lastvar = self.in_parentheses(glob)
                    varinline = True
                case "LSQUARE":
                    raise NotImplementedError()
                case "LBRACE":
                    lastvar = self.in_braces(glob)
                    varinline = True
                case "STR" | "TYPE" | "FIELD" | "BOOL" | "INT" | "FLOAT" | "FACTOR":
                    name, var = self.force_type(t, area)
                    local[name] = lastvar = var
                    varinline = True
                case "USING":
                    raise NotImplementedError()
                case "COMMENT":
                    continue
                case "NEWLINE":
                    varinline = False
                case _:
                    error.unexpected_token(token)
        return lastvar

    def force_type(
        self, var_type: "VarType", glob: dict[str, UqVar]
    ) -> tuple[str, UqVar]:
        """Compulsively transform the type."""
        var_name = self.tokenizer.expect("ID").value
        var = self.define_var(var_name, glob)
        return var_name, var.astype(var_type)

    def define_var(self, var_name: str, glob: dict[str, UqVar]) -> UqVar:
        """Define variable."""
        raise NotImplementedError()
        token = self.tokenizer.next()
        match token.type:
            case "ID":
                raise NotImplementedError()
            case "ASSIGN":
                raise NotImplementedError()

    def eval_var(self, var: UqVar, glob: dict[str, UqVar]) -> UqVar:
        """Evaluate variable."""
        if var.is_function():
            token = self.tokenizer.next()
            match token.type:
                case "ID":
                    return self.eval_var(var.getres(glob[token.value]), glob)
                case "LPAR":
                    return var.getres(self.in_parentheses(glob))
                case "LBRACE":
                    return var.getres(self.in_braces(glob))
                case _:
                    error.unexpected_token(token)
        elif var.is_list():
            token = self.tokenizer.next()
            match token.type:
                case "LSQUARE":
                    return var.getval(self.in_squares(glob))
                case "INT":
                    return var.getval(UqVar.from_token(token))
                case _:
                    error.unexpected_token(token)
        return var

    def in_parentheses(self, glob: dict[str, UqVar]) -> UqVar:
        """Evaluate variable in parentheses."""
        raise NotImplementedError()

    def in_squares(self, glob: dict[str, UqVar]) -> UqVar:
        """Evaluate variable in square brackets."""
        raise NotImplementedError()

    def in_braces(self, glob: dict[str, UqVar]) -> UqVar:
        """Evaluate variable in braces."""
        raise NotImplementedError()
