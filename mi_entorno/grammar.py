grammar = """
start: statement*

statement: variable_declaration
         | while_declaration
         | function_declaration
         | if_condition
         | void_declaration

variable_declaration: "var" CNAME "=" INT

function_declaration: "func" CNAME "(" ")" "{" variable_declaration* "}"
if_condition: "if" "(" logical_expression ")" "{" variable_declaration* "}" else_block?
void_declaration: "void" "main" "(" ")" "{" variable_declaration* "}"
while_declaration: "while" "(" TRUE_OR_FALSE ")" "{" variable_declaration* "}"

TRUE_OR_FALSE: "true" | "false"
else_block: "else" "{" variable_declaration* "}"
logical_expression: CNAME OPERATOR INT

OPERATOR: ">" | "<" | "==" | "<=" | ">=" | "!="

%import common.CNAME
%import common.INT
%import common.WS
%ignore WS
"""
