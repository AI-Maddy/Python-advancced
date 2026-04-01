"""
Example 1 — Compiler subsystem facade.

Hides lexer, parser, semantic analyser, and code generator behind a
simple ``compile(source)`` call.
"""
from __future__ import annotations


class Lexer:
    def tokenize(self, source: str) -> list[str]:
        tokens = source.split()
        print(f"  Lexer: tokenized {len(tokens)} tokens")
        return tokens


class Parser:
    def parse(self, tokens: list[str]) -> dict:
        ast = {"type": "program", "body": tokens}
        print(f"  Parser: built AST with {len(tokens)} nodes")
        return ast


class SemanticAnalyser:
    def analyse(self, ast: dict) -> dict:
        ast["analysed"] = True
        print("  SemanticAnalyser: type-checked OK")
        return ast


class CodeGenerator:
    def generate(self, ast: dict) -> str:
        bytecode = f"BYTECODE[{len(ast['body'])} ops]"
        print(f"  CodeGenerator: emitted {bytecode}")
        return bytecode


class CompilerFacade:
    """Simple compile(source) → bytecode facade."""

    def __init__(self) -> None:
        self._lexer = Lexer()
        self._parser = Parser()
        self._analyser = SemanticAnalyser()
        self._codegen = CodeGenerator()

    def compile(self, source: str) -> str:
        print("Compiling…")
        tokens = self._lexer.tokenize(source)
        ast = self._parser.parse(tokens)
        ast = self._analyser.analyse(ast)
        return self._codegen.generate(ast)


def main() -> None:
    compiler = CompilerFacade()
    result = compiler.compile("let x = 1 + 2 ; print x ;")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
