"""test lexer module"""

import unittest

from bnfparser import lexer, error

BNF_NUMBER_OK = '''

<number> ::= <digit> | <number> ; representing a number
;
<digit> ::= "1" | "2" | "3" ; representing a number letter


;
;
;
; ; ; ;

; Hello
'''

BNF_NUMBER_KO = '''
<number> := <digit> | number> ; representing a number

<digit> ::= " | "2" | "3" ; representing a number letter

'''

class TestLexer(unittest.TestCase):
    """Controller for the lexer tests
    """

    def test_bnf_number_ok(self):
        """Test with an valid source
        """

        try:
            lexer.Lexer(BNF_NUMBER_OK).scan()
        except error.LexerError:
            self.fail()

    def test_bnf_number_ko(self):
        """Test with a invalid source
        """

        l = lexer.Lexer(BNF_NUMBER_KO)

        self.assertRaises(error.LexerError, l.scan)

if __name__ == '__main__':
    unittest.main()
