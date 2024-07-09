"""lexer module"""

from typing import List, Any

from .error import LexerError
from .token import Token, TokenKind

RESERVED_KEYWORDS = {
    "<EOL>": (TokenKind.EOL_VAR, "\n")
}

def is_identifier_char(char: str) -> bool:
    """Return if the char is allowed for an identifier

    Args:
        char (str): A character

    Returns:
        bool: Is the character allowed
    """
    return char.isalnum() or char in "-_"

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
        """Returns if the current cursor has reached the end of the file

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

    def __error(self, message: str) -> LexerError:
        """Return a custom exception for the lexer errors

        Args:
            message (str): An error message

        Returns:
            LexerError: A LexerError instance
        """

        return LexerError.error(self.__line, message)

    def __assign(self):
        """Manage an assign token
        """

        is_matched = self.__match(":") \
            and self.__match("=")

        if not is_matched:
            raise self.__error("Invalid assigment characters sequence")

        self.__add_token(TokenKind.ASSIGN)

    def __identifier(self):
        """Manage an identifie token
        """

        while (c := self.__peek()) != ">":
            if self.__is_at_end():
                raise self.__error("Unterminated identifier")

            if not is_identifier_char(c):
                raise self.__error("Unallowed character for identifier " + c)

            self.__advance()

        self.__advance()

        keyword = self.__source[self.__start:self.__current]

        if keyword in RESERVED_KEYWORDS:
            self.__add_token(*RESERVED_KEYWORDS[keyword])
            return

        self.__add_token(TokenKind.IDENTIFIER)

    def __string(self, start_char: str):
        """Manage a string token
        """

        while (c := self.__peek()) != start_char:
            if self.__is_at_end():
                raise self.__error("Unterminated string")

            if c == "\n":
                raise self.__error("Multiline string is not allowed")

            self.__advance()

        self.__advance()

        # Preventing double quotes being part of the string
        while self.__peek() == start_char:
            self.__advance()

        literal = self.__source[self.__start + 1:self.__current - 1]

        self.__add_token(TokenKind.STRING, literal)

    def __single_line_comment(self):
        """Manage a single line comment
        """

        while self.__peek() != "\n":
            self.__advance()

    def __scan(self):
        """Scan a token based on the current character
        """

        match (c := self.__advance()):
            case "|": self.__add_token(TokenKind.PIPE)
            case "(": self.__add_token(TokenKind.LEFT_PAREN)
            case ")": self.__add_token(TokenKind.RIGHT_PAREN)
            case "<": self.__identifier()
            case ":": self.__assign()
            case "\r" | "\t" | " ": pass
            case "\n":
                self.__add_token(TokenKind.EOL)
                self.__line += 1
            case ";": self.__single_line_comment()
            case "\"" | "'":
                self.__string(c)
            case _:
                raise self.__error("Invalid character " + c)

    def scan(self) -> List[Token]:
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
