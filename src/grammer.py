"""
Processes the uquant abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from . import tokenize

__all__ = ["UqProcessor"]


class UqProcessor:
    """Processor for uquant language."""

    def __init__(self) -> None:
        self.globals = {}

    def process(self, code: str) -> None:
        """Process the code."""
        for token in tokenize.tokenize(code):
            print(token)
