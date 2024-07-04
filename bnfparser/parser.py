"""parser module"""

from sys import stderr

from typing import List, Union

from .token import Token, TokenKind
from .error import Error, ParserError
from .expression import Expression, Terminal, Variable, Or, Assignment, Group, NonTerminal

class Parser:
    """Parse tokens then produces a AST representing the BNF langage
    """

    def __init__(self, tokens: List[Token]):
        self.__tokens = tokens
        self.__current = 0

    def __is_at_end(self) -> bool:
        """Returns if the current cursor has reached the end of file

        Returns:
            bool: Is the current token of kind `TokenKind.EOF`
        """

        return self.__peek().kind == TokenKind.EOF

    def __peek(self, index: Union[list ,None]=None) -> Token:
        """
            get the current token
        """

        if index is None:
            index = self.__current

        return self.__tokens[index]

    def __peek_previous(self) -> Token:
        """
            Get the previous token
        """

        return self.__peek(self.__current - 1)

    def __check(self, kind: TokenKind) -> bool:
        """
            Compare the current token kind with a specific token kind
        """

        if self.__is_at_end():
            return False

        return self.__peek().kind == kind

    def __match(self, *kinds: TokenKind) -> bool:
        """Compare the current token kind with multiple token kinds

        Returns:
            bool: Has a match
        """

        if ret := self.__peek().kind in kinds:
            self.__advance()

        return ret

    def __error(self, token: Token, message: str) -> ParserError:
        """Write a token error into stdout and return a `ParserError` instance

        Args:
            token (Token): A token
            message (str): Error message

        Returns:
            ParserError: Exception child class
        """

        Error.error_token(token, message)

        return ParserError()

    def __consume(self, kind: TokenKind, message: str) -> Token:
        """Consume the current token only if it matches the token kind,
            otherwise, it becomes an error

        Args:
            kind (TokenKind): A token kind
            message (str): Message if an error happend

        Raises:
            self.__error

        Returns:
            Token: The current token
        """

        if self.__check(kind):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __advance(self) -> Token:
        """Move the cursor on the next token and return the previous one

        Returns:
            Token: The current token
        """

        if not self.__is_at_end():
            self.__current += 1

        return self.__peek_previous()

    def __primary(self) -> Expression:
        """Last grammar production

        Raises:
            self.__error: Unknown character/string

        Returns:
            Expression: An expression representing an operator
        """

        if self.__match(TokenKind.STRING):
            return Terminal(self.__peek_previous().literal)

        if self.__match(TokenKind.LEFT_PAREN):
            expr = self.__expression()

            self.__consume(TokenKind.RIGHT_PAREN, "Expect ')'")

            return Group(expr)

        if self.__match(TokenKind.IDENTIFIER):
            return Variable(self.__peek_previous())

        raise self.__error(self.__peek_previous(), "Expect expression")

    def __left_or(self) -> Expression:
        """Or left side

        Raises:
            self.__error: If no expression found

        Returns:
            Expression: An expression
        """

        left = []

        while not self.__match(TokenKind.EOL) and self.__peek().kind != TokenKind.RIGHT_PAREN:
            if self.__peek().kind == TokenKind.PIPE:
                break

            left.append(self.__primary())

        size = len(left)

        if size == 0:
            raise self.__error(self.__peek(), "Expected values")

        if size == 1:
            return left[0]

        return NonTerminal(left)

    def __or(self) -> Expression:
        """Or grammar production

        Returns:
            Expression: An expression
        """

        expressions = [self.__left_or()]

        while self.__match(TokenKind.PIPE):
            a = self.__left_or()
            expressions.append(a)

        size = len(expressions)

        if size == 1:
            return expressions[0]

        return Or(expressions)

    def __expression(self) -> Expression:
        """Top grammar production

        Returns:
            Expression: An expression
        """

        return self.__or()

    def __assignment(self) -> Expression:
        """Assignment grammar production

        Raises:
            self.__error: Needs an identifier
            self.__error: Needs the '::=' symbol

        Returns:
            Expression: An Assignment expression
        """

        if not self.__match(TokenKind.IDENTIFIER):
            raise self.__error(self.__peek(), "Expected an identifier")

        name = self.__peek_previous()

        if not self.__match(TokenKind.ASSIGN):
            raise self.__error(self.__peek(), "Expected '::='")

        expression = self.__expression()

        return Assignment(name, expression)

    def parse(self) -> Union[List[Expression],  None]:
        """Returns a list of expressions representing the AST

        Returns:
            Union[List[Expression],  None]: Expressions or None
        """

        expressions = []

        try:
            while not self.__is_at_end():
                if self.__match(TokenKind.EOL):
                    continue

                expressions.append(self.__assignment())
        except ParserError as e:
            print(e, file=stderr)
            return None

        return expressions
