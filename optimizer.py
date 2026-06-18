from tokens import TokenType
from nodes import *

class Optimizer:
    def __init__(self):
        self.constants = {}
        self.copies = {}

    def optimize(self, node):

        if isinstance(node, ProgramNode):
            return ProgramNode([
                self.optimize(s) for s in node.statements
            ])

        if isinstance(node, VarDeclNode):

            value = self.optimize(node.value)
            if isinstance(value, NumberNode):
                self.constants[node.name] = value.value

            return VarDeclNode(node.name, value)

        if isinstance(node, AssignmentNode):

            value = self.optimize(node.value)

            if isinstance(value, VariableNode):
                self.copies[node.name] = value.name
            else:
                self.copies[node.name] = None

            return AssignmentNode(node.name, value)

        if isinstance(node, VariableNode):

            if node.name in self.constants:
                return NumberNode(self.constants[node.name])

            while node.name in self.copies and self.copies[node.name]:
                node = VariableNode(self.copies[node.name])

            return node

        if isinstance(node, BinaryOpNode):

            l = self.optimize(node.left)
            r = self.optimize(node.right)

            if isinstance(l, NumberNode) and isinstance(r, NumberNode):

                if node.op == TokenType.PLUS:
                    return NumberNode(l.value + r.value)
                if node.op == TokenType.MINUS:
                    return NumberNode(l.value - r.value)
                if node.op == TokenType.STAR:
                    return NumberNode(l.value * r.value)
                if node.op == TokenType.SLASH:
                    return NumberNode(l.value / r.value)

            return BinaryOpNode(l, node.op, r)

        return node