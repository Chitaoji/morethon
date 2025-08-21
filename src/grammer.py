"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from .error import unexpeted_token
from .tokenize import UqTokenizer

__all__ = ["UqParser"]


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.globals = {}
        self.tokenizer = UqTokenizer()

    def parse_code(self, code: str, glob: dict) -> None:
        """Parce the code."""
        self.tokenizer.parse_code(code)
        local = {}
        while token := self.tokenizer.next():
            match token.type:
                case "MISMATCH":
                    return unexpeted_token(token)
                case "ID":
                    if token.value in glob or token.value in local:
                        pass
