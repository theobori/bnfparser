"""input_parser module"""

from typing import Any
from collections import deque

from ..error import VisitorError
from ..expression import Visitor, Terminal, NonTerminal, \
    Variable, Or, Assignment, Group, Expression
from ..resolver import Environment

from .tree import InputTree
from .input import Input
from .node import Nodekind

class InputParser(Visitor):
    """`Visitor` implementation that produce a tree based on a given input.
    Assuming the input matches with the BNF grammar tree.
    """

    def __init__(self, source: str, environment: Environment):
        self.__input = Input(source)

        # Variables environment
        self.__environment = environment

        # Used for recursive grammar rules
        self.__visited = {token: False for token in environment}

        # Used for backtracking without deepcopy the entire tree
        self.__trees = deque([InputTree()])

    def __reset(self):
        self.__input.reset()
        self.__trees[-1].reset()

    def __reset_visited(self):
        for k in self.__visited:
            self.__visited[k] = False

    def visit_terminal_expression(self, expression: Terminal) -> Any:
        is_matched = self.__input.match(expression.value)

        if is_matched:
            self.__reset_visited()
            self.__trees[-1].add(Nodekind.VALUE, expression.value)

        return is_matched

    def visit_nonterminal_expression(self, expression: NonTerminal) -> Any:
        curr = self.__trees[-1].current

        for e in expression.expressions:
            if not self.__parse_expression(e):
                self.__trees[-1].current = curr
                return False

        return True

    def visit_variable_expression(self, expression: Variable) -> Any:
        if not (name := expression.name) in self.__environment:
            raise VisitorError.error_token(
                name,
                "Missing " + name.lexeme + " in the environment"
            )

        if self.__visited[name]:
            return False

        self.__visited[name] = True
        value = self.__environment[name]

        self.__trees[-1].add_and_forward(Nodekind.VARIABLE, name.lexeme)
        ret = self.__parse_expression(value)
        self.__trees[-1].back()

        return ret

    def visit_or_expression(self, expression: Or) -> Any:
        steps, tree = -1, None
        initial_current = self.__input.current

        for e in expression.values:
            # Reset the input current cursor
            self.__input.current = initial_current
            # Add an empty tree to the stack
            self.__trees.append(InputTree())

            has_matched = self.__parse_expression(e)

            # Get the last added tree
            tmp_tree = self.__trees.pop()

            # Update the tree if there are more steps
            # and if it matched
            if has_matched and self.__input.current > steps:
                steps = self.__input.current
                tree = tmp_tree

        if tree is None:
            return False

        # Update current
        self.__input.current = steps

        # Add the childrens from the longest path
        for children in tree.root.childrens:
            self.__trees[-1].add_children(children)

        self.__reset_visited()

        return True

    def visit_assignment_expression(self, expression: Assignment) -> Any:
        return self.__parse_expression(expression.expression)

    def visit_group_statement(self, expression: Group) -> Any:
        return self.__parse_expression(expression.expression)

    def __parse_expression(self, expression: Expression):
        """Verify the given `expression` with the right `Visitor` method

        Args:
            expression (Expression): An expression
        """

        return expression.accept(self)

    def parse_input(self, start: Variable) -> InputTree | None:
        """Produce an AST based on the grammar rules

        Args:
            start (Variable): Grammar entry point rule

        Returns:
            InputTree | None: Return None if it doest match, otherwise, it returns the tree
        """

        self.__reset()

        # Insert first node
        self.__trees[-1].add_and_forward(
            Nodekind.VARIABLE,
            start.name.lexeme
        )

        try:
            if self.__parse_expression(start) and self.__input.is_full_match():
                return self.__trees[-1]
        except VisitorError:
            return None

        return None
