import re
from sys import argv

class LexicalError(Exception):
    def __init__(self, line, column, token):
        self.line = line
        self.column = column
        self.token = token

def tokenize_code(code):
    tokens = []
    line_number = 1

    # Expresiones regulares para los tokens
    pattern_keywords = r'\b(int|float|char|long|short|const|while|if|else|for|do|switch|case|break|default|sizeof|cout|continue|return)\b'
    pattern_operators = r'\+\+|--|\+|-|\*|/|&&|\|\||==|!=|<=|>=|<|>'
    pattern_assignment = r'='
    pattern_identifiers = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    pattern_constants = r'\b\d+(\.\d*)?\b|\'[^\']*\''
    pattern_strings = r'\".*?\"'
    pattern_punctuation = r'[;{}()]'
    pattern_spaces = r'\s+'
    pattern_end = r'\$'

    # Unimos todas las expresiones regulares en una única expresión
    token_patterns = f'({pattern_keywords})|({pattern_operators})|({pattern_assignment})|({pattern_identifiers})|({pattern_constants})|({pattern_strings})|({pattern_punctuation})|({pattern_spaces}|{pattern_end})'

    for match in re.finditer(token_patterns, code):
        for i in range(1, 10):
            if match.group(i):
                token = (match.group(i), match.start(), line_number)
                tokens.append(token)
                break
        if match.group(10):
            line_number += 1
    return tokens

class SyntaxError(Exception):
    def __init__(self, message):
        self.message = message

# Define las funciones para cada no terminal en las reglas de producción
def S(tokens):
    if tokens or tokens[0][0]== '$':
        return
    if tokens and (tokens[0][0] == 'int' or tokens[0][0] == 'const'):
        B(tokens[1:])
    elif tokens and (tokens[0][0] == 'float' or tokens[0][0] == 'const'):
        B(tokens[1:])
    elif tokens and tokens[0][0] == 'char':
        A(tokens[1:])
    else:
        raise SyntaxError('Error léxico en S')

def B(tokens):
    if tokens or tokens[0][0]== '$':
            return
    if tokens and tokens[0][0] == 'var':
        C(tokens[1:])
    else:
        raise SyntaxError('Error léxico en B')

def C(tokens):
    if tokens or tokens[0][0]== '$':
            return
    if tokens and tokens[0][0] == ';':
        pass
    else:
        raise SyntaxError('Error léxico en C')

def A(tokens):
    if tokens or tokens[0][0]== '$':
            return
    if tokens and tokens[0][0] == 'var':
        B(tokens[1:])
    else:
        raise SyntaxError('Error léxico en A')

# Resto de las funciones para los demás no terminales ...

# Implementa el analizador léxico predictivo recursivo
def parse(tokens):
    try:
        S(tokens)
        print('Análisis léxico exitoso.')
    except SyntaxError as syntax_error:
        print(f'Error léxico: {syntax_error.message}')

# Código que deseas analizar
def main():
    if len(argv) == 2:
        code = argv[1]
        code_to_tokenize = str(code)

        try:
            # Utilizamos el analizador léxico para obtener los tokens del código
            tokens = tokenize_code(code_to_tokenize)

            # Imprimimos los tokens encontrados
            for token, position, line in tokens:
                print(f'Token: "{token}", Posición: {position}, Línea: {line}')

            # Utilizamos el analizador léxico para analizar los tokens
            parse(tokens)

        except LexicalError as lex_error:
            print(f'Error léxico: Token no reconocido: "{lex_error.token}" en la línea {lex_error.line}, columna {lex_error.column}')
    else:
        code_to_tokenize = '''
        while(i > 3){
        cout << i << endl;
        i++;	
        };
        $
        '''

        try:
            # Utilizamos el analizador léxico para obtener los tokens del código
            tokens = tokenize_code(code_to_tokenize)

            # Imprimimos los tokens encontrados
            for token, position, line in tokens:
                print(f'Token: "{token}", Posición: {position}, Línea: {line}')

            # Utilizamos el analizador léxico para analizar los tokens
            parse(tokens)

        except LexicalError as lex_error:
            print(f'Error léxico: Token no reconocido: "{lex_error.token}" en la línea {lex_error.line}, columna {lex_error.column}')

if __name__ == "__main__":
    main()
