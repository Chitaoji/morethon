"""
Contains a tokenizer for uquant language: tokenize(), etc.

NOTE: this module is private. All functions and objects are available in the main
`uquant` namespace - use that instead.

"""

import re
from typing import Iterator, NamedTuple

__all__ = ["UqToken", "tokenize"]


class UqToken(NamedTuple):
    """Token for uquant language."""

    type: str
    value: str
    line: int


def tokenize(code: str) -> Iterator[UqToken]:
    """Tokenize the code."""
    keywords = {"using", "str", "field", "fac", "int", "float", "bool", "True", "False"}
    token_specification = [
        ("NUM", r"\d+(\.\d*)?"),  # Integer or decimal numbers
        ("DOUBLEARROW", r"=>"),  # Double arrows
        ("ARROW", r"->"),  # Arrows
        ("ASSIGN", r"="),  # Assignment operators
        ("END", r";"),  # Statement terminators
        ("ELLIPSIS", r"\.\.\."),  # Ellipsis
        ("ID", r"[A-Za-z._]+"),  # Identifiers
        ("OP", r"[+\-*/^]"),  # Arithmetic operators
        ("NEWLINE", r"\n"),  # Line endings
        ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
        ("COMMENT", r"#.*"),  # Comments
        ("LP", r"\("),  # Left parentheses
        ("RP", r"\)"),  # Right parentheses
        ("LS", r"\["),  # Left square brackets
        ("RS", r"\]"),  # Right square brackets
        ("LB", r"{"),  # Left braces
        ("RB", r"}"),  # Right braces
        ("DOUBLECOLON", r"::"),  # Double Colons
        ("COLON", r":"),  # Colons
        ("COMMA", r","),  # Commas
        ("TYPEJOIN", r"\$"),  # Type join
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    line_num = 1
    for m in re.finditer(tok_regex, code):
        ttype = m.lastgroup
        value = m.group()
        match ttype:
            case "NUM":
                value = float(value) if "." in value else int(value)
            case "ID" if value in keywords:
                ttype = value.upper()
            case "NEWLINE":
                line_num += 1
                continue
            case "SKIP":
                continue
            case "MISMATCH":
                raise RuntimeError(f"{value!r} unexpected on line {line_num}")
        yield UqToken(ttype, value, line_num)
