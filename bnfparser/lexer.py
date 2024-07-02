"""lexer module"""

from typing import List, Any

from .token import Token, TokenKind
from .error import Error

def is_allowed(char: str) -> bool:
    """Return if the char is allowed for an identifier

    Args:
        char (str): The character

    Returns:
        bool: Is the character allowed
    """
    return char.isalpha() or char in "-_"

class Lexer:
    """Lexing the source string, it parses into tokens
    """

    def __init__(self, source: str):
        self.__source = source

        self.__current = 0
        self.__start = self.__current
        self.__line = 1
        self.__tokens = []

    @property
    def source(self) -> str:
        """Return a copy of the source

        Returns:
            str: The source copy
        """

        return self.__source

    @property
    def tokens(self) -> List[Token]:
        """Return a copy of the token list

        Returns:
            List[Token]: Token list
        """

        return self.__tokens

    def __is_at_end(self) -> bool:
        """Returns is the current cursor has reached the end of the file

        Returns:
            bool: Has the current index is higher than the source size
        """

        return self.__current >= len(self.__source)

    def __peek(self, index: int=None) -> str:
        """Get a source character (`self.__current`) based on an index

        Args:
            index (int, optional): Index. Defaults to None.

        Returns:
            str: A source character
        """

        if self.__is_at_end():
            return "\0"

        if index is None:
            index = self.__current

        return self.__source[index]

    def __advance(self) -> str:
        """Move the current cursor to the next character
            and return the previous one

        Returns:
            str: The current character
        """

        char = self.__peek()

        self.__current += 1

        return char

    def __add_token(self, kind: TokenKind, literal: Any=None):
        """Add a token to the token list in function of the
            start and current cursors position

        Args:
            kind (TokenKind): Token kind
            literal (Any, optional): Token literal if it needs one. Defaults to None.
        """

        lexeme = self.__source[self.__start:self.__current]
        token = Token(kind, lexeme, literal, self.__line)

        self.__tokens.append(token)

    def __match(self, char: str) -> bool:
        """Check if a character match the current one, then go on the next

        Args:
            char (str): Char compared

        Returns:
            bool: Is equivalent
        """

        if self.__is_at_end():
            return False

        if self.__peek() != char:
            return False

        self.__current += 1

        return True

    def __assign(self) -> TokenKind:
        """Manage an assign token
        """

        is_matched = self.__match(":") \
            and self.__match("=")

        if not is_matched:
            Error.error(self.__line, "Invalid assigment characters sequence")
            return

        self.__add_token(TokenKind.ASSIGN)

    def __identifier(self) -> TokenKind:
        """Manage an identifie token
        """

        while self.__peek() != ">" or is_allowed(self.__peek()):
            if self.__is_at_end():
                Error.error(self.__line, "Unterminated identifier")
                return

            self.__advance()

        self.__advance()

        self.__add_token(TokenKind.IDENTIFIER)

    def __string(self):
        """Manage a string token
        """

        while self.__peek() != "\"":
            if self.__is_at_end():
                Error.error(self.__line, "Unterminated string")
                return

            if self.__peek() == "\n":
                Error.error(self.__line, "Multiline string is not allowed")
                return

            self.__advance()

        self.__advance()

        literal = self.__source[self.__start + 1:self.__current - 1]

        self.__add_token(TokenKind.STRING, literal)

    def __single_line_comment(self):
        """Manage a single line comment
        """

        while self.__peek() != "\n":
            self.__advance()

    def __scan(self):
        c = self.__advance()

        match c:
            case "|": self.__add_token(TokenKind.PIPE)
            case "(": self.__add_token(TokenKind.LEFT_PAREN)
            case ")": self.__add_token(TokenKind.RIGHT_PAREN)
            case "<": self.__identifier()
            case ":": self.__assign()
            case "\r" | "\t" | " ": pass
            case "\n":
                self.__line += 1
            case ";": self.__single_line_comment()
            case "\"":
                self.__string()
            case _:
                Error.error(self.__line, "Invalid character " + c)

    def scan_tokens(self) -> List[Token]:
        """Scan the source, it means it is going to convert the source into
        token list.

        Returns:
            List[Token]: Token list
        """

        while not self.__is_at_end():
            self.__start = self.__current

            self.__scan()

        # Add EOF token
        eof_token = Token(TokenKind.EOF, "", None, self.__line)
        self.__tokens.append(eof_token)

        return self.__tokens
