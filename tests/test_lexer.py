"""test lexer module"""

import unittest

from bnfparser import lexer, token, error

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

    def test_bnf_number_ko(self):
        """Test with an invalid source
        """

        lexer.Lexer(BNF_NUMBER_KO).scan_tokens()

        self.assertTrue(error.Error.had_lexer_error)

    def test_bnf_number_ok(self):
        """Test with a valid source
        """

        l = lexer.Lexer(BNF_NUMBER_OK)

        tokens = l.scan_tokens()

        self.assertEqual(
            tokens,
            [
                # Line 1
                token.Token(token.TokenKind.IDENTIFIER, "<number>"),
                token.Token(token.TokenKind.ASSIGN, "::="),
                token.Token(token.TokenKind.IDENTIFIER, "<digit>"),
                token.Token(token.TokenKind.PIPE, "|"),
                token.Token(token.TokenKind.IDENTIFIER, "<number>"),

                # Line 2
                token.Token(token.TokenKind.IDENTIFIER, "<digit>"),
                token.Token(token.TokenKind.ASSIGN, "::="),
                token.Token(token.TokenKind.STRING, "\"1\"", "1"),
                token.Token(token.TokenKind.PIPE, "|"),
                token.Token(token.TokenKind.STRING, "\"2\"", "2"),
                token.Token(token.TokenKind.PIPE, "|"),
                token.Token(token.TokenKind.STRING, "\"3\"", "3"),

                # End of file
                token.Token(token.TokenKind.EOF, ""),
            ]
        )

if __name__ == '__main__':
    unittest.main()
