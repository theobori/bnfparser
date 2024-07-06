"""test generator module"""

import unittest

from bnfparser import lexer, parser, resolver, generator

BNF_EXPRESSIONS = (
'''
<sentence> ::= <noun-phrase> <space> <verb-phrase>
<noun-phrase> ::= <article> <space> <adjective> <space> <noun> | <article> <space> <noun> | <noun>
<verb-phrase> ::= <verb> <space> <noun-phrase> | <verb>
<article> ::= "the" | "a"
<adjective> ::= "quick" | "lazy" | "happy" | "sad"
<noun> ::= "fox" | "dog" | "cat" | "mouse"
<verb> ::= "jumps" | "runs" | "sleeps" | "eats"
<space> ::= " "
''',
'''
<abc> ::= (("a" ("b")) | "c") | ("d" | "r")
''',
)

class TestGenerator(unittest.TestCase):
    """Controller for the generator tests
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

            # Getting variables environment
            r = resolver.Resolver()
            environment = r.resolve(expressions)

            # Generating
            g = generator.Generator(environment)
            s = g.generate(expressions)

            self.assertNotEqual(s, "")

if __name__ == '__main__':
    unittest.main()
