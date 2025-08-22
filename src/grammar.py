"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from . import error
from .tokenize import UqTokenizer

__all__ = ["UqParser"]


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.globals = {}
        self.tokenizer = UqTokenizer()

    def exec(self, code: str) -> None:
        """Execute the code."""
        try:
            self.parse_code(code, {})
        except error.UqError:
            pass

    def parse_code(self, code: str, glob: dict) -> None:
        """Parse the code and save the result in glob dict."""
        self.tokenizer.parse_code(code)
        local = {}
        while token := self.tokenizer.next():
            match token.type:
                case "ILLEGAL":
                    error.illegal_token(token)
                case "ID":
                    if token.value in glob or token.value in local:
                        pass
