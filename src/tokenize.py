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
        ("NUM", r"\d+(\.\d*)?"),  # Integer or decimal number
        ("ASSIGN", r"="),  # Assignment operator
        ("END", r";"),  # Statement terminator
        ("ID", r"[A-Za-z.]+"),  # Identifiers
        ("OP", r"[+\-*/^]"),  # Arithmetic operators
        ("NEWLINE", r"\n"),  # Line endings
        ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
        ("COMMENT", r"#.*"),  # Comments
        ("LP", r"\("),  # Left parentheses
        ("RP", r"\)"),  # Right parentheses
        ("LB", r"{"),  # Left braces
        ("RB", r"}"),  # Right braces
        ("COLON", r":"),  # Colons
        ("COMMA", r","),  # Commas
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


statements = """
using snaps

# 变量不可变，不可重复声明
a = 1 # int 
b = True # bool 
avg.price = (close + open) / 2 # field
mid.price = (ask1 + bid1) / 2 # field

# 类型自动推导
int c = 1.0 # int
bool d = False # bool
field e = 1 # field

# 定义函数
power: x, y = x ^ y # field a, b => a, b -> a ^ b
unsigned: f = {
    g: x, y = f(abs(x), y)
    g
} # field a, object b, c => (a, b -> c) -> (a, b -> c)

# 类型继承
# object
#   str
#   type
#   field
#     bool
#     int
#     float
# 例：object包含field，field包含int
# 若a与b均为类型，a ^ b表示两种类型的最小共同父类，field ^ int = field

# factor
# fac关键词定义的变量也是一个field，但在命名空间中会被强制添加'factor.'前缀，
# （其他关键词定义的变量名称中不得含有此前缀）
fac test = unsigned(power)(avg.price / mid.price - 1, 2) # field
"""

for token in tokenize(statements):
    print(token)
