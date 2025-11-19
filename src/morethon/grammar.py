"""
Processes the morethon abstract syntax grammar.

NOTE: this module is private. All functions and objects are available in the main
`morethon` namespace - use that instead.

"""

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, NamedTuple, Self

from . import error
from .tokenize import MoToken, MoTokenizer

if TYPE_CHECKING:
    from ._typing import VarType

__all__ = ["MoInterpreter"]


class MoDefinedType(NamedTuple):
    """Defines function type in morethon language."""

    require_type: "VarType" | Self | None
    return_type: "VarType" | Self

    def __eq__(self, value: Self, /) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return (
            self.require_type == value.require_type
            and self.return_type == value.return_type
        )


class MoFunc(NamedTuple):
    """Defines function in morethon language."""

    functype: MoDefinedType
    function: Callable[["MoVar"], "MoVar"]

    def eval(self, arg: "MoVar") -> "MoVar":
        """Evaluate."""
        return self.function(arg.force_type(self.functype))


@dataclass
class MoVar:
    """Defines variables in morethon language."""

    name: str
    type: "VarType"
    value: MoFunc | str | int | float | bool | None

    @classmethod
    def from_token(cls, token: MoToken) -> Self:
        """Init from token."""
        match token.type:
            case "NUM":
                if "." in token.value:
                    return cls("unspecified", "FLOAT", float(token.value))
                return cls("unspecified", "INT", int(token.value))
            case "STRING":
                return cls("unspecified", "STR", token.value[1:-1])
            case "TRUE":
                return cls("unspecified", "BOOL", True)
            case "FALSE":
                return cls("unspecified", "BOOL", False)
        return cls("unspecified", token.type, token.value)

    @classmethod
    def null(cls) -> Self:
        """Return a null instance."""
        return cls("null", "NULL", None)

    def force_type(self, var_type: "VarType" | MoDefinedType) -> Self:
        """Force to the type."""
        if isinstance(var_type, MoDefinedType):
            if var_type.require_type is None and self.type == var_type.return_type:
                return self
            if self.type == "FUNCTION" and self.value.functype == var_type:
                return self
            error.is_not_type(self, var_type)
        if not self.type == var_type:
            error.is_not_type(self, var_type)
        return self

    def is_function(self) -> bool:
        """Is self a function."""
        return self.type == "FUNCTION"

    def is_list(self) -> bool:
        """Is self a list."""
        return self.type == "LIST"

    def eval(self, arg: Self) -> Self:
        """Evaluate if is function."""
        if not self.is_function():
            error.not_a_function(self)
        return self.value.eval(arg)

    def getitem(self, arg: Self) -> Self:
        """Get item if is list."""
        if not self.is_list():
            error.not_a_list(self)
        return self.value.eval(arg)

    def setname(self, name: str) -> None:
        """Set name."""
        self.name = name


class MoNamespace(NamedTuple):
    """Defines namespaces in morethon language."""

    name: str
    variables: dict[str, MoVar]
    namespaces: dict[str, Self]

    def __contains__(self, key: str, /) -> bool:
        splited = re.split(r"::", key, maxsplit=1)
        if len(splited) == 1:
            return key in self.variables or key in self.namespaces
        sp, name = splited
        return sp in self.namespaces and name in self.namespaces[sp]

    def __getitem__(self, key: str, /) -> MoVar:
        if not key in self:
            error.not_defined(key)
        splited = re.split(r"::", key, maxsplit=1)
        if len(splited) == 1:
            if key in self.namespaces:
                error.getting_namespace(key)
            return self.variables[key]
        sp, name = splited
        return self.namespaces[sp][name]

    def __setitem__(self, key: str, /) -> MoVar:
        if "::" in key:
            splited = re.split(r"::", key, maxsplit=1)
            error.setting_namespace(splited[0])
        if key in self:
            error.already_defined(key)
        return self.variables[key]

    def new(self) -> Self:
        """Renew a namespace."""
        return self.__class__(self.name, self.variables.copy(), self.namespaces)


class MoInterpreter:
    """Processor for morethon language."""

    def __init__(self) -> None:
        self.tokenizer = MoTokenizer()

    def exec(self, code: str) -> None:
        """Execute the code."""
        self.tokenizer.parse_code(code)
        glob = MoNamespace("main", {}, {})
        try:
            lastvar = self.open_loop(glob)
            print(lastvar)
        except error.ErrorFromMo:
            pass

    def open_loop(self, glob: MoNamespace, inline: bool = False) -> MoVar:
        """Open-loop behaviour."""
        token = self.tokenizer.next()
        match t := token.type:
            case "ID" if token.value in glob:
                return self.eval_var(glob[token.value], glob)
            case "ID":
                if inline:
                    error.not_defined(token.value)
                return self.define_var(token.value, glob)
            case "LPAR":
                return self.in_parentheses(glob)
            case "LSQUARE":
                raise NotImplementedError(5)
            case "LBRACE":
                return self.in_braces(glob)
            case "STR" | "TYPE" | "FIELD" | "BOOL" | "INT" | "FLOAT" | "FACTOR":
                return self.force_type(t, glob)
            case "USING":
                raise NotImplementedError(6)
            case "COMMENT" | "NEWLINE" | "NULL":
                pass
            case "NUM" | "STRING" | "TRUE" | "FALSE":
                return MoVar.from_token(token)
            case _:
                error.unexpected_token(token)
        return MoVar.null()

    def force_type(self, var_type: "VarType", glob: MoNamespace) -> MoVar:
        """Compulsively transform the type."""
        var_name = self.tokenizer.expect("ID").value
        var = self.define_var(var_name, glob)
        return var.force_type(var_type)

    def define_var(self, var_name: str, glob: MoNamespace) -> MoVar:
        """Define variable."""
        while token := self.tokenizer.next():
            match token.type:
                case "ID":
                    raise NotImplementedError(1)
                case "ASSIGN":
                    var = self.open_loop(glob, inline=True)
                    var.setname(var_name)
                    return var
                case "NEWLINE":
                    break
                case _:
                    error.unexpected_token(token)
        error.not_defined(var_name)

    def eval_var(self, var: MoVar, glob: MoNamespace) -> MoVar:
        """Evaluate variable."""
        if var.is_function():
            token = self.tokenizer.next()
            match token.type:
                case "ID":
                    return self.eval_var(var.eval(glob[token.value]), glob)
                case "LPAR":
                    return var.eval(self.in_parentheses(glob))
                case "LBRACE":
                    return var.eval(self.in_braces(glob))
                case _:
                    error.unexpected_token(token)
        elif var.is_list():
            token = self.tokenizer.next()
            match token.type:
                case "LSQUARE":
                    return var.getitem(self.in_squares(glob))
                case "INT":
                    return var.getitem(MoVar.from_token(token))
                case _:
                    error.unexpected_token(token)
        return var

    def in_parentheses(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in parentheses."""
        raise NotImplementedError(2)

    def in_squares(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in square brackets."""
        raise NotImplementedError(3)

    def in_braces(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in braces."""
        raise NotImplementedError(4)
