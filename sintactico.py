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

#Función para Bloques switch-case

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
    # Inicializamos un índice para recorrer los tokens
    index = 0

    # Verificamos el primer token (puede ser un identificador, constante numérica o constante de caracteres)
    if not (is_identifier(tokens[index]) or is_numeric_constant(tokens[index]) or is_character_constant(tokens[index])):
        raise SyntaxError(f"Invalid expression: '{tokens}'")

    index += 1

    # Continuamos analizando mientras haya tokens
    while index < len(tokens):
        # Esperamos un operador binario
        if not is_binary_operator(tokens[index]):
            raise SyntaxError(f"Expected binary operator, got: '{tokens[index]}'")
        
        index += 1

        # Esperamos otro identificador, constante numérica o constante de caracteres
        if not (is_identifier(tokens[index]) or is_numeric_constant(tokens[index]) or is_character_constant(tokens[index])):
            raise SyntaxError(f"Invalid expression: '{tokens}'")

        index += 1

    # Si todo está bien, la expresión es válida

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

#Esta función extrae los tokens que constituyen el cuerpo de un caso, deteniéndose en el próximo case, default, o llave de cierre }.
def extract_body_until_case_or_brace(tokens):
    body_tokens = []
    index = 0
    while index < len(tokens) and tokens[index] not in ('case', 'default', '}'):
        body_tokens.append(tokens[index])
        index += 1
    return body_tokens


#Función para Analizar los Casos (case) dentro de los corchetes de una declaración switch.
def parse_cases(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index] == 'case':
            index += parse_case(tokens[index:])
        elif tokens[index] == 'default':
            index += parse_default_case(tokens[index:])
        else:
            raise SyntaxError("Expected 'case' or 'default'")

#Función para Analizar un Caso Individual dentro de un bloque switch.
def parse_case(tokens):
    if tokens[0] != 'case':
        raise SyntaxError("Expected 'case'")
    
    # Analizar la constante después de 'case'
    parse_constant(tokens[1])
    
    if tokens[2] != ':':
        raise SyntaxError("Expected ':'")
    
    # Analizar el cuerpo del caso
    body_tokens = extract_body_until_case_or_brace(tokens[3:])
    parse_body(body_tokens)
    
    return 3 + len(body_tokens)
# Función para Analizar el Caso default dentro de un bloque switch.
def parse_default_case(tokens):
    if tokens[0] != 'default':
        raise SyntaxError("Expected 'default'")
    if tokens[1] != ':':
        raise SyntaxError("Expected ':'")
    
    # Analizar el cuerpo del caso default
    body_tokens = extract_body_until_brace(tokens[2:])
    parse_body(body_tokens)
    
    return 2 + len(body_tokens)

#La función S maneja la declaración de un int con un sizeof o un sizeof solo.
def S(tokens):
    if tokens and tokens[0] == 'int':
        A(tokens[1:])
    elif tokens and tokens[0] == 'sizeof':
        if tokens[1] == '(' and tokens[3] == ')':
            # Se valida que tenga la forma sizeof (var);
            pass
        else:
            raise SyntaxError('Error sintáctico en S')
    else:
        raise SyntaxError('Error sintáctico en S')

#La función A maneja la declaración de una variable después de la palabra clave int.
def A(tokens):
    if tokens and tokens[0] == 'var':
        B(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en A')

#La función B maneja el operador de asignación (igual) en la declaración.
def B(tokens):
    if tokens and tokens[0] == 'igual':
        C(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en B')

#La función C maneja el uso de sizeof en la declaración.
def C(tokens):
    if tokens and tokens[0] == 'sizeof':
        # Aquí puedes validar la forma de sizeof según las reglas del lenguaje
        pass
    else:
        raise SyntaxError('Error sintáctico en C')

#La función S maneja la estructura de una sentencia IF.
def S(tokens):
    if tokens and tokens[0] == 'if':
        if tokens[1] == '(':
            A(tokens[2:])
        else:
            raise SyntaxError('Error sintáctico en S')
    else:
        raise SyntaxError('Error sintáctico en S')

#La función A maneja la comparación dentro de la sentencia IF.
def A(tokens):
    if tokens and is_comparison_operator(tokens[0]):
        B(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en A')

#La función B maneja los tipos int, char, float, o var dentro de la sentencia IF.
def B(tokens):
    if tokens and tokens[0] in ('int', 'char', 'float', 'var'):
        E(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en B')


#Las funciones E y F manejan las condiciones adicionales y los operadores lógicos dentro de la sentencia IF
def E(tokens):
    if not tokens:
        pass
    elif tokens[0] in ('&&', '||'):
        F(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en E')

def F(tokens):
    if tokens and is_variable(tokens[0]):
        A(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en F')

#Esta función verifica si un token es uno de los operadores de comparación permitidos en el lenguaje (<=, >=, <, >, ==, !=).        
def is_comparison_operator(token):
    valid_operators = ['<=', '>=', '<', '>', '==', '!=']
    return token in valid_operators

#Esta función verifica si un token es un identificador de variable válido
def is_variable(token):
    pattern = r'^[a-zA-Z_][a-zA-Z_0-9]*$'
    return re.match(pattern, token) is not None

#La función G maneja el bloque else después de una sentencia IF.
def G(tokens):
    if tokens and tokens[0] == 'else':
        H(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en G')

#La función H maneja el contenido dentro del bloque else.
def H(tokens):
    if tokens and is_variable(tokens[0]):
        C(tokens[1:])
    else:
        raise SyntaxError('Error sintáctico en H')

#La función C maneja la salida (cout) dentro de la sentencia IF.
def C(tokens):
    # Verificamos que los tokens comiencen con 'cout << var;'
    if tokens and tokens[0] == 'cout' and tokens[1] == '<<' and is_variable(tokens[2]) and tokens[3] == ';':
        # Verificamos que el siguiente token sea '}' para cerrar el bloque IF
        if tokens[4] == '}':
            # Llamamos a la función G para manejar el bloque ELSE opcional
            G(tokens[5:])
        else:
            raise SyntaxError(f"Expected '}', got '{tokens[4]}'")
    else:
        raise SyntaxError('Error sintáctico en C')







