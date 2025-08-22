"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import Callable, NamedTuple, Self

from . import error
from ._typing import ObjectType
from .tokenize import UqTokenizer

__all__ = ["UqParser"]


class UqObject(NamedTuple):
    """Object for uquant language."""

    name: str
    type: "ObjectType"
    value: Callable | str | int | float | bool | None

    def getval(self, arg: Self) -> Self:
        """Get value if is function."""
        return self.value(arg)

    def is_function(self) -> bool:
        """Is function."""
        return self.type == "FUNCTION"


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.tokenizer = UqTokenizer()

    def exec(self, code: str) -> None:
        """Execute the code."""
        try:
            self.open_loop(code, {})
        except error.UqError:
            pass

    def open_loop(self, code: str, glob: dict[str, UqObject]) -> None:
        """Open-loop behaviour."""
        self.tokenizer.parse_code(code)
        local: dict[str, UqObject] = {}
        while token := self.tokenizer.next():
            match token.type:
                case "ID":
                    if token.value in glob or token.value in local:
                        pass
                case "LPAR":
                    pass
                case "LSQUARE":
                    pass
                case "LBRACE":
                    pass
                case "STR":
                    pass
                case "TYPE":
                    pass
                case "FIELD":
                    pass
                case "BOOL":
                    pass
                case "INT":
                    pass
                case "FLOAT":
                    pass
                case "FAC":
                    pass
                case "USING":
                    pass
                case "COMMENT":
                    pass
                case _:
                    error.unexpected_token(token)
