"""test parser module"""

import unittest


from bnfparser import core

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

class TestParser(unittest.TestCase):
    """Controller for the syntax and semantic tests together
    """

    def test_expressions_ok(self):
        """Test with valid expressions
        """

        for expression in BNF_EXPRESSIONS_OK:
            try:
                core.parse(expression)
            except AssertionError as e:
                self.fail(e)

    def test_expressions_ko(self):
        """Test with invalid expressions
        """

        for expression in BNF_EXPRESSIONS_KO:
            self.assertRaises(AssertionError, core.parse, expression)

if __name__ == '__main__':
    unittest.main()
