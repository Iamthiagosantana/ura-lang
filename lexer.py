from tokens import TokenType

def lexer(line):
    i = 0
    tokens = []
    ops = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "=": TokenType.EQUAL,
        ">": TokenType.GR,
        "<": TokenType.LR,
        ">=": TokenType.GE,
        "<=": TokenType.LE,
        "==": TokenType.EQ,
        "!=": TokenType.NEQ,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LKEY,
        "}": TokenType.RKEY
    }
    while i < len(line):
        char = line[i]

        # Whitespace
        if char.isspace():
            i += 1
            continue
        
        # Numbers
        if char.isdigit() or char == '.':
            num = ""
            point_count = 0

            while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                char = line[i]

                if char == '.':
                    point_count += 1

                if point_count > 1:
                    raise Exception(
                        "Invalid syntax: numbers can only have one decimal point"
                    )

                num += char
                i += 1

            tokens.append((TokenType.NUMBER, float(num)))
            continue
        
        # Variables
        if char.isalpha() or char == '_':
            ident = ""

            while i < len(line) and (
                line[i].isalnum() or line[i] == '_'
            ):
                ident += line[i]
                i += 1

            if ident == "var":
                tokens.append((TokenType.VAR, ident))
            elif ident == "while":
                tokens.append((TokenType.WHILE, ident))
            elif ident == "true" or ident == "false":
                tokens.append((TokenType.BOOL, ident))
            else:
                tokens.append((TokenType.IDENTIFIER, ident))

            continue

        # Strings
        if char == '"':
            i += 1
            string = ""

            while i < len(line) and line[i] != '"':
                string += line[i]
                i += 1

            if i >= len(line):
                raise Exception("Unterminated string")

            i += 1  # Skip closing quote

            tokens.append((TokenType.STRING, string))
            continue

        # Operators
        if i < len(line) - 1:
            double_char = line[i:i+2]
            if double_char in ops:
                tokens.append((ops[double_char], double_char))
                i += 2
                continue

        if char in ops:
            tokens.append((ops[char], char))
            i += 1
            continue

        raise Exception(f"Unknown character: {char}")

    tokens.append((TokenType.EOF, None))
    return tokens