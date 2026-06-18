class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

class NumberNode:
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value

class BoolNode:
    def __init__(self, value):
        self.value = value

class VariableNode:
    def __init__(self, name):
        self.name = name

class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode:
    def __init__(self, op, value):
        self.op = op
        self.value = value

class VarDeclNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class WhileNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class BlockNode:
    def __init__(self, statements):
        self.statements = statements