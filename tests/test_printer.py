"""test printer module"""

import unittest

from bnfparser import lexer, parser, printer

BNF_EXPRESSIONS = (
'''
<sentence> ::= <noun-phrase> <verb-phrase>
<noun-phrase> ::= <article> <adjective> <noun> | <article> <noun> | <noun>
<verb-phrase> ::= <verb> <noun-phrase> | <verb>
<article> ::= "the" | "a"
<adjective> ::= "quick" | "lazy" | "happy" | "sad"
<noun> ::= "fox" | "dog" | "cat" | "mouse"
<verb> ::= ("jumps" | ("runs" | "sleeps")) | "eats"
''',
'''
<abc> ::= (("a" ("b")) | "c") | ("d" | <r>)
''',
)

class TestPrinter(unittest.TestCase):
    """Controller for the printer tests
    """

    def test_expressions(self):
        """Test with valid expressions
        """

        for expression in BNF_EXPRESSIONS:
            # Lexing
            l = lexer.Lexer(expression)
            tokens = l.scan()

            # Parsing
            p = parser.Parser(tokens)
            expressions = p.parse()

            # Printing
            pr = printer.Printer()
            pr.print(expressions)

if __name__ == '__main__':
    unittest.main()
