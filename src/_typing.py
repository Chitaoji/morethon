"""
Contains typing classes.

NOTE: this module is not intended to be imported at runtime.

"""

from typing import Literal

import loggings

loggings.warning("this module is not intended to be imported at runtime")

ObjectType = Literal[
    "FUNCTION", "STR", "TYPE", "FIELD", "FACTOR", "INT", "FLOAT", "BOOL"
]
TokenType = (
    ObjectType
    | Literal[
        "NUM",
        "DOUBLEARROW",
        "ARROW",
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
        "OBJECT",
    ]
)
