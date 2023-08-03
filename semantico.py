# Terminal symbols
TERMINALS = [
    'var', 'constant', 'sizeof', 'cout', 'continue', 'return', 'case', 'break',
    'default', 'int', 'float', 'char', 'long', 'short', 'const', '=', '<=', '>=',
    '<', '>', '==', '!=', '+', '*', '/', '-', '++', '--', '&&', '||', 'while',
    'if', 'else', 'for', 'do', 'switch'
]

# Data structure for symbol table entry
class SymbolEntry:
    def __init__(self, name, data_type, is_constant=False):
        self.name = name
        self.data_type = data_type
        self.is_constant = is_constant

# Symbol table to store variable declarations
symbol_table = {}

# Helper function to add an entry to the symbol table
def add_entry(name, data_type, is_constant=False):
    if name in symbol_table:
        raise Exception(f"Variable '{name}' has already been declared.")
    symbol_table[name] = SymbolEntry(name, data_type, is_constant)

# Basic type hierarchy for type inference
TYPE_HIERARCHY = {
    'int': ['int'],
    'float': ['float'],
    'char': ['char'],
    'long int': ['int'],
    'short int': ['int'],
    'const char': ['char'],
    'const int': ['int'],
    'const float': ['float']
}

# Helper function for type inference
def get_most_specific_type(type1, type2):
    if type1 == type2:
        return type1
    if type2 in TYPE_HIERARCHY.get(type1, []):
        return type2
    if type1 in TYPE_HIERARCHY.get(type2, []):
        return type1
    return None

# Helper function for checking type compatibility
def check_type_compatibility(var_name, declared_type, assigned_type):
    if declared_type == assigned_type:
        return True
    if assigned_type in TYPE_HIERARCHY.get(declared_type, []):
        return True
    print(f"Error: Type mismatch for variable '{var_name}'. "
          f"Expected '{declared_type}', but found '{assigned_type}'.")
    return False

def analyze_expression(expression):
    tokens = expression.strip().split()
    if len(tokens) >= 3 and tokens[1] == '=':
        data_type = tokens[0]
        var_name = tokens[2]
        expr_tokens = tokens[3:]
        assigned_type = infer_expression_type(expr_tokens)
        if assigned_type:
            add_entry(var_name, data_type)
            if not check_type_compatibility(var_name, data_type, assigned_type):
                return False
        else:
            return False
    return True

def infer_expression_type(expr_tokens):
    # Simple type inference: assuming only one expression with one type in the code
    data_type = None
    for token in expr_tokens:
        if token.isdigit():
            data_type = get_most_specific_type(data_type, 'int')
        elif '.' in token and all(part.isdigit() for part in token.split('.')):
            data_type = get_most_specific_type(data_type, 'float')
        elif token.startswith("'") and token.endswith("'") and len(token) == 3:
            data_type = get_most_specific_type(data_type, 'char')
        else:
            var_entry = symbol_table.get(token)
            if var_entry:
                data_type = get_most_specific_type(data_type, var_entry.data_type)
            else:
                print(f"Error: Variable '{token}' used without declaration.")
                return None
    return data_type

def analyze_while_loop(expression):
    # Separate the loop condition and the loop body
    loop_parts = expression.strip().split("{", 1)
    loop_condition = loop_parts[0].strip()
    loop_body = loop_parts[1].strip("}").strip()

    # Analyze the loop condition
    if not analyze_expression(loop_condition):
        return False

    # Analyze the loop body
    lines = loop_body.split(";")
    for line in lines:
        line = line.strip()
        if line:
            if not analyze_expression(line + ";"):
                return False

    return True

def analyze_for_loop(expression):
    # Separate the initialization, condition, and increment parts of the loop
    loop_parts = expression.strip().split("(", 1)[1].split(")", 1)[0].split(";")
    loop_init = loop_parts[0].strip()
    loop_condition = loop_parts[1].strip()
    loop_increment = loop_parts[2].strip()

    # Analyze the loop initialization
    if loop_init:
        if not analyze_expression(loop_init + ";"):
            return False

    # Analyze the loop condition
    if not analyze_expression(loop_condition):
        return False

    # Analiza el incremento del for
    if loop_increment:
        if not analyze_expression(loop_increment + ";"):
            return False

    # Analiza el cuerpo del for
    loop_body = expression.split("{", 1)[1].strip("}").strip()
    lines = loop_body.split(";")
    for line in lines:
        line = line.strip()
        if line:
            if not analyze_expression(line + ";"):
                return False

    return True


#for_loop_expression = "for(i=1;i<=10;++i){ if(i==3) continue; if(i==7) break; }"

# while_loop_expression = "while(i > 3){ cout << i << endl; i++; }"

# Example expression to analyze
expression = "for(i=1;i<=10;++i){ if(i==3) continue; if(i==7) break; }"
if analyze_for_loop(expression):
    print("Esto es un for loop")
elif analyze_while_loop(expression):
    print("Esto es un while loop")
elif analyze_expression(expression):
    print("Esto es una asignación o una declaración")
else:
    print("Expression failed semantic analysis.")
