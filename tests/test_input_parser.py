"""test input parser module"""

import unittest

from bnfparser import core

BNF_EXPRESSIONS = (
(
'''
<sentence> ::= <noun-phrase> <space> <verb-phrase>
<noun-phrase> ::= <article> <space> <adjective> <space> <noun> | <article> <space> <noun> | <noun>
<verb-phrase> ::= <verb> <space> <noun-phrase> | <verb>
<article> ::= "the" | "a"
<adjective> ::= "quick" | "lazy" | "happy" | "sad"
<noun> ::= "fox" | "dog" | "cat" | "mouse"
<verb> ::= "jumps" | "runs" | "sleeps" | "eats"
<space> ::= " "
''', (
        "the cat eats the quick fox",
        "the lazy mouse jumps a quick mouse",
        "cat jumps cat",
        "the happy dog jumps",
        "mouse sleeps",
    ),
    (
        "the cat eats booa",
        "runs",
        "fox",
        "the hello !...",
    )
),
(
'''
<list> ::= ("[" <elements> "]") | "[" "]"
<elements> ::= (<element> | <element> "," <elements>)
<element> ::= <number> | <string> | <list>
<number> ::= <digit> | <digit> <number>
<string> ::= "\"" <characters> "\""
<characters> ::= <character> | <character> <characters>
<character> ::= <letter> | <digit> | <symbol>
<letter> ::= "a" | "b" | "c" | "z" | "A" | "B" | "C" | "Z"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "=" | "+"
''', (
        '["1",[9,[["B&"]],[37]]]',
        '[1,"bazazaazaz9","9Z-",5]',
        '[[[[7123123123123123123124,"6","9"],[["5",[6]],"(3b"]],031]]',
        '["z",["2@",579],55671,"&",38]',
        '[")",[0],[882,["Z","6b"],5]]',
        '["0Z"]',
        '[]',
    ), (
        "[1,2,3,4,hello]",
        "[1,2,3,4",
        "1,2,3,]",
    )
),
(
'''
<adn> ::= ("A" | "T" | "C" | "G") | ("A" | "T" | "C" | "G") <adn>
''', (
        "ACCTAGCTGACGTAG",
        "ACTGTGTGTCACA",
        "AAAAAAAAAAAAAAAAAAAA",
        "TTTTTTTTTTTTT"
    ),
    (
        "ACAACD",
        "ATCGTGAD",
        "khkazd azd &é",
        "",
    )
),
)

class TestInputParser(unittest.TestCase):
    """Controller for generated tree from inputs
    """

    def test_expressions(self):
        """Test with expressions
        """

        i = 0
        for expression, ok, ko in BNF_EXPRESSIONS:
            bnf = core.parse(expression)

            for source in ok:
                print(source)
                print()

                tree = bnf.parse_input(source)

                self.assertIsNotNone(tree)

                # tree.build_graph().render(
                #     filename=f"{i}",
                #     format="png",
                #     cleanup=True,
                #     view=True,
                #     directory="./built_graphs"
                # )

                i += 1

            for source in ko:
                print(source)
                print()

                self.assertIsNone(bnf.parse_input(source))

if __name__ == '__main__':
    unittest.main()
