"""test generator module"""

import unittest

from bnfparser import core

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
<list> ::= "[" <elements> "]"
<elements> ::= <element> | <element> "," <elements>
<element> ::= <number> | <string> | <list>
<number> ::= <digit> | <digit> <number>
<string> ::= "\"" <characters> "\""
<characters> ::= <character> | <character> <characters>
<character> ::= <letter> | <digit> | <symbol>
<letter> ::= "a" | "b" | "c" | "z" | "A" | "B" | "C" | "Z"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "=" | "+"
''',
'''
<abc> ::= (("a" ("b")) | "c") | (("d" | "r" "a"))
''',
'''
 <syntax>         ::= <rule> | <rule> <syntax>
 <rule>           ::= <opt-whitespace> "<" <rule-name> ">" <opt-whitespace> "::=" <opt-whitespace> <expression> <line-end>
 <opt-whitespace> ::= " " <opt-whitespace> | ""
 <expression>     ::= <list> | <list> <opt-whitespace> "|" <opt-whitespace> <expression>
 <line-end>       ::= <opt-whitespace> <EOL> | <line-end>
 <list>           ::= <term> | <term> <opt-whitespace> <list>
 <term>           ::= <literal> | "<" <rule-name> ">"
 <literal>        ::= '"' <text1> '"' | "'" <text2> "'"
 <text1>          ::= "" | <character1> <text1>
 <text2>          ::= "" | <character2> <text2>
 <character>      ::= <letter> | <digit> | <symbol>
 <letter>         ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
 <digit>          ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
 <symbol>         ::= "|" | " " | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | ">" | "=" | "<" | "?" | "@" | "[" | "\" | "]" | "^" | "_" | "`" | "{" | "}" | "~"
 <character1>     ::= <character> | "'"
 <character2>     ::= <character> | '"'
 <rule-name>      ::= <letter> | <rule-name> <rule-char>
 <rule-char>      ::= <letter> | <digit> | "-"
''',
)

class TestGenerator(unittest.TestCase):
    """Controller for the generator tests
    """

    def test_expressions(self):
        """Test with valid expressions
        """

        for expression in BNF_EXPRESSIONS:
            bnf = core.parse(expression)
            s = bnf.generate()

            print(s)

            self.assertNotEqual(s, "")

if __name__ == '__main__':
    unittest.main()
