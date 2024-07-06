"""print module"""

from typing import List, Any, Dict

from .expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression

INDENT_SYMBOL = " "
INDENT_SIZE = 2
INDENT_SEQUENCE = INDENT_SIZE * INDENT_SYMBOL

class Printer(Visitor):
    """`Visitor` implementation that print the tree
    """

    def __init__(self):
        self.__indent_prefix = ""

    def __print(self, *args: tuple, **kwargs: Dict[str, Any]):
        """`print` wrapper that use a managed indentation
        """

        print(self.__indent_prefix, end="")
        print(*args, **kwargs)

    def __indent_reset(self):
        """Reset the indentation
        """

        self.__indent_prefix = ""

    def __indent_increase(self):
        """Indent
        """

        self.__indent_prefix += INDENT_SEQUENCE

    def __indent_decrease(self):
        """Undo indent
        """

        self.__indent_prefix = self.__indent_prefix[INDENT_SIZE:]

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        self.__print("TERMINAL \"", expression.value, "\"", sep="")

    def visit_right_expression(self, expression: NonTerminal) -> Any:
        self.__print("NONTERMINAL")

        self.__indent_increase()

        for e in expression.expressions:
            self.__print_expression(e)

        self.__indent_decrease()

    def visit_variable_expression(self, expression: Variable) -> Any:
        self.__print("VARIABLE", expression.name.lexeme)

    def visit_or_expression(self, expression: Or) -> Any:
        self.__print("OR", "[")
        self.__indent_increase()

        for value in expression.values:
            self.__print_expression(value)

        self.__indent_decrease()
        self.__print("]")

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        self.__print("VARIABLE", expression.name.lexeme)

        self.__indent_increase()
        self.__print_expression(expression.expression)
        self.__indent_decrease()

    def visit_group_statement(self, expression: Group) -> Any:
        self.__print("GROUP", "(")
        self.__indent_increase()

        self.__print_expression(expression.expression)

        self.__indent_decrease()
        self.__print(")")

    def __print_expression(self, expression: Expression):
        """Print the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        expression.accept(self)

    def print(self, expressions: List[Expression]):
        """Print the tree from left to right
        Args:
            expressions (List[Expression]): Expressions list
        """

        for expression in expressions:
            self.__indent_reset()
            self.__print_expression(expression)
