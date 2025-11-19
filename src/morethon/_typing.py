"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Literal

import loggings

loggings.warning("this module is not intended to be imported at runtime")

VarType = Literal[
    "FUNCTION",
    "STR",
    "TYPE",
    "NUM",
    "INT",
    "FLOAT",
    "BOOL",
    "LIST",
    "NULL",
]
TokenType = (
    VarType
    | Literal[
        "STRING",
        "NUM",
        "DOUBLEARROW",
        "TYPEASSIGN",
        "ASSIGN",
        "END",
        "ELLIPSIS",
        "ID",
        "OP",
        "NEWLINE",
        "SKIP",
        "COMMENT",
        "LPAR",
        "RPAR",
        "LSQUARE",
        "RSQUARE",
        "LBRACE",
        "RBRACE",
        "DOUBLECOLON",
        "COLON",
        "COMMA",
        "TYPEJOIN",
        "ILLEGAL",
        "USING",
        "TRUE",
        "FALSE",
        "NULL",
    ]
)
