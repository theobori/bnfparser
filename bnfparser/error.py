"""error module"""

from sys import stderr

from .token import Token, TokenKind

class ParserError(Exception):
    """
        Exception for the parser
    """

class Error:
    """
        It manages the Lox workflow
    """

    had_lexer_error = False
    # had_runtime_error = False

    @staticmethod
    def __report(line: int, where: str, message: str):
        """
            Write an error/indication on stdout for the user
        """

        print("[line", str(line) + "] Error", where, ":", message, file=stderr)

        Error.had_lexer_error = True

    @staticmethod
    def error(line: int, message: str):
        """
            Report an error
        """

        Error.__report(line, "", message)

    @staticmethod
    def error_token(token: Token, message: str):
        """
            Report an error based on a token
        """

        if token.kind == TokenKind.EOF:
            where = " at end"
        else:
            where = " at '" + token.lexeme + "'"

        Error.__report(token.line, where, message)
