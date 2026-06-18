from tokens import TokenType
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]
    
    def advance(self):
        token = self.tokens[self.current]
        self.current += 1
        return token

    def match(self, *types):
        token_type = self.peek()[0]

        if token_type in types:
            self.advance()
            return True

        return False
    
    def consume(self, token_type, message):
        if self.peek()[0] == token_type:
            return self.advance()
        
        raise Exception(message)
    
    def parse(self):
        statements = []

        while self.peek()[0] != TokenType.EOF:
            statements.append(self.statement())
        
        return ProgramNode(statements)

    def statement(self):
        if self.match(TokenType.VAR):
            return self.var_decl()
        if self.match(TokenType.WHILE):
            return self.while_statement()

        return self.assignment()
    
    def var_decl(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name"
        )[1]

        self.consume(
            TokenType.EQUAL,
            "Expected '='"
        )

        value = self.expression()

        return VarDeclNode(name, value)
    
    def while_statement(self):
        self.consume(TokenType.LPAREN, "Expected '(' after while")

        condition = self.expression()

        self.consume(TokenType.RPAREN, "Expected ')'")

        block = self.block()

        return WhileNode(condition, block)

    def assignment(self):
        name = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name"
        )[1]

        self.consume(
            TokenType.EQUAL,
            "Expected '='"
        )

        value = self.expression()

        return AssignmentNode(name, value)
    
    def block(self):
        self.consume(TokenType.LKEY, "Expected '{'")

        statements = []

        while self.peek()[0] != TokenType.RKEY and self.peek()[0] != TokenType.EOF:
            statements.append(self.statement())

        self.consume(TokenType.RKEY, "Expected '}'")

        return BlockNode(statements)

    def expression(self):
        return self.term()

    def term(self):
        left = self.factor()

        while self.match(
            TokenType.PLUS,
            TokenType.MINUS
        ):
            op = self.tokens[self.current - 1][0]

            right = self.factor()

            left = BinaryOpNode(left, op, right)

        return left

    def factor(self):
        left = self.unary()

        while self.match(
            TokenType.STAR,
            TokenType.SLASH
        ):
            
            op = self.tokens[self.current - 1][0]

            right = self.unary()

            left = BinaryOpNode(left, op, right)

        return left
    
    def unary(self):
        if self.match(TokenType.MINUS):
            return UnaryOpNode(TokenType.MINUS, self.unary())

        return self.primary()

    def primary(self):
        token = self.peek()

        if self.match(TokenType.NUMBER):
            return NumberNode(token[1])

        if self.match(TokenType.STRING):
            return StringNode(token[1])

        if self.match(TokenType.IDENTIFIER):
            return VariableNode(token[1])

        raise Exception("Expected expression")