from tokens import TokenType
from nodes import *

class CodeGenerator:
    def __init__(self):
        self.data_section = []
        self.text_section = []
        self.variables = set()
        self.string_count = 0

    def generate(self, node):
        if isinstance(node, ProgramNode):
            for statement in node.statements:
                self.generate(statement)
            return

        if isinstance(node, VarDeclNode):
            if node.name not in self.variables:
                self.variables.add(node.name)

                self.data_section.append(
                    f"{node.name} dq 0"
                )

            self.generate_expression(node.value)

            self.text_section.append(
                f"mov [{node.name}], rax"
            )

            return
        
        if isinstance(node, AssignmentNode):
            self.generate_expression(node.value)
            self.text_section.append(
                f"mov [{node.name}], rax"
            )
            return
        
        raise Exception(
            f"Unknown statement node: {type(node).__name__}"
        )

    def generate_expression(self, node):
        if isinstance(node, NumberNode):
            self.text_section.append(
                f"mov rax, {int(node.value)}"
            )

            return
        
        if isinstance(node, StringNode):
            label = f"str_{self.string_count}"

            self.string_count += 1

            self.data_section.append(
                f'{label} db "{node.value}", 0'
            )

            self.text_section.append(
                f"lea rax, [{label}]"
            )

            return

        if isinstance(node, VariableNode):
            self.text_section.append(
                f"mov rax, [{node.name}]"
            )
            return
        
        if isinstance(node, BinaryOpNode):
            self.generate_expression(node.left)

            self.text_section.append(
                "push rax"
            )

            self.generate_expression(node.right)

            self.text_section.append(
                "pop rbx"
            )

            # PLUS
            if node.op == TokenType.PLUS:

                self.text_section.append(
                    "add rax, rbx"
                )

                return

            # MINUS
            if node.op == TokenType.MINUS:

                self.text_section.append(
                    "sub rbx, rax"
                )

                self.text_section.append(
                    "mov rax, rbx"
                )

                return

            # MULTIPLY
            if node.op == TokenType.STAR:

                self.text_section.append(
                    "imul rax, rbx"
                )

                return

            # DIVIDE
            if node.op == TokenType.SLASH:

                self.text_section.append(
                    "mov rdx, 0"
                )

                self.text_section.append(
                    "mov rcx, rax"
                )

                self.text_section.append(
                    "mov rax, rbx"
                )

                self.text_section.append(
                    "idiv rcx"
                )

                return
            
        raise Exception(
            f"Unknown expression node: {type(node).__name__}"
        )
    
    def build(self):
        data = "section .data\n"

        for line in self.data_section:
            data += f"    {line}\n"

        text = (
            "section .text\n"
            "global _start\n\n"
            "_start:\n"
        )

        for line in self.text_section:
            text += f"    {line}\n"

        text += (
            "    mov rax, 60\n"
            "    mov rdi, 0\n"
            "    syscall\n"
        )

        return data + text
    