"""
Handles errors.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grammar import UqVar
    from .tokenize import UqToken

__all__ = ["unexpected_token", "illegal_token", "mismatched_token"]


def unexpected_token(token: "UqToken") -> None:
    """UqError."""
    UqSyntaxError(f"unexpected token {token.value!r} on line {token.lineno}").err()


def illegal_token(token: "UqToken") -> None:
    """UqError."""
    UqSyntaxError(f"illegal token {token.value!r} on line {token.lineno}").err()


def mismatched_token(token: "UqToken", token_value: str) -> None:
    """UqError."""
    UqSyntaxError(f"mismatched token {token_value!r} on line {token.lineno}").err()


def invalid_type_trans(var: "UqVar", var_type: str) -> None:
    """UqError."""
    UqTypeError(f"invalid type transform from {var.type} to {var_type}").err()


def not_a_function(var: "UqVar") -> None:
    """UqError."""
    UqTypeError(f"not a function: {var.name}").err()


def not_a_list(var: "UqVar") -> None:
    """UqError."""
    UqTypeError(f"not a list: {var.name}").err()


def variable_already_defined(var_name: str) -> None:
    """UqError."""
    UqKeyError(f"variable already defined: {var_name!r}").err()


def setting_namespace(namespace: str) -> None:
    """UqError."""
    UqKeyError(f"trying to set variable in namespace: {namespace!r}").err()


# ==============================================================================
#                                 Error types
# ==============================================================================


class ErrorFromUq(Exception):
    """Error raised by uq parser."""


class UqError:
    """Uq error base class."""

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def err(self) -> None:
        """Raise error."""
        print(f"{self.__class__.__name__[2:]}{self.msg}")
        raise ErrorFromUq()

    def print(self) -> None:
        """Print error message."""
        print(f"{self.__class__.__name__[2:]}{self.msg}")


class UqSyntaxError(UqError):
    """Syntax error."""


class UqValueError(UqError):
    """Value error."""


class UqTypeError(UqError):
    """Type error."""


class UqKeyError(UqError):
    """Key error."""
