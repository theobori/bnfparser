# BNF parser

[![lint](https://github.com/theobori/bnfparser/actions/workflows/lint.yml/badge.svg)](https://github.com/theobori/bnfparser/actions/workflows/lint.yml) [![build](https://github.com/theobori/bnfparser/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/bnfparser/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This Python module parses BNF grammar rules and produces an AST representing the BNF syntax. It can also generate random expressions from given BNF grammar rules and parse input sequences matching the BNF rules. It handles infinite recursion grammar rules within the needed `Visitor` implementations.

## 🍬 Syntactic sugar

I've added a grouping feature that have the following syntax.

```text
<adn> ::= ("A" | "T" | "C" | "G") | ("A" | "T" | "C" | "G") <adn>
```

It is the same as below.

```text
<adn> ::= <base> | <base> <adn>
<base> ::= "A" | "T" | "C" | "G"
```

## 📖 Build and run

For the build, you only need the following requirements:

- [Python](https://www.python.org/downloads/) 3+ (tested with 3.12.4)

## 🤝 Contribute

If you want to help the project, you can follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## 📎 Some examples

Here is an example of how you could use this module.

```py
import bnfparser
import sys

RESTRICTED_LIST = '''
<list> ::= "[" <elements> "]"
<elements> ::= (<element> | <element> "," <elements>)
<element> ::= <number> | <string> | <list>
<number> ::= <digit> | <digit> <number>
<string> ::= "\"" <characters> "\""
<characters> ::= <character> | <character> <characters>
<character> ::= <letter> | <digit> | <symbol>
<letter> ::= "a" | "b" | "c" | "z" | "A" | "B" | "C" | "Z"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<symbol> ::= "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*" | "(" | ")" | "-" | "_" | "=" | "+"
'''

try:
    bnf = bnfparser.parse(RESTRICTED_LIST)
# except bnfparser.LexerError as error:
#     pass
# except bnfparser.ParserError as error:
#     pass
# except bnfparser.VisitorError as error:
#     pass
except bnfparser.BaseError as error:
    print(error, file=sys.stderr)

# Generate a random expression
print(bnf.generate())

# Printing an AST representation
bnf.print()

# BNF expressions list (AST)
expressions = bnf.expressions

# InputTree inheriting the graphviz.Graph class
input_tree = bnf.parse_input('[")",[0],[882,["Z","6b"],5]]')

# Change the entry point rule
try:
    bnf.set_start("<string>")
# except bnfparser.CoreError:
#     pass
except bnfparser.BaseError:
    pass

# Generate a random expression
print(bnf.generate())

input_tree = bnf.parse_input("\"123\"")
if not input_tree is None:
    # Building graphviz graph then render it
    input_tree.build_graph().render(
        filename="bnf_string_graph",
        format="png",
        cleanup=True,
        view=True,
        directory="./images"
    )

# Saved as ./images/bnf_string_graph.png
```

![bnf_string_graph](/images/bnf_string_graph.png)

## 🎉 Tasks

- [x] Iterative generator
- [ ] Iterative input parser
- [x] Handles infinite recursion grammar rules
