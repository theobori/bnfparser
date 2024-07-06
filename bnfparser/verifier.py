"""verifier module"""

from typing import List, Any
from sys import stderr

from .error import Error, VisitorError
from .token import Token

from .expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression

class Verifier(Visitor):
    """`Visitor` implementation that verify some semantic
    stuff post parsing
    """

    def __init__(self):
        self.__first_visit = False
        self.__identifiers = set()

    def __error(self, token: Token, message: str) -> VisitorError:
        """Write a token error into stdout and return a `ParserError` instance

        Args:
            token (Token): A token
            message (str): Error message

        Returns:
            ParserError: Exception child class
        """

        Error.error_token(token, message)

        return VisitorError()

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        return

    def visit_right_expression(self, expression: NonTerminal) -> Any:
        for e in expression.expressions:
            self.__verify_expression(e)

    def visit_variable_expression(self, expression: Variable) -> Any:
        if self.__first_visit:
            return

        if not (name := expression.name) in self.__identifiers:
            raise self.__error(name, "Undefined variable")

    def visit_or_expression(self, expression: Or) -> Any:
        for value in expression.values:
            self.__verify_expression(value)

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        name = expression.name

        if self.__first_visit and name in self.__identifiers:
            raise self.__error(name, "Already defined")

        self.__identifiers.add(name)

        self.__verify_expression(expression.expression)

    def visit_group_statement(self, expression: Group) -> Any:
        self.__verify_expression(expression.expression)

    def __verify_expression(self, expression: Expression):
        """Verify the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        expression.accept(self)

    def __verify(self, expressions: List[Expression], first_visit: bool=True):
        self.__first_visit = first_visit

        for expression in expressions:
            self.__verify_expression(expression)

    def verify(self, expressions: List[Expression]) -> bool:
        """verify the tree from left to right
        Args:
            expressions (List[Expression]): Expressions list
        """

        try:
            # Check for already defined identifiers
            self.__verify(expressions, True)

            # Check for undefined identifiers within expressions
            self.__verify(expressions, False)
        except VisitorError as e:
            print(e, file=stderr)
            return False

        return True
