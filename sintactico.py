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

    # Check if the second token is a valid identifier (variable name) or constant
    if not re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', tokens[1]) and not is_valid_constant(tokens[1]):
        return None

    # Check if there is an assignment operator and a value after the identifier
    if len(tokens) > 2 and tokens[2] == '=':
        # Join the tokens after the assignment operator to get the initialization value
        initial_value = ' '.join(tokens[3:])
    else:
        initial_value = None


def parse_short_declaration(input_string):
    tokens = re.findall(r'\w+|\S', input_string)
    if tokens[0] != "short":
        return None

    # Check if the second token is a valid identifier (variable name) or constant
    if not re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', tokens[1]) and not is_valid_constant(tokens[1]):
        return None

    # Check if there is an assignment operator and a value after the identifier
    if len(tokens) > 2 and tokens[2] == '=':
        # Join the tokens after the assignment operator to get the initialization value
        initial_value = ' '.join(tokens[3:])
    else:
        initial_value = None

    return ("short", tokens[1], initial_value)

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

def parse_const_declaration(tokens):
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

def is_declaration(tokens):
    # List of valid data types
    valid_types = ['int', 'float', 'char']
    # List of valid modifiers
    valid_modifiers = ['short', 'long']

    if len(tokens) < 2:
        return False

    # Check if the first token is a valid modifier (optional)
    if tokens[0] in valid_modifiers:
        tokens = tokens[1:]

    # Check if the first token is a valid data type
    if tokens[0] not in valid_types:
        return False

    # Check if the second token is a valid identifier (variable name) or constant
    if not re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', tokens[1]) and not is_valid_constant(tokens[1]):
        return False

    # Check if there is an assignment operator and a value after the identifier
    if len(tokens) > 2 and tokens[2] == '=' and len(tokens) < 4:
        return False

    return True

def is_valid_constant(token):
    # Regular expression pattern for numeric constants
    pattern_numeric = r'\b\d+(\.\d*)?\b'
    # Regular expression pattern for character constants
    pattern_character = r'\'[^\\\']*\''

    # Check if the token matches any of the constant patterns
    return re.match(pattern_numeric, token) or re.match(pattern_character, token)

def is_control_structure(tokens):
    # List of valid control structure keywords
    valid_keywords = ['for', 'while', 'if']

    if len(tokens) < 2:
        return False

    # Check if the first token is a valid control structure keyword
    if tokens[0] not in valid_keywords:
        return False

    # Check if there is a valid condition inside parentheses for 'if' and 'while'
    if tokens[0] in ['if', 'while']:
        if len(tokens) < 3 or tokens[1] != '(' or tokens[-1] != ')':
            return False

    # Check if there is a valid initialization, condition, and update for 'for'
    if tokens[0] == 'for':
        if len(tokens) < 6 or tokens[1] != '(' or tokens[3] != ';' or tokens[-2] != ')':
            return False

    return True


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
    if tokens[2] != '=':
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

def extract_parentheses_content(input_string):
    # Initializing variables
    stack = []
    result = []

    # Iterating over the characters in the input string
    for char in input_string:
        if char == '(':
            # If an opening parenthesis is encountered, push it onto the stack
            stack.append(char)
        elif char == ')':
            # If a closing parenthesis is encountered, pop characters from the stack
            # until an opening parenthesis is found
            if stack:
                stack.pop()
                if not stack:
                    # If the stack is empty, it means we have found the closing parenthesis
                    # for the content we want to extract. So, we add the characters to the result.
                    result.append(char)
            else:
                # If there's no matching opening parenthesis in the stack, raise an error
                raise SyntaxError("Mismatched parentheses in the input string")
        else:
            # If the character is not a parenthesis, add it to the result
            if stack:
                # If we are inside the parentheses, add the character to the result
                result.append(char)

    # After processing all characters, join the result list to get the content inside the parentheses as a string
    return ''.join(result)

def parse_condition(tokens):
    # Extracting the content inside the parentheses
    condition_content = extract_parentheses_content(tokens)
    
    # Parsing the expression inside the parentheses
    parse_expression(condition_content)

def extract_braces_content(input_string):
    # Initializing variables
    stack = []
    result = []

    # Iterating over the characters in the input string
    for char in input_string:
        if char == '{':
            # If an opening brace is encountered, push it onto the stack
            stack.append(char)
            if len(stack) > 1:
                # If this is not the first opening brace, add it to the result
                result.append(char)
        elif char == '}':
            # If a closing brace is encountered, pop characters from the stack
            # until an opening brace is found
            if stack:
                stack.pop()
                if not stack:
                    # If the stack is empty, it means we have found the closing brace
                    # for the content we want to extract. So, we stop iterating.
                    break
            else:
                # If there's no matching opening brace in the stack, raise an error
                raise SyntaxError("Mismatched braces in the input string")
        else:
            # If the character is not a brace, add it to the result
            if len(stack) > 1:
                # If we are inside the outermost braces, add the character to the result
                result.append(char)

    # After processing all characters, join the result list to get the content inside the braces as a string
    return ''.join(result)

def parse_else_statement(tokens):
    # Extracting the content inside the curly braces
    else_content = extract_braces_content(tokens)
    
    # Parsing the body of the "else" statement
    parse_body(re.findall(r'\w+|\S', else_content))


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

def is_valid_variable(variable_name):
    # Regular expression pattern for valid variable names
    pattern_variable = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'

    # Check if the variable name matches the valid variable pattern
    return re.match(pattern_variable, variable_name) is not None


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

def extract_body_until_closing_brace(tokens):
    # Initializing variables
    stack = []
    result = []

    # Iterating over the characters in the input tokens
    for token in tokens:
        if token == '{':
            # If an opening brace is encountered, push it onto the stack
            stack.append(token)
            if len(stack) > 1:
                # If this is not the first opening brace, add it to the result
                result.append(token)
        elif token == '}':
            # If a closing brace is encountered, pop characters from the stack
            # until an opening brace is found
            if stack:
                stack.pop()
                if not stack:
                    # If the stack is empty, it means we have found the closing brace
                    # for the content we want to extract. So, we stop iterating.
                    break
            else:
                # If there's no matching opening brace in the stack, raise an error
                raise SyntaxError("Mismatched braces in the input tokens")
        else:
            # If the token is not a brace, add it to the result
            if len(stack) > 1:
                # If we are inside the outermost braces, add the token to the result
                result.append(token)

    # After processing all tokens, return the result list containing the content inside the braces
    return result


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


def main():
    expressions = [
        "int opcion;",
        "float opcion2 = 0.0;",
        "char var = 'W';",
        "const char var = 'W';",
        "const char var = '\n';",
        "long int opcion3;",
        "short int opcion4 = 1;",
        "while(i > 3){\n\tcout << i << endl;\n\ti++;\n}",
        "if(opcion >= opcion2);\nif(opcion >= opcion2);\nelse\n\treturn;",
        "int var = sizeof(var / const);",
        "for (i = 1; i <= 10; ++i) {\n\tif (i == 3)\n\t\tcontinue;\n\tif (i == 7)\n\t\tbreak;\n}",
        "switch(expression) {\n\tdefault:\n\t\t// some statements to execute when default;\n\tcase '0':\n\t\t// some statements to execute when 1\n\t\tbreak;\n\tcase '1':\n\t\t// some statements to execute when 5\n\t\tbreak;\n}",
        "int i;\ndo {\n\tcout << i;\n\ti++;\n} while (i < 10);"
    ]

    for expression in expressions:
        tokens = re.findall(r'\w+|\S', expression)
        if tokens[0] == 'int':
            result = parse_int_declaration(expression)
        elif tokens[0] == 'float':
            result = parse_float_declaration(expression)
        elif tokens[0] == 'char':
            result = parse_char_declaration(expression)
        elif tokens[0] == 'long':
            result = parse_long_declaration(expression)
        elif tokens[0] == 'short':
            result = parse_short_declaration(expression)
        elif tokens[0] == 'while':
            result = is_control_structure(expression)
        elif tokens[0] == 'for':
            result = is_control_structure
        
        else:
            result = None

        print(f"Expression: {expression}\nAST: {result}\n")


if __name__ == "__main__":
    main()