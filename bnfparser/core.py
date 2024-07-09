"""core module"""

from typing import List

from .expression import Expression
from .token import Token, TokenKind
from .lexer import Lexer
from .parser import Parser
from .resolver import Resolver, Environment
from .error import CoreError
from .expression import Variable

from .generator import Generator
from .printer import Printer

from .input.tree import InputTree
from .input.input_parser import InputParser

class Bnf:
    """BNF controller
    """

    def __init__(self, expressions: List[Expression], environment: Environment):
        self.__expressions = expressions
        self.__environment = environment
        self.__start = None

        # Default start expression (variable)
        self.set_start()

    @property
    def expressions(self) -> List[Expression]:
        """Returne the BNF AST

        Returns:
            List[Expression]: _description_
        """

        return self.__expressions

    def set_start(self, start: str="") -> "Bnf":
        """Setter for `self.__start`

        Args:
            start (str): The start token name

        Returns:
            self: Bnf
        """

        if len(self.__expressions) == 0:
            return self

        # Looking for a start BNF expression
        if start == "":
            self.__start = self.__expressions[0]
        else:
            token_start = Token(TokenKind.IDENTIFIER, start)

            if not token_start in self.__environment:
                raise CoreError(start + " is not in this environment")

            self.__start = Variable(token_start)

        return self

    def generate(self) -> str:
        """Generates a random expression

        Returns:
            str: A random expression
        """

        return Generator(self.__environment)\
            .generate(self.__start)

    def print(self):
        """Print the expression tree
        """

        return Printer().print(self.__expressions)

    def parse_input(self, input_source: str) -> InputTree | None:
        """Parse an input source that is supposed to be built on `self.__expressions`

        Args:
            input_source (str): Input source

        Returns:
            InputTree | None: None if it doesnt match, otherwise, a tree is returned
        """

        return InputParser(input_source, self.__environment)\
            .parse_input(self.__start)

def parse(source: str) -> Bnf:
    """Parse a BNF grammar expression

    Args:
        source (str): An expression

    Returns:
        Bnf: BNF grammar controller
    """

    # Lexing
    l = Lexer(source)
    tokens = l.scan()

    # Parsing
    p = Parser(tokens)
    expressions = p.parse()

    # Getting variables environment
    r = Resolver()
    environment = r.resolve(expressions)

    return Bnf(expressions, environment)
