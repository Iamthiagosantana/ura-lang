from enum import Enum

class TokenType(Enum):
    VAR = "VAR"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOL = "BOOL"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    EQUAL = "="

    LPAREN = "("
    RPAREN = ")"
    LKEY = "{"
    RKEY = "}"
    
    WHILE = "WHILE"

    GE = ">="
    GR = ">"
    LE = "<="
    LR = "<"
    EQ = "=="
    NEQ = "!="

    EOF = "EOF"