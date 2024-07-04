"""token module"""

from typing import Any
from enum import Enum
from dataclasses import dataclass

class TokenKind(Enum):
    """Represents every available token kinds
    """

    ASSIGN = "assign"
    COLON = "colon"
    PIPE = "pipe"
    LEFT_PAREN = "left_paren"
    RIGHT_PAREN = "right_paren"

    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"

    EOL = "eol"
    EOF = "eof"

@dataclass
class Token:
    """Represents a token
    """

    kind: TokenKind
    lexeme: str
    literal: Any = None
    line: int = -1

    def __str__(self) -> str:
        ret = str(self.kind) + " (" + self.lexeme + "')"

        if self.literal:
            ret += " " + str(self.literal)

        return ret

    def __eq__(self, o: "Token") -> bool:
        return self.kind == o.kind \
            and self.literal == o.literal \
            and self.lexeme == o.lexeme
