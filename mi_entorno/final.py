from flask import Flask, render_template, request
from lark import Lark
from grammar import grammar
from MyTransformer import MyTransformer

app = Flask(__name__)

mensajeERROR = ""
bandera = False
texto = ""
output = ""  # Asumiendo que quieres mostrar algún resultado del procesamiento

@app.route('/')
def pagina():
    return render_template('formulario.html', bandera="", texto=texto, mensajeERROR=mensajeERROR, output=output)

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    global mensajeERROR, bandera, texto, output
    transformer = MyTransformer()
    transformer.variables = {}
    transformer.statements = []
    transformer.mensaje_if = ""
    transformer.mensaje_funcion = ""
    transformer.mensaje_void = ""
    transformer.mensaje_while = ""
    transformer.mensaje_variable = ""
    tokens = []

    texto = request.form.get('texto')
    #print(texto)
    parser = Lark(grammar, start='start', parser='earley')
    output = ""  # Reinicia el output cada vez que se procesa un formulario

    try:
        tree = parser.parse(texto)
        #print(tree.pretty())
        
        transformer.transform(tree)
        
        bandera = True
        mensajeERROR = ""
        output = tree.pretty()  # Asumiendo que quieres mostrar la estructura del árbol
    except Exception as e:
        print("Error en el procesamiento:", e)
        bandera = False
        mensajeERROR = str(e).split('\n')[0]

    print(transformer.mensaje_if)
    print(transformer.mensaje_funcion)
    print(transformer.mensaje_void)
    print(transformer.mensaje_while)

    msj_if = transformer.mensaje_if
    msj_fun = transformer.mensaje_funcion
    msj_void = transformer.mensaje_void
    msj_while = transformer.mensaje_while
    msj_variable = transformer.mensaje_variable

    try:
        for token in parser.lex(texto):
            tokens.append(f"Type: {token.type}, Value: {token}")
    except Exception as e:
        print(f"Error tokenizing input: {e}")

    print(transformer.mensaje_variable)

    return render_template('formulario.html', bandera=bandera, texto=texto, mensajeERROR=mensajeERROR, tree=output, msj_if=msj_if, msj_fun=msj_fun, msj_void=msj_void, msj_while=msj_while, tokens=tokens, msj_variable=msj_variable)

if __name__ == '__main__':
    app.run(debug=True)

