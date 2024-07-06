"""core module"""

from typing import List

from .expression import Expression
from .lexer import Lexer
from .parser import Parser
from .resolver import Resolver, Environment

from .generator import Generator
from .printer import Printer

class Bnf:
    """BNF controller
    """

    def __init__(self, expressions: List[Expression], environment: Environment):
        self.__expressions = expressions
        self.__environment = environment

    def generate(self, start: str="") -> str:
        """Generates a random expression

        Args:
            start (str, optional): Start token name (must have < and >). Defaults to "".

        Returns:
            str: A random expression
        """

        return Generator(self.__environment)\
            .generate(self.__expressions, start)

    def print(self):
        """Print the expression tree
        """

        return Printer().print(self.__expressions)

def parse(source: str) -> Bnf:
    """Parse a BNF grammar expression

    Args:
        source (str): An expression

    Returns:
        Bnf: BNF controller object
    """

    # Lexing
    l = Lexer(source)
    tokens = l.scan()

    # Parsing
    p = Parser(tokens)
    expressions = p.parse()

    assert not expressions is None

    # Getting variables environment
    r = Resolver()
    environment = r.resolve(expressions)

    assert not environment is None

    return Bnf(expressions, environment)
