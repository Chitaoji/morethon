"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from .tokenize import UqTokenizer

__all__ = ["UqParser"]


class UqParser:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.globals = {}
        self.tokenizer = UqTokenizer()

    def parse_code(self, code: str) -> None:
        """Parce the code."""
        self.tokenizer.parse_code(code)
