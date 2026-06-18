#!/usr/bin/env python3

import sys
import subprocess

from lexer import lexer
from parser import Parser
from analyzer import SemanticAnalyzer
from optimizer import Optimizer
from compiler import CodeGenerator

if len(sys.argv) < 2:
    print("Usage: python3 ura.py <file.ura>")
    exit(1)

filename = sys.argv[1]

with open(filename, "r") as f:
    source = f.read()

tokens = lexer(source)

parser = Parser(tokens)

ast = parser.parse()

semantic = SemanticAnalyzer()
semantic.analyze(ast)

optimizer = Optimizer()

optimized_ast = optimizer.optimize(ast)

generator = CodeGenerator()

generator.generate(optimized_ast)

asm = generator.build()

base = filename.replace(".ura", "")

asm_file = base + ".asm"
obj_file = base + ".o"
exe_file = base

with open(asm_file, "w") as f:
    f.write(asm)

print(f"Generated {asm_file}")

subprocess.run([
    "nasm",
    "-f",
    "elf64",
    asm_file,
    "-o",
    obj_file
], check=True)

print(f"Generated {obj_file}")

subprocess.run([
    "ld",
    obj_file,
    "-o",
    exe_file
], check=True)

print(f"Built executable: {exe_file}")

print("Running program...")

subprocess.run([
    f"./{exe_file}"
])