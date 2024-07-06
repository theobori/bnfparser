"""generator module"""

import random

from typing import List, Any, Dict
from sys import stderr

from .error import VisitorError
from .token import Token, TokenKind
from .expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression

class Generator(Visitor):
    """`Visitor` implementation that produce a random string based
    on a BNF grammer
    """

    def __init__(self, environment: Dict[Token, Expression]):
        self.__destination = ""
        self.__environment = environment

    def __add(self, s: str):
        self.__destination += s

    def __reset(self):
        self.__destination = ""

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        self.__add(expression.value)

    def visit_right_expression(self, expression: NonTerminal) -> Any:
        for e in expression.expressions:
            self.__generate_expression(e)

    def visit_variable_expression(self, expression: Variable) -> Any:
        if not (name := expression.name) in self.__environment:
            self.error(name, "Missing " + name.lexeme + " in the environment")

        value = self.__environment[name]

        self.__generate_expression(value)

    def visit_or_expression(self, expression: Or) -> Any:
        value = random.choice(expression.values)

        self.__generate_expression(value)

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        self.__generate_expression(expression.expression)

    def visit_group_statement(self, expression: Group) -> Any:
        self.__generate_expression(expression.expression)

    def __generate_expression(self, expression: Expression):
        """Verify the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        expression.accept(self)

    def generate(self, expressions: List[Expression], start: str="") -> str:
        """Generate a random string based on the give `expressions`

        Args:
            expressions (List[Expression]): Representing the tree
            start (str, optional): Start identifier value. Defaults to "".

        Raises:
            VisitorError: Can raise an error

        Returns:
            str: A random string
        """

        self.__reset()

        if len(expressions) == 0:
            return ""

        # Looking for a start BNF expression
        if start == "":
            expression_start = expressions[0]
        else:
            token_start = Token(TokenKind.IDENTIFIER, start)

            if not token_start in self.__environment:
                raise VisitorError(f"Token {token_start} is not in this environment")

            expression_start = self.__environment[token_start]

        try:
            self.__generate_expression(expression_start)
        except VisitorError as e:
            print(e, file=stderr)
            return ""

        return self.__destination
