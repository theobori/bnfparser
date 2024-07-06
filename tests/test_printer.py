"""test printer module"""

import unittest

from bnfparser import lexer, parser, printer

BNF_EXPRESSIONS_OK = (
'''
<expression> ::= <term> | <expression> "+" <term> | <expression> "-" <term>
<term> ::= <factor> | <term> "*" <factor> | <term> "/" <factor>
<factor> ::= <number> | "(" <expression> ")"
<number> ::= <digit> | <digit> <number>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
''',
'''
<list> ::= "[" <elements> "]"
<elements> ::= <element> | <element> "," <elements>
<element> ::= <number> | <string> | <list>
<number> ::= <digit> | <digit> <number>
<string> ::= "\"\"\"" <characters> "\"\"\""
<characters> ::= <character> | <character> <characters>
<character> ::= <letter> | <digit> | <symbol>
<letter> ::= "a" | "b" | "c" | "z" | "A" | "B" | "C" | "Z"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "=" | "+"
''',
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
'''
<a> ::= "hello"
'''
)

class TestPrinter(unittest.TestCase):
    """Controller for the printer tests
    """

    def test_expressions_ok(self):
        """Test with valid expressions
        """

        for expression in BNF_EXPRESSIONS_OK:
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
