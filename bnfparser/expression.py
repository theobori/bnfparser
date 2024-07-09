"""expression module"""

from dataclasses import dataclass
from typing import List, Any

from .error import VisitorError, ExpressionError
from .token import Token

class Expression:
    """Expression base class
    """

    def accept(self, visitor: "Visitor") -> Any:
        """Accept a `Visitor` implementation then
        call the appropriate `Visitor` method with `Expression` as argument

        Args:
            visitor (Visitor): A `Visitor` implementation

        Returns:
            Any: Any value
        """

        raise ExpressionError("Not implemented")

@dataclass
class Terminal(Expression):
    """Represents a Terminal expression
    """

    value: str

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_terminal_expression(self)

@dataclass
class NonTerminal(Expression):
    """Represents a NonTerminal expression
    """

    expressions: List[Expression]

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_nonterminal_expression(self)

@dataclass
class Variable(Expression):
    """Represents a Variable expression
    """

    name: Token

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_variable_expression(self)

@dataclass
class Or(Expression):
    """Represents a Or expression. It is not binary by choice.
    """

    values: List[Expression]

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_or_expression(self)

@dataclass
class Assignment(Expression):
    """Represents a Assignment expression
    """

    name: Token
    expression: Expression

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_assignment_expression(self)

@dataclass
class Group(Expression):
    """Represents a Group expression
    """

    expression: Expression

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit_group_statement(self)


class Visitor:
    """Base class for `Visitor` implementations
    """

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        """Operate on a `Terminal` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")

    def visit_nonterminal_expression(self, expression: NonTerminal) -> Any:
        """Operate on a `NonTerminal` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")

    def visit_variable_expression(self, expression: Variable) -> Any:
        """Operate on a `Variable` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")

    def visit_or_expression(self, expression: Or) -> Any:
        """Operate on a `Or` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        """Operate on a `Assignment` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")

    def visit_group_statement(self, expression: Group) -> Any:
        """Operate on a `Group` expression

        Returns:
            Any: Any value
        """

        raise VisitorError("Not implemented")
