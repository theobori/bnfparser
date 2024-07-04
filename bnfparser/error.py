"""error module"""

from sys import stderr

from .token import Token, TokenKind

class ParserError(Exception):
    """Exception for the parser
    """

class VisitorError(Exception):
    """Exception for the `Visitor` implementations
    """

class ExpressionError(Exception):
    """Exception for a `Visitor` implementation
    """


class Error:
    """It manages the Lox workflow
    """

    had_lexer_error = False

    @staticmethod
    def __report(line: int, where: str, message: str):
        """Write an error/indication on stdout for the user

        Args:
            line (int): Source line number
            where (str): Source location
            message (str): Error message
        """

        print("[line", str(line) + "] Error", where, ":", message, file=stderr)

        Error.had_lexer_error = True

    @staticmethod
    def error(line: int, message: str):
        """Wrapper for reporting an error

        Args:
            line (int): Source line number
            message (str): Error message
        """

        Error.__report(line, "", message)

    @staticmethod
    def error_token(token: Token, message: str):
        """Wrapper for reporting an error from a token

        Args:
            token (Token): Token
            message (str): Error message
        """

        if token.kind == TokenKind.EOF:
            where = " at end"
        else:
            where = " at '" + token.lexeme + "'"

        Error.__report(token.line, where, message)
