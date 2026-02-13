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
        if self.functype.require_type is not None:
            arg = arg.force_type(self.functype.require_type)
        return self.function(arg)


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

    def force_type(self, var_type: "VarType | MoDefinedType") -> Self:
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
        if arg.type != "INT":
            error.is_not_type(arg, "INT")
        try:
            return self.value[arg.value]
        except (IndexError, TypeError):
            error.unexpected_token(MoToken("INT", str(arg.value), 1, ""))

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
        if key not in self:
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
        lastvar = MoVar.null()
        try:
            while True:
                value = self.open_loop(glob)
                if value.type == "NULL" and self.tokenizer.last_token.type == "NULL":
                    break
                if value.type != "NULL":
                    lastvar = value
            print(lastvar)
        except error.ErrorFromMo:
            pass

    def open_loop(self, glob: MoNamespace, inline: bool = False) -> MoVar:
        """Open-loop behaviour."""
        token = self.tokenizer.next()
        return self.open_from_token(token, glob, inline)

    def open_from_token(self, token: MoToken, glob: MoNamespace, inline: bool = False) -> MoVar:
        """Open-loop behaviour from current token."""
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
                return self.in_squares(glob)
            case "LBRACE":
                return self.in_braces(glob)
            case "STR" | "TYPE" | "FIELD" | "BOOL" | "INT" | "FLOAT" | "FACTOR":
                return self.force_type(t, glob)
            case "USING":
                while (token := self.tokenizer.next()) and token.type != "NEWLINE":
                    match token.type:
                        case "ID":
                            continue
                        case _:
                            error.unexpected_token(token)
                return MoVar.null()
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
        if var_name in glob:
            error.already_defined(var_name)
        params: list[str] = []
        while token := self.tokenizer.next():
            match token.type:
                case "ID":
                    params.append(token.value)
                case "ASSIGN":
                    if params:
                        var = MoVar(
                            var_name,
                            "FUNCTION",
                            self._make_function(var_name, params, glob),
                        )
                    else:
                        var = self.open_loop(glob, inline=True)
                        var = self.eval_expression(var, glob, {"NEWLINE", "RPAR", "RSQUARE", "RBRACE"})
                    var.setname(var_name)
                    glob.variables[var_name] = var
                    return var
                case "NEWLINE":
                    break
                case _:
                    error.unexpected_token(token)
        error.not_defined(var_name)

    def _make_function(self, var_name: str, params: list[str], glob: MoNamespace) -> MoFunc:
        """Build a curried function from parameters."""
        body = self.read_expr_tokens_until("NEWLINE")

        def build_layer(index: int, given: dict[str, MoVar]) -> MoFunc:
            param = params[index]

            def fn(arg: MoVar) -> MoVar:
                local_given = given | {param: arg}
                if index < len(params) - 1:
                    return MoVar(
                        f"{var_name}<{index+1}>",
                        "FUNCTION",
                        build_layer(index + 1, local_given),
                    )

                local = MoNamespace(var_name, glob.variables | local_given, glob.namespaces)
                old_tokenizer = self.tokenizer
                try:
                    self.tokenizer = MoTokenizer()
                    self.tokenizer.parse_code(body + "\n")
                    result = self.open_loop(local, inline=True)
                    return self.eval_expression(result, local, {"NEWLINE", "NULL"})
                finally:
                    self.tokenizer = old_tokenizer

            return MoFunc(MoDefinedType(None, "NULL"), fn)

        return build_layer(0, {})

    def eval_var(self, var: MoVar, glob: MoNamespace) -> MoVar:
        """Evaluate variable."""
        if var.is_function():
            token = self.tokenizer.next()
            match token.type:
                case "ID":
                    return self.eval_var(var.eval(glob[token.value]), glob)
                case "LPAR":
                    return self.eval_var(var.eval(self.in_parentheses(glob)), glob)
                case "LBRACE":
                    return self.eval_var(var.eval(self.in_braces(glob)), glob)
                case "NUM" | "STRING" | "TRUE" | "FALSE" | "LSQUARE":
                    return self.eval_var(var.eval(self.open_from_token(token, glob, inline=True)), glob)
                case _:
                    error.unexpected_token(token)
        elif var.is_list():
            token = self.tokenizer.next()
            match token.type:
                case "LSQUARE":
                    return var.getitem(self.in_index(glob))
                case "NUM":
                    return var.getitem(MoVar.from_token(token))
                case _:
                    error.unexpected_token(token)
        return var

    def eval_expression(self, left: MoVar, glob: MoNamespace, stops: set[str]) -> MoVar:
        """Evaluate left-associative binary expression."""
        while token := self.tokenizer.next():
            if token.type in stops | {"NULL"}:
                return left
            if token.type != "OP":
                error.unexpected_token(token)
            right = self.open_loop(glob, inline=True)
            left = self.apply_op(token.value, left, right)
        return left

    def apply_op(self, op: str, left: MoVar, right: MoVar) -> MoVar:
        """Apply numeric operators."""
        if left.type not in {"INT", "FLOAT", "BOOL"} or right.type not in {
            "INT",
            "FLOAT",
            "BOOL",
        }:
            error.unexpected_token(MoToken("OP", op, 1, ""))
        lvalue = float(left.value) if left.type == "FLOAT" or right.type == "FLOAT" else int(left.value)
        rvalue = float(right.value) if left.type == "FLOAT" or right.type == "FLOAT" else int(right.value)
        match op:
            case "+":
                value = lvalue + rvalue
            case "-":
                value = lvalue - rvalue
            case "*":
                value = lvalue * rvalue
            case "/":
                value = lvalue / rvalue
            case "^":
                value = lvalue**rvalue
            case _:
                error.unexpected_token(MoToken("OP", op, 1, ""))
        if isinstance(value, float) and value.is_integer() and left.type == right.type == "INT":
            return MoVar("unspecified", "INT", int(value))
        if isinstance(value, float) and not value.is_integer() or "/" == op:
            return MoVar("unspecified", "FLOAT", float(value))
        return MoVar("unspecified", "INT", int(value))

    def read_expr_tokens_until(self, stop: str) -> str:
        """Read tokens as expression source until stop token."""
        parts: list[str] = []
        depth = 0
        while token := self.tokenizer.next():
            if token.type in {"LPAR", "LSQUARE", "LBRACE"}:
                depth += 1
            elif token.type in {"RPAR", "RSQUARE", "RBRACE"}:
                depth -= 1
            if depth == 0 and token.type == stop:
                break
            parts.append(token.value)
        return " ".join(parts)

    def _consume_until(self, stop: str) -> None:
        while (token := self.tokenizer.next()) and token.type not in {stop, "NULL"}:
            continue

    def in_parentheses(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in parentheses."""
        value = self.open_loop(glob, inline=True)
        value = self.eval_expression(value, glob, {"RPAR"})
        if self.tokenizer.last_token.type != "RPAR":
            error.unexpected_token(self.tokenizer.last_token)
        return value


    def in_index(self, glob: MoNamespace) -> MoVar:
        """Evaluate list index in square brackets."""
        value = self.open_loop(glob, inline=True)
        value = self.eval_expression(value, glob, {"RSQUARE"})
        if self.tokenizer.last_token.type != "RSQUARE":
            error.unexpected_token(self.tokenizer.last_token)
        return value

    def in_squares(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in square brackets."""
        items: list[MoVar] = []
        token = self.tokenizer.next()
        if token.type == "RSQUARE":
            return MoVar("unspecified", "LIST", items)
        if token.type == "LSQUARE":
            value = self.in_squares(glob)
        else:
            value = self.open_from_token(token, glob, inline=True)
        items.append(value)
        while True:
            token = self.tokenizer.next()
            if token.type == "RSQUARE":
                break
            if token.type != "COMMA":
                error.unexpected_token(token)
            items.append(self.open_loop(glob, inline=True))
        return MoVar("unspecified", "LIST", items)

    def in_braces(self, glob: MoNamespace) -> MoVar:
        """Evaluate variable in braces."""
        local = glob.new()
        last = MoVar.null()
        while token := self.tokenizer.next():
            if token.type == "RBRACE":
                return last
            if token.type in {"COMMENT", "NEWLINE"}:
                continue
            last = self.open_from_token(token, local, inline=False)
            if last.type != "NULL":
                last = self.eval_expression(last, local, {"NEWLINE", "RBRACE"})
                if self.tokenizer.last_token.type == "RBRACE":
                    return last
        error.unexpected_token(self.tokenizer.last_token)
