"""generator module"""

import random

from typing import Any
from collections import deque

from .error import VisitorError
from .expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression
from .resolver import Environment

class Generator(Visitor):
    """`Visitor` implementation that produce a random string based
    on a BNF grammar
    """

    def __init__(self, environment: Environment):
        self.__destination = ""
        self.__environment = environment
        self.__expressions_stack = deque()

    def __add(self, s: str):
        self.__destination += s

    def __reset(self):
        self.__destination = ""
        self.__expressions_stack.clear()

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        self.__add(expression.value)

    def visit_nonterminal_expression(self, expression: NonTerminal) -> Any:
        for e in reversed(expression.expressions):
            self.__expressions_stack.append(e)

    def visit_variable_expression(self, expression: Variable) -> Any:
        if not (name := expression.name) in self.__environment:
            raise VisitorError.error_token(
                name,
                "Missing " + name.lexeme + " in the environment"
            )

        value = self.__environment[name]
        self.__expressions_stack.append(value)

    def visit_or_expression(self, expression: Or) -> Any:
        value = random.choice(expression.values)
        self.__expressions_stack.append(value)

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        self.__expressions_stack.append(expression.expression)

    def visit_group_statement(self, expression: Group) -> Any:
        self.__expressions_stack.append(expression.expression)

    def __generate_expression(self, expression: Expression):
        """Verify the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        expression.accept(self)

    def generate(self, start: Expression) -> str:
        """Generate a random string based on the given `expressions`

        Args:
            start (Expression): A start expression

        Returns:
            str: A random string
        """

        self.__reset()

        # Init stack
        self.__expressions_stack.append(start)

        try:
            while self.__expressions_stack:
                self.__generate_expression(self.__expressions_stack.pop())
        except VisitorError:
            return ""

        return self.__destination
