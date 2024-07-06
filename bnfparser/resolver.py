"""resolver module"""

from typing import List, Any, Dict, Union
from sys import stderr

from .error import VisitorError
from .token import Token
from .expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression

Environment = Dict[Token, Expression]

class Resolver(Visitor):
    """`Visitor` implementation that verify some semantic stuff post parsing.
    Its main goal is to resolve identifiers / variables.
    """

    def __init__(self):
        self.__first_visit = False
        self.__identifiers = {}

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        return

    def visit_right_expression(self, expression: NonTerminal) -> Any:
        for e in expression.expressions:
            self.__resolve_expression(e)

    def visit_variable_expression(self, expression: Variable) -> Any:
        if self.__first_visit:
            return

        if not (name := expression.name) in self.__identifiers:
            raise self.error(name, "Undefined variable")

    def visit_or_expression(self, expression: Or) -> Any:
        for value in expression.values:
            self.__resolve_expression(value)

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        name = expression.name

        if self.__first_visit and name in self.__identifiers:
            raise self.error(name, "Already defined")

        self.__identifiers[name] = expression.expression

        self.__resolve_expression(expression.expression)

    def visit_group_statement(self, expression: Group) -> Any:
        self.__resolve_expression(expression.expression)

    def __resolve_expression(self, expression: Expression):
        """Resolve the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        expression.accept(self)

    def __resolve(self, expressions: List[Expression], first_visit: bool=True):
        self.__first_visit = first_visit

        for expression in expressions:
            self.__resolve_expression(expression)

    def resolve(self, expressions: List[Expression]) -> Union[Environment, None]:
        """verify the tree from left to right
        Args:
            expressions (List[Expression]): Expressions list
        """

        try:
            # Check for already defined identifiers then store variables values
            self.__resolve(expressions, True)

            # Check for undefined identifiers within expressions
            self.__resolve(expressions, False)
        except VisitorError as e:
            print(e, file=stderr)
            return None

        return self.__identifiers
