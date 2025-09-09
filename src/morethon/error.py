"""
Handles errors.

NOTE: this module is private. All functions and objects are available in the main
`morethon` namespace - use that instead.

"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .grammar import MoVar
    from .tokenize import MoToken

__all__ = ["unexpected_token", "illegal_token", "mismatched_token"]


def unexpected_token(token: "MoToken") -> None:
    """Raises MoError."""
    MoSyntaxError(f"unexpected token {token.value!r} on line {token.lineno}").err()


def illegal_token(token: "MoToken") -> None:
    """Raises MoError."""
    MoSyntaxError(f"illegal token {token.value!r} on line {token.lineno}").err()


def mismatched_token(token: "MoToken", token_value: str) -> None:
    """Raises MoError."""
    MoSyntaxError(f"mismatched token {token_value!r} on line {token.lineno}").err()


def is_not_type(var: "MoVar", var_type: str) -> None:
    """Raises MoError."""
    MoTypeError(
        f"variable {var.name!r} is of type {var.type!r}, but not {var_type!r}"
    ).err()


def not_a_function(var: "MoVar") -> None:
    """Raises MoError."""
    MoTypeError(f"not a function: {var.name}").err()


def not_a_list(var: "MoVar") -> None:
    """Raises MoError."""
    MoTypeError(f"not a list: {var.name}").err()


def not_defined(var_name: str) -> None:
    """Raises MoError."""
    MoNameError(f"variable not defined yet: {var_name!r}").err()


def already_defined(var_name: str) -> None:
    """Raises MoError."""
    MoNameError(f"variable already defined: {var_name!r}").err()


def setting_namespace(namespace: str) -> None:
    """Raises MoError."""
    MoNameError(f"trying to set variable in namespace: {namespace!r}").err()


def getting_namespace(namespace: str) -> None:
    """Raises MoError."""
    MoNameError(f"is a namespace: {namespace!r}").err()


# ==============================================================================
#                                 Error types
# ==============================================================================


class ErrorFromMo(Exception):
    """Error raised by uq parser."""


class MoError:
    """Morethon error."""

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def err(self) -> None:
        """Raise error."""
        print(f"{self.__class__.__name__[2:]}: {self.msg}")
        raise ErrorFromMo()

    def print(self) -> None:
        """Print error message."""
        print(f"{self.__class__.__name__[2:]}: {self.msg}")


class MoSyntaxError(MoError):
    """Syntax error."""


class MoValueError(MoError):
    """Value error."""


class MoTypeError(MoError):
    """Type error."""


class MoNameError(MoError):
    """Key error."""
