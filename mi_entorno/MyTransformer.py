from lark import Transformer, Tree
import re
import ast

class MyTransformer(Transformer):
    def __init__(self):
        self.variables = {}
        self.statements = []
        self.tokens = []
        self.mensaje_if = ""
        self.mensaje_funcion = ""
        self.mensaje_void = ""
        self.mensaje_while = ""
        self.mensaje_variable = ""

    def variable_declaration(self, items):
        var_name = items[0].value
        var_value = int(items[1].value)
        self.variables[var_name] = var_value
        #print(f"Variable '{var_name}' declarada con valor {var_value}")
        self.mensaje_variable += f"Variable '{var_name}' declarada con valor {var_value}\n"
        return (var_name, var_value)


    def function_declaration(self, items):
        func_name = items[0].value
        variable_declarations = items[1:]

        #print(f"Declaración de función '{func_name}' con variables:")
        self.mensaje_funcion = f"Declaración de función '{func_name}' con variables:",
        for var_declaration in variable_declarations:
            if var_declaration:
                var_name, var_value = var_declaration
                #print(f"- Variable '{var_name}' con valor {var_value}")
                self.statements.append((var_name, var_value))
                self.mensaje_funcion += var_name, "=", var_value

    def if_condition(self, items):
        logical_expression_str = items[0]     
        
        if self.evaluate_logical_expression(logical_expression_str):
            self.statements.append((items[1]))
            print("ssss")
            self.mensaje_if = "La condición if es verdadera.", (items[1])
        else:
            print("La condición if es falsa.")
            temp = items
            print(temp)

            self.mensaje_if += "La condición if es falsa."

    def evaluate_logical_expression(self, logical_expression_str):
        parts = logical_expression_str.split()
        if len(parts) != 3:
            #print(f"Error: Formato de expresión lógica inválido '{logical_expression_str}'.")
            return False

        var_name, operator, value_str = parts
        var_value = self.variables.get(var_name)

        if var_value is None:
            #print(f"Error: La variable '{var_name}' no está definida.")
            self.mensaje_if += f"Error: La variable '{var_name}' no está definida."
            return False

        try:
            value = int(value_str)
        except ValueError:
            #print(f"Error: El valor '{value_str}' no es un entero válido.")
            return False

        if operator == "==":
            return var_value == value
        elif operator == "!=":
            return var_value != value
        elif operator == ">":
            return var_value > value
        elif operator == "<":
            return var_value < value
        elif operator == ">=":
            return var_value >= value
        elif operator == "<=":
            return var_value <= value
        else:
            #print(f"Error: Operador '{operator}' no reconocido.")
            return False

    def void_declaration(self, items):
        variable_declarations = items[0:]
        #print(f"Declaración void con variables: {items}")
        self.mensaje_void = f"Declaración de main con variables:",
        for var_declaration in variable_declarations:
            if var_declaration:
                var_name, var_value = var_declaration
                #print(f"- Variable '{var_name}' con valor {var_value}")
                self.statements.append((var_name, var_value))
                self.mensaje_void += var_name, "=", var_value

    def TRUE_OR_FALSE(self, items):
        #print(f"Items en condition: {items}") 
        condition_value = items[0]
        #print(f"Condición evaluada: {condition_value}")
        return condition_value

    def while_declaration(self, items):
        condition = items[0]
        body_items  = items[1:]

        if condition == 't':
            self.mensaje_while = "Declaracion del while verdadera con variable"
            for _ in range(100):
                for statement in body_items:
                    self.mensaje_while += str(statement)
                    #print(statement)
        else:
            #print("La condición del bucle while es falsa; no se ejecuta el cuerpo.")
            self.mensaje_while = "La condición del bucle while es falsa; no se ejecuta el cuerpo."
            

    def else_block(self, items):
        self.mensaje_if += f"bloque else con variables: {items}"
        return f"bloque else con variables: {items}"

    def logical_expression(self, items):
        return f"{items[0]} {items[1]} {items[2]}"
