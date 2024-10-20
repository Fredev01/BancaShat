from flask import Flask, jsonify, redirect, render_template, request, url_for
import pymysql
from features import settings
from features import db
from features.customer.model import Cliente

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta/para/registrar', methods=['POST'])
def registrar_cliente():
    try:
        data = request.get_json()
        
        # Imprime los datos recibidos
        print(f'Datos recibidos: {data}')

        nuevo_cliente = Cliente(
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            genero=data['genero'],
            correo=data['correo'],
            telefono=data['telefono'],
            numero_tarjeta=data['numero_tarjeta'],
            fecha_expiracion=data['fecha_expiracion'],
            cvv=data['cvv']
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

        print('Cliente registrado con éxito.')
        return jsonify({'mensaje': 'Cliente registrado con éxito'}), 201
    except Exception as e:
        print(f'Error al registrar cliente: {e}')
        return jsonify({'error': str(e)}), 400

def consultar_clientes():
    """Función para consultar todos los clientes en la base de datos."""
    return Cliente.query.all()   

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    """Función para agregar y consultar clientes. Los datos bancarios estan guardandose como texto XD"""
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        genero = request.form['genero']
        correo = request.form['correo']
        telefono = request.form['telefono']
        numero_tarjeta = request.form['numero_tarjeta']  
        fecha_expiracion = request.form['fecha_expiracion']  
        cvv = request.form['cvv']  

        # Llamar a la función para agregar el cliente
        registrar_cliente(nombre, apellidos, genero, correo, telefono, numero_tarjeta, fecha_expiracion, cvv)

        # Redirigir a la misma página para mostrar el nuevo cliente
        return redirect(url_for('clientes'))

    # Consultar todos los clientes
    clientes = consultar_clientes()
    return render_template('clientes.html', clientes=clientes)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000)
