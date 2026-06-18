from tokens import TokenType
from nodes import *

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}

    def analyze(self, node):
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.analyze(statement)
            return

        if isinstance(node, NumberNode):
            return "number"

        if isinstance(node, StringNode):
            return "string"

        if isinstance(node, VariableNode):

            if node.name not in self.symbols:
                raise Exception(
                    f"Undefined variable '{node.name}'"
                )

            return self.symbols[node.name]

        if isinstance(node, VarDeclNode):

            if node.name in self.symbols:
                raise Exception(
                    f"Variable '{node.name}' already defined"
                )

            value_type = self.analyze(node.value)

            self.symbols[node.name] = value_type

            return value_type


        if isinstance(node, AssignmentNode):

            if node.name not in self.symbols:
                raise Exception(
                    f"Undefined variable '{node.name}'"
                )

            value_type = self.analyze(node.value)

            original_type = self.symbols[node.name]

            if value_type != original_type:
                raise Exception(
                    f"Cannot assign {value_type} to {original_type}"
                )

            return value_type


        if isinstance(node, BinaryOpNode):

            left_type = self.analyze(node.left)
            right_type = self.analyze(node.right)

            if node.op in (
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.STAR,
                TokenType.SLASH
            ):

                if left_type == "number" and right_type == "number":
                    return "number"

                raise Exception(
                    f"Operator {node.op.value} requires numbers"
                )
            
            if node.op in (
                TokenType.GE,
                TokenType.GR,
                TokenType.LE,
                TokenType.LR,
                TokenType.EQ,
                TokenType.NEQ
            ):
                if left_type == "number" and right_type == "number":
                    return "bool"

                raise Exception(
                    f"Operator {node.op.value} requires numbers"
                )


        raise Exception(
            f"Unknown node type: {type(node).__name__}"
        )