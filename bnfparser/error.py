"""error module"""

from typing import Type, TypeVar

from .token import Token, TokenKind

T = TypeVar('T', bound='BaseError')

class BaseError(Exception):
    """BNF Base exception with a custom message
    """

    @staticmethod
    def __report(line: int, where: str, message: str) -> str:
        """Returns error indications

        Args:
            line (int): Source line number
            where (str): Source location
            message (str): Error message

        Returns:
            str: Formatted error message
        """

        return f"[line {line}] Error {where}: {message}"

    @classmethod
    def error(cls: Type[T], line: int, message: str) -> T:
        """Wrapper for reporting an error

        Args:
            line (int): Source line number
            message (str): Error message

        Returns:
            T: An instance of the error class
        """

        message = cls.__report(line, "", message)

        return cls(message)

    @classmethod
    def error_token(cls: Type[T], token: Token, message: str) -> T:
        """Wrapper for reporting an error from a token

        Args:
            token (Token): Token
            message (str): Error message

        Returns:
            T: An instance of the error class
        """

        if token.kind == TokenKind.EOF:
            where = " at end"
        else:
            where = " at '" + token.lexeme + "'"

        message = cls.__report(token.line, where, message)

        return cls(message)

    def __init__(self, message: str = ""):
        self.message = message

        super().__init__(self.message)

class LexerError(BaseError):
    """Exception for the lexer
    """

class ParserError(BaseError):
    """Exception for the parser
    """

class VisitorError(BaseError):
    """Exception for the `Visitor` implementations
    """

class ExpressionError(BaseError):
    """Exception for a Expression
    """

class CoreError(BaseError):
    """Exception for a Core
    """
