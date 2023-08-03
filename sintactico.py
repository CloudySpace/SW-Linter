import re
def parse_int_declaration(input_string):
    # Tokenizando la entrada usando una expresión regular simple
    tokens = re.findall(r'\w+|\S', input_string)
    
    # Verificando la palabra clave 'int'
    if tokens[0] != "int":
        return None
    
    # Verificando el identificador (nombre de la variable)
    variable_name = tokens[1]
    
    # Verificando si hay una asignación inicial
    initial_value = None
    if len(tokens) > 3 and tokens[2] == "=":
        initial_value = tokens[3]
    
    # Devolviendo la representación del nodo del AST
    return ("int", variable_name, initial_value)

def parse_float_declaration(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "float":
        return None
    variable_name = tokens[1]
    initial_value = None
    if len(tokens) > 3 and tokens[2] == "=":
        initial_value = tokens[3]
    return ("float", variable_name, initial_value)

def parse_char_declaration(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "char":
        return None
    variable_name = tokens[1]
    initial_value = None
    if len(tokens) > 3 and tokens[2] == "=":
        initial_value = tokens[3]
    return ("char", variable_name, initial_value)

def parse_long_declaration(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "long":
        return None
    variable_name = tokens[1]
    initial_value = None
    if len(tokens) > 3 and tokens[2] == "=":
        initial_value = tokens[3]
    return ("long", variable_name, initial_value)

def parse_short_declaration(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "short":
        return None
    variable_name = tokens[1]
    initial_value = None
    if len(tokens) > 3 and tokens[2] == "=":
        initial_value = tokens[3]
    return ("short", variable_name, initial_value)

def parse_declaration(tokens):
    variable_type = tokens[0]
    variable_name = tokens[1]
    if tokens[2] == '=':
        initial_value = parse_expression(tokens[3:]) # Analiza el valor inicial
        return {'type': 'declaration', 'var_type': variable_type, 'name': variable_name, 'value': initial_value}, 4
    else:
        return {'type': 'declaration', 'var_type': variable_type, 'name': variable_name}, 2

def parse_control_structure(tokens):
    control_type = tokens[0]
    condition = parse_expression(tokens[1:]) # Analiza la condición
    body, size = parse_body(tokens[3:]) # Analiza el cuerpo
    return {'type': control_type, 'condition': condition, 'body': body}, 3 + size

def parse_if_else_statement(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "if":
        return None
    condition = tokens[1:tokens.index(')') + 1]
    body = tokens[tokens.index('{') + 1:tokens.index('}')]
    else_body = None
    if "else" in tokens:
        else_body = tokens[tokens.index('else') + 2:tokens[::-1].index('}') - 1]
    return ("if-else", condition, body, else_body)

def parse_while_statement(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "while":
        return None
    condition = tokens[1:tokens.index(')') + 1]
    body = tokens[tokens.index('{') + 1:tokens.index('}')]
    return ("while", condition, body)

def parse_for_statement(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "for":
        return None

    # Separando las partes de la declaración for
    for_parts = input_string[input_string.index('(') + 1:input_string.index(')')].split(';')
    initialization = re.findall(r'\w+|\S', for_parts[0])
    condition = re.findall(r'\w+|\S', for_parts[1])
    increment = re.findall(r'\w+|\S', for_parts[2])
    body = tokens[tokens.index('{') + 1:tokens.index('}')]

    return ("for", initialization, condition, increment, body)

def parse_switch_case_statement(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "switch":
        return None
    expression = tokens[1:tokens.index(')') + 1]
    cases = []
    body_tokens = tokens[tokens.index('{') + 1:tokens.index('}')]
    i = 0
    while i < len(body_tokens):
        if body_tokens[i] == "case":
            case_expression = body_tokens[i + 1]
            case_body = []
            i += 2
            while i < len(body_tokens) and body_tokens[i] != "case" and body_tokens[i] != "default":
                case_body.append(body_tokens[i])
                i += 1
            cases.append(("case", case_expression, case_body))
        elif body_tokens[i] == "default":
            default_body = []
            i += 1
            while i < len(body_tokens):
                default_body.append(body_tokens[i])
                i += 1
            cases.append(("default", default_body))
        else:
            i += 1
    return ("switch-case", expression, cases)


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

ddef parse_const_declaration(tokens):
    if tokens[0] != 'const':
        raise SyntaxError("Expected 'const'")
    
    # Identificar el tipo de la constante
    const_type = tokens[1]
    
    # Llamar a la función correspondiente basada en el tipo y obtener el nodo del tipo
    type_node = None
    if const_type == 'int':
        type_node = parse_int_declaration(tokens[1:])
    elif const_type == 'float':
        type_node = parse_float_declaration(tokens[1:])
    elif const_type == 'char':
        type_node = parse_char_declaration(tokens[1:])
    elif const_type == 'long':
        type_node = parse_long_declaration(tokens[1:])
    elif const_type == 'short':
        type_node = parse_short_declaration(tokens[1:])
    else:
        raise SyntaxError(f"Unexpected type '{const_type}' for const declaration")
    
    # Construir y retornar el nodo AST para la declaración constante
    return {'type': 'const_declaration', 'const_type': const_type, 'declaration': type_node}


def parse_body(tokens):
    index = 0
    body_nodes = []  # Lista para almacenar los nodos del cuerpo

    # Continuamos analizando mientras haya tokens
    while index < len(tokens):
        # Verificamos si estamos en un caso ('case') o en el caso predeterminado ('default')
        if tokens[index] == 'case' or tokens[index] == 'default':
            node, size = parse_case_or_default(tokens[index:])
            body_nodes.append(node)
            index += size
        # Verificamos si estamos en una declaración
        elif is_declaration(tokens[index:]):
            node, size = parse_declaration(tokens[index:])
            body_nodes.append(node)
            index += size
        # Verificamos si estamos en una estructura de control (como un 'if' o un 'while')
        elif is_control_structure(tokens[index:]):
            node, size = parse_control_structure(tokens[index:])
            body_nodes.append(node)
            index += size
        else:
            raise SyntaxError(f"Unexpected tokens in body: '{tokens[index:]}'")
    
    # Retornar la lista de nodos que representan el cuerpo de código
    return body_nodes

def parse_case_or_default(tokens):
    if tokens[0] == 'case':
        case_expression = parse_expression(tokens[1:]) # Analiza la expresión del caso
        body, size = parse_body(tokens[3:]) # Analiza el cuerpo del caso
        return {'type': 'case', 'expression': case_expression, 'body': body}, 3 + size
    elif tokens[0] == 'default':
        body, size = parse_body(tokens[1:]) # Analiza el cuerpo del caso predeterminado
        return {'type': 'default', 'body': body}, 1 + size
    else:
        raise SyntaxError(f"Expected 'case' or 'default', but found '{tokens[0]}'")

def extract_expression_until_opening_brace(tokens):
    expression_tokens = []
    index = 0
    while tokens[index] != '{':
        expression_tokens.append(tokens[index])
        index += 1
    return expression_tokens, index

def extract_body_until_keyword(tokens, keyword):
    body_tokens = []
    index = 0
    while index < len(tokens) and tokens[index] != keyword:
        body_tokens.append(tokens[index])
        index += 1
    return body_tokens, index

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

def parse_logical_expression(tokens):
    # La expresión puede incluir operadores lógicos
    index = 0
    while index < len(tokens):
        if tokens[index] in ('&&', '||'):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

def parse_sizeof(tokens):
    # Verificamos que el primer token sea 'sizeof'
    if tokens[0] != 'sizeof':
        raise SyntaxError(f"Expected 'sizeof', got '{tokens[0]}'")

    # Extraemos el argumento de sizeof (puede ser una variable o constante)
    argument_token = tokens[1].strip('()')

    # Verificamos que el argumento sea una variable o constante válida
    if not (is_valid_variable(argument_token) or is_valid_constant(argument_token)):
        raise SyntaxError(f"Invalid argument for sizeof: '{argument_token}'")

def parse_cases(tokens):
    index = 0
    while index < len(tokens):
        # Verificamos si estamos en un caso ('case') o en el caso predeterminado ('default')
        if tokens[index] == 'case' or tokens[index] == 'default':
            index += parse_case_or_default(tokens[index:])
        else:
            raise SyntaxError(f"Unexpected tokens in cases: '{tokens[index:]}'")

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

def parse_variable(token):
    # Utilizamos la expresión regular de lexico.py para verificar si el token es un identificador válido
    pattern_identifiers = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    if not re.match(pattern_identifiers, token):
        raise SyntaxError(f"Invalid variable: '{token}'")

def parse_cout(tokens):
    # Verificamos que los primeros tokens sean 'cout' y '<<'
    if tokens[0] != 'cout' or tokens[1] != '<<':
        raise SyntaxError(f"Expected 'cout <<', got '{tokens[0]} {tokens[1]}'")

    # Extraemos y analizamos la expresión a imprimir
    expression_tokens = tokens[2:]
    parse_expression(expression_tokens)

def parse_relational_expression(tokens):
    # La expresión puede incluir operadores relacionales
    index = 0
    while index < len(tokens):
        if tokens[index] in ('<=', '>=', '<', '>', '==', '!='):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

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

def parse_arithmetic_expression(tokens):
    # La expresión puede incluir operadores aritméticos
    index = 0
    while index < len(tokens):
        if tokens[index] in ('+', '*', '/', '-', '++', '--'):
            parse_expression(tokens[:index])
            parse_expression(tokens[index + 1:])
            break
        index += 1

def parse_return_statement(tokens):
    # Verificamos que el primer token sea 'return'
    if tokens[0] != 'return':
        raise SyntaxError(f"Expected 'return', got '{tokens[0]}'")

    # Extraemos y analizamos la expresión a devolver
    expression_tokens = tokens[1:]
    parse_expression(expression_tokens)