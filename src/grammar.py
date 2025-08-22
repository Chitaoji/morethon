"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import TYPE_CHECKING, Callable, NamedTuple, Self

from . import error
from .tokenize import UqTokenizer

if TYPE_CHECKING:
    from ._typing import VarType

__all__ = ["UqParser"]


class Field:
    """Uq field."""

    def __init__(self, *args):
        pass

    def set_factor(self) -> None:
        """Factor."""


class UqVar(NamedTuple):
    """Defines variables in uquant language."""

    name: str
    type: "VarType"
    value: Callable[[Self], Self] | Field | str | int | float | bool | None

    def astype(self, var_type: "VarType") -> Self:
        """As type."""
        if self.type == var_type:
            return self
        match var_type:
            case "FUNCTION" | "TYPE":
                error.invalid_type_trans(self, var_type)
            case "FIELD":
                if self.type in {"INT", "FLOAT", "BOOL"}:
                    new_value = Field(self.value)
                error.invalid_type_trans(self, var_type)
            case "FACTOR":
                if self.type in {"INT", "FLOAT", "BOOL", "FIELD"}:
                    new_value = Field(self.value)
                    new_value.set_factor()
                error.invalid_type_trans(self, var_type)
            case "STR":
                new_value = str(self.value)
            case "INT":
                if self.type in {"FLOAT", "BOOL"}:
                    new_value = int(self.value)
                error.invalid_type_trans(self, var_type)
            case "FLOAT":
                if self.type in {"INT", "BOOL"}:
                    new_value = float(self.value)
                error.invalid_type_trans(self, var_type)
            case "BOOL":
                new_value = bool(self.value)
        return UqVar(self.name, var_type, new_value)

    def is_function(self) -> bool:
        """Is function."""
        return self.type == "FUNCTION"

    def getval(self, arg: Self) -> Self:
        """Get value if is function."""
        return self.value(arg)


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.tokenizer = UqTokenizer()

    def exec(self, code: str) -> None:
        """Execute the code."""
        try:
            self.open_loop(code, {})
        except error.ErrorFromUq:
            pass

    def open_loop(self, code: str, glob: dict[str, UqVar]) -> UqVar:
        """Open-loop behaviour."""
        self.tokenizer.parse_code(code)
        local: dict[str, UqVar] = {}
        lastvar = UqVar("", "NULL", None)
        while token := self.tokenizer.next():
            match t := token.type:
                case "ID":
                    if token.value in glob or token.value in local:
                        lastvar = self.eval_var(local)
                    else:
                        local[token.value] = self.define_var(local)
                case "LPAR":
                    pass
                case "LSQUARE":
                    pass
                case "LBRACE":
                    pass
                case "STR" | "TYPE" | "FIELD" | "BOOL" | "INT" | "FLOAT" | "FACTOR":
                    name, var = self.force_type(t, local)
                    local[name] = var
                case "USING":
                    pass
                case "COMMENT":
                    pass
                case _:
                    error.unexpected_token(token)
        print(lastvar)
        return lastvar

    def force_type(
        self, var_type: "VarType", glob: dict[str, UqVar]
    ) -> tuple[str, UqVar]:
        """Compulsively transform the type."""
        return ..., ...

    def define_var(self, glob: dict[str, UqVar]) -> UqVar:
        """Define variable."""
        return ...

    def eval_var(self, glob: dict[str, UqVar]) -> UqVar:
        """Evaluate e."""
        return ...
