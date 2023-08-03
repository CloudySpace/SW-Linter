#Analizador sintáctico 
import re

#Función para Declaraciones int
def parse_int_declaration(tokens):
    if tokens[0] != 'int':
        raise SyntaxError("Expected 'int'")
    if not is_identifier(tokens[1]):
        raise SyntaxError("Expected identifier")
    # Continuar con el análisis sintáctico de la declaración

#Función para Declaraciones float
def parse_float_declaration(tokens):
    if tokens[0] != 'float':
        raise SyntaxError("Expected 'float'")
    if not is_identifier(tokens[1]):
        raise SyntaxError("Expected identifier")
    if tokens[2] == '=':
        parse_assignment(tokens[3:])
    elif tokens[2] == ';':
        pass # Fin de la declaración
    else:
        raise SyntaxError("Expected '=' or ';'")

#Función para Declaraciones char
def parse_char_declaration(tokens):
    if tokens[0] != 'char':
        raise SyntaxError("Expected 'char'")
    if not is_identifier(tokens[1]):
        raise SyntaxError("Expected identifier")
    if tokens[2] == '=':
        parse_assignment(tokens[3:])
    elif tokens[2] == ';':
        pass # Fin de la declaración
    else:
        raise SyntaxError("Expected '=' or ';'")

#Función para Declaraciones long
def parse_long_declaration(tokens):
    if tokens[0] != 'long':
        raise SyntaxError("Expected 'long'")
    if not is_identifier(tokens[1]):
        raise SyntaxError("Expected identifier")
    if tokens[2] == '=':
        parse_assignment(tokens[3:])
    elif tokens[2] == ';':
        pass # Fin de la declaración
    else:
        raise SyntaxError("Expected '=' or ';'")

#Función para Declaraciones short
def parse_short_declaration(tokens):
    if tokens[0] != 'short':
        raise SyntaxError("Expected 'short'")
    if not is_identifier(tokens[1]):
        raise SyntaxError("Expected identifier")
    if tokens[2] == '=':
        parse_assignment(tokens[3:])
    elif tokens[2] == ';':
        pass # Fin de la declaración
    else:
        raise SyntaxError("Expected '=' or ';'")

# Función para Declaraciones const
#primero verifica si la declaración comienza con la palabra clave const. Luego, identifica el tipo de la constante (como int, float, char, etc.) y llama a la función correspondiente para analizar el resto de la declaración. Esto permite una fácil extensión para admitir más tipos en el futuro.
def parse_const_declaration(tokens):
    if tokens[0] != 'const':
        raise SyntaxError("Expected 'const'")
    
    # Identificar el tipo de la constante
    const_type = tokens[1]
    
    # Llamar a la función correspondiente basada en el tipo
    if const_type == 'int':
        parse_int_declaration(tokens[1:])
    elif const_type == 'float':
        parse_float_declaration(tokens[1:])
    elif const_type == 'char':
        parse_char_declaration(tokens[1:])
    elif const_type == 'long':
        parse_long_declaration(tokens[1:])
    elif const_type == 'short':
        parse_short_declaration(tokens[1:])
    else:
        raise SyntaxError(f"Unexpected type '{const_type}' for const declaration")

#unción para Ciclos while

def parse_while_statement(tokens):
    if tokens[0] != 'while':
        raise SyntaxError("Expected 'while'")
    if tokens[1] != '(':
        raise SyntaxError("Expected '('")
    
    # Analizar la condición dentro de los paréntesis
    condition_tokens = extract_parentheses_content(tokens[2:])
    parse_condition(condition_tokens)
    
    # Analizar el cuerpo del ciclo
    body_tokens = extract_braces_content(tokens[2 + len(condition_tokens):])
    parse_body(body_tokens)

#Función para Condicionales if-else
def parse_if_statement(tokens):
    if tokens[0] != 'if':
        raise SyntaxError("Expected 'if'")
    if tokens[1] != '(':
        raise SyntaxError("Expected '('")
    
    # Analizar la condición dentro de los paréntesis
    condition_tokens = extract_parentheses_content(tokens[2:])
    parse_condition(condition_tokens)
    
    # Analizar el cuerpo del if
    body_tokens = extract_braces_content(tokens[2 + len(condition_tokens):])
    parse_body(body_tokens)
    
    # Analizar el cuerpo del else si existe
    else_tokens = tokens[3 + len(condition_tokens) + len(body_tokens):]
    if else_tokens and else_tokens[0] == 'else':
        parse_else_statement(else_tokens[1:])

#Función Principal para Analizar DO WHILE
def parse_do_while_statement(tokens):
    # Verificamos la palabra clave 'do'
    if tokens[0] != 'do':
        raise SyntaxError(f"Expected 'do', got '{tokens[0]}'")

    # Extraemos y analizamos el cuerpo del bucle
    body_tokens, index = extract_body_until_keyword(tokens[1:], 'while')
    parse_body(body_tokens)

    # Verificamos la palabra clave 'while'
    if tokens[index + 1] != 'while':
        raise SyntaxError(f"Expected 'while', got '{tokens[index + 1]}'")

    # Extraemos y analizamos la condición
    condition_tokens = extract_condition_until_semicolon(tokens[index + 2:])
    parse_expression(condition_tokens)

#Función Auxiliar para Extraer el Cuerpo del Bucle
def extract_body_until_keyword(tokens, keyword):
    body_tokens = []
    index = 0
    while index < len(tokens) and tokens[index] != keyword:
        body_tokens.append(tokens[index])
        index += 1
    return body_tokens, index

#Función Auxiliar para Extraer la Condición
def extract_condition_until_semicolon(tokens):
    condition_tokens = []
    index = 0
    while index < len(tokens) and tokens[index] != ';':
        condition_tokens.append(tokens[index])
        index += 1
    # Verificamos que la condición termine con un punto y coma
    if tokens[index] != ';':
        raise SyntaxError(f"Expected ';', got '{tokens[index]}'")
    return condition_tokens

#Función Principal para Analizar FOR
def parse_for_statement(tokens):
    # Verificamos la palabra clave 'for'
    if tokens[0] != 'for':
        raise SyntaxError(f"Expected 'for', got '{tokens[0]}'")

    # Extraemos y analizamos las partes de la sentencia for
    initialization_tokens, condition_tokens, update_tokens, index = extract_for_parts(tokens[1:])
    parse_expression(initialization_tokens)
    parse_expression(condition_tokens)
    parse_expression(update_tokens)

    # Extraemos y analizamos el cuerpo del bucle
    body_tokens = extract_body_until_closing_brace(tokens[index + 1:])
    parse_body(body_tokens)

#Función Auxiliar para Extraer las Partes de la Sentencia FOR
def extract_for_parts(tokens):
    # Verificamos el paréntesis de apertura
    if tokens[0] != '(':
        raise SyntaxError(f"Expected '(', got '{tokens[0]}'")

    # Extraemos las partes separadas por punto y coma
    initialization_tokens, condition_tokens, update_tokens = [], [], []
    part = initialization_tokens
    index = 1
    while tokens[index] != ')':
        if tokens[index] == ';':
            if part is initialization_tokens:
                part = condition_tokens
            elif part is condition_tokens:
                part = update_tokens
        else:
            part.append(tokens[index])
        index += 1

    # Verificamos el paréntesis de cierre
    if tokens[index] != ')':
        raise SyntaxError(f"Expected ')', got '{tokens[index]}'")

    return initialization_tokens, condition_tokens, update_tokens, index

#Función para Bloques switch-case
#Función Principal para Analizar switch-case
def parse_switch_statement(tokens):
    # Verificamos la palabra clave 'switch'
    if tokens[0] != 'switch':
        raise SyntaxError(f"Expected 'switch', got '{tokens[0]}'")

    # Extraemos y analizamos la expresión
    expression_tokens, index = extract_expression_until_opening_brace(tokens[1:])
    parse_expression(expression_tokens)

    # Extraemos y analizamos los casos
    case_tokens = extract_body_until_closing_brace(tokens[index + 1:])
    parse_cases(case_tokens)

#Función Auxiliar para Extraer la Expresión
def extract_expression_until_opening_brace(tokens):
    expression_tokens = []
    index = 0
    while tokens[index] != '{':
        expression_tokens.append(tokens[index])
        index += 1
    return expression_tokens, index

#Función Auxiliar para Analizar los Casos
def parse_cases(tokens):
    index = 0
    while index < len(tokens):
        # Verificamos si estamos en un caso ('case') o en el caso predeterminado ('default')
        if tokens[index] == 'case' or tokens[index] == 'default':
            index += parse_case_or_default(tokens[index:])
        else:
            raise SyntaxError(f"Unexpected tokens in cases: '{tokens[index:]}'")

#Función Auxiliar para Analizar un Caso o el Caso Predeterminado
def parse_case_or_default(tokens):
    if tokens[0] == 'case':
        # Analizar un caso individual
        parse_expression(tokens[1:-1])  # Asume que 'break;' está al final
    elif tokens[0] == 'default':
        # Analizar el caso predeterminado
        parse_body(tokens[1:-1])  # Asume que 'break;' está al final
    else:
        raise SyntaxError(f"Expected 'case' or 'default', got '{tokens[0]}'")


#Esta función analiza una constante en un caso, como el valor numérico después de la palabra clave case.
def parse_constant(token):
    # Expresión regular para constantes numéricas enteras y flotantes
    pattern_numeric = r'\b\d+(\.\d*)?\b'
    # Expresión regular para constantes de caracteres
    pattern_character = r'\'[^\\\']*\''

    # Verificamos si el token coincide con una constante numérica
    if re.match(pattern_numeric, token):
        return

    # Verificamos si el token coincide con una constante de caracteres
    if re.match(pattern_character, token):
        return

    # Si no coincide con ninguna de las anteriores, se lanza un error
    raise SyntaxError(f"Invalid constant: '{token}'")

#Esta función analiza una expresión, como la expresión dentro de los paréntesis en una declaración switch.
def parse_expression(tokens):
    # Analizamos operadores aritméticos
    if any(op in tokens for op in ('+', '-', '*', '/')):
        return parse_arithmetic_expression(tokens)

    # Analizamos operadores relacionales
    if any(op in tokens for op in ('<=', '>=', '<', '>', '==', '!=')):
        return parse_relational_expression(tokens)

    # Analizamos operadores lógicos
    if any(op in tokens for op in ('&&', '||')):
        return parse_logical_expression(tokens)

    # Analizamos una asignación
    if '=' in tokens:
        return parse_assignment(tokens)

    # Si la expresión es una variable, la analizamos
    if re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', tokens[0]):
        return parse_variable(tokens[0])

    # Aquí puedes agregar más reglas para analizar otros tipos de expresiones

    raise SyntaxError(f"Invalid expression: '{tokens}'")

#Esta función analiza el cuerpo de un caso, como las declaraciones dentro de un caso en un bloque switch.
def parse_body(tokens):
    index = 0

    # Continuamos analizando mientras haya tokens
    while index < len(tokens):
        # Verificamos si estamos en un caso ('case') o en el caso predeterminado ('default')
        if tokens[index] == 'case' or tokens[index] == 'default':
            index += parse_case_or_default(tokens[index:])
        # Verificamos si estamos en una declaración
        elif is_declaration(tokens[index:]):
            index += parse_declaration(tokens[index:])
        # Verificamos si estamos en una estructura de control (como un 'if' o un 'while')
        elif is_control_structure(tokens[index:]):
            index += parse_control_structure(tokens[index:])
        else:
            raise SyntaxError(f"Unexpected tokens in body: '{tokens[index:]}'")

#función para analizar una asignación:
def parse_assignment(tokens):
    # Extraemos la variable y el valor
    variable_token = tokens[0]
    value_tokens = tokens[2:]

    # Verificamos el operador de asignación
    if tokens[1] != '=':
        raise SyntaxError(f"Expected '=', got '{tokens[1]}'")

    # Analizamos la variable y el valor (puede ser una expresión)
    parse_variable(variable_token)
    parse_expression(value_tokens)


#Operadores Relacionales
def parse_relational_expression(tokens):
    # La expresión puede incluir operadores relacionales
    index = 0
    while index < len(tokens):
        if tokens[index] in ('<=', '>=', '<', '>', '==', '!='):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

#Operadores Aritméticos
def parse_arithmetic_expression(tokens):
    # La expresión puede incluir operadores aritméticos
    index = 0
    while index < len(tokens):
        if tokens[index] in ('+', '*', '/', '-', '++', '--'):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

#Operadores Lógicos
def parse_logical_expression(tokens):
    # La expresión puede incluir operadores lógicos
    index = 0
    while index < len(tokens):
        if tokens[index] in ('&&', '||'):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

def parse_variable(token):
    # Utilizamos la expresión regular de lexico.py para verificar si el token es un identificador válido
    pattern_identifiers = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    if not re.match(pattern_identifiers, token):
        raise SyntaxError(f"Invalid variable: '{token}'")

#Función para analizar el operador sizeof
def parse_sizeof(tokens):
    # Verificamos que el primer token sea 'sizeof'
    if tokens[0] != 'sizeof':
        raise SyntaxError(f"Expected 'sizeof', got '{tokens[0]}'")

    # Extraemos el argumento de sizeof (puede ser una variable o constante)
    argument_token = tokens[1].strip('()')

    # Verificamos que el argumento sea una variable o constante válida
    if not (is_valid_variable(argument_token) or is_valid_constant(argument_token)):
        raise SyntaxError(f"Invalid argument for sizeof: '{argument_token}'")

#Función para analizar la sentencia cout
def parse_cout(tokens):
    # Verificamos que los primeros tokens sean 'cout' y '<<'
    if tokens[0] != 'cout' or tokens[1] != '<<':
        raise SyntaxError(f"Expected 'cout <<', got '{tokens[0]} {tokens[1]}'")

    # Extraemos y analizamos la expresión a imprimir
    expression_tokens = tokens[2:]
    parse_expression(expression_tokens)

