"""test parser module"""

import unittest

from typing import List

from bnfparser import lexer, parser, expression, verifier

BNF_EXPRESSIONS_OK = (
'''
<number> ::= <digit> | <number> "random string"; representing a number
<digit> ::= "1" | "2" | "3" ; representing a number letter
''',
'''
<abc> ::= (("a" ("b")) | "c") | ("d" | <r>)
<r> ::= "sec" "ond" | <first>
<first> ::= ("sec" "ond") | <first>
''',
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
<verb> ::= "jumps" | "runs" | "sleeps" | "eats"
''',
)

BNF_EXPRESSIONS_KO = (
'''
<abc> ::= "hello" | <abc>
<d> ::= "a"
<c> ::=
''',
'''
<d> ::= "a"
<d> ::= "b"
''',
'''
<b> ::= ((((("b"))))
''',
'''
<b> ::= <a>
<a> ::= <c>
''',
)

def parse(s: str) -> List[expression.Expression]:
    """Lexing then parsing a source

    Args:
        s (str): The source as a string

    Returns:
        List[expression.Expression]: Parsed expressions
    """

    # Lexing
    l = lexer.Lexer(s)
    tokens = l.scan()

    # Parsing
    p = parser.Parser(tokens)
    expressions = p.parse()

    return expressions

class TestParser(unittest.TestCase):
    """Controller for the parser tests
    """

    def test_expressions_ok(self):
        """Test with valid expressions
        """

        for e in BNF_EXPRESSIONS_OK:
            self.assertIsNotNone(parse(e))

    def test_expressions_ko(self):
        """Test with invalid expressions
        """

        for e in BNF_EXPRESSIONS_KO:
            expressions = parse(e)

            if expressions is None:
                continue

            print(e)

            # Verifying semantic
            v = verifier.Verifier()
            is_valid = v.verify(expressions)

            self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
