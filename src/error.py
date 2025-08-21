"""
Handles errors.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tokenize import UqToken

__all__ = ["unexpeted_token"]


def unexpeted_token(token: "UqToken") -> None:
    """Unexpected token."""
    print(f"unexpected token {token.value!r} on line {token.lineno}")
