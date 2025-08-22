"""
Handles errors.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokenize import UqToken

__all__ = ["unexpected_token", "illegal_token", "mismatched_token"]


def unexpected_token(token: "UqToken") -> None:
    """UqError."""
    print(f"unexpected token {token.value!r} on line {token.lineno}")
    raise UqError()


def illegal_token(token: "UqToken") -> None:
    """UqError."""
    print(f"illegal token {token.value!r} on line {token.lineno}")
    raise UqError()


def mismatched_token(token: "UqToken", token_value: str) -> None:
    """UqError."""
    print(f"mismatched token {token_value!r} on line {token.lineno}")
    raise UqError()


class UqError(Exception):
    """Error raised by uq language."""
