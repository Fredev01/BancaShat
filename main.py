from flask import Flask, jsonify, redirect, render_template, request, url_for
import pymysql
from features import settings
from features import db
from features.customer import Customer
from features.customer.model import  Mensaje
from utils import RSAEncrypt, AESEncrypt

pymysql.install_as_MySQLdb()

app = Flask(__name__)
rsa_encrypt = RSAEncrypt()
aes_encrypt = AESEncrypt()

app.config["SECRET_KEY"] = settings.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aviso-privacidad')
def aviso_privacidad():
    return render_template('aviso_privacidad.html')

def consultar_clientes() -> list[Customer]:
    """Función para consultar todos los clientes en la base de datos."""
    return Customer.query.all()

@app.post('/registrar-cliente')
def registrar_cliente():
    data = request.json
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    genero = data.get('genero')
    correo = data.get('correo')
    telefono = data.get('telefono')
    numero_tarjeta = data.get('numero_tarjeta')
    fecha_expiracion = data.get('fecha_expiracion')
    cvv = data.get('cvv')
    # TODO: Validar los datos

    # Encriptar los datos
    numero_tarjeta_encrypted = aes_encrypt.encrypt(numero_tarjeta)
    fecha_expiracion_encrypted = aes_encrypt.encrypt(fecha_expiracion)
    cvv_encrypted = aes_encrypt.encrypt(cvv)
    try:
        nuevo_cliente = Customer(
            nombre=nombre,
            apellidos=apellidos,
            genero=genero,
            correo=correo,
            telefono=telefono,
            numero_tarjeta=numero_tarjeta_encrypted,
            fecha_expiracion=fecha_expiracion_encrypted,
            cvv=cvv_encrypted
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error al registrar el cliente'}), 500

    return jsonify({'message': 'Cliente registrado exitosamente'}), 201


@app.get('/clientes')
def clientes():
    customers = consultar_clientes()
    customers_decrypted = []
    for customer in customers:
        # Desencriptar los datos
        numero_tarjeta_decrypted = aes_encrypt.decrypt(customer.numero_tarjeta.encode())
        fecha_expiracion_decrypted = aes_encrypt.decrypt(customer.fecha_expiracion.encode())
        cvv_decrypted = aes_encrypt.decrypt(customer.cvv.encode())
        customer.numero_tarjeta = numero_tarjeta_decrypted
        customer.fecha_expiracion = fecha_expiracion_decrypted
        customer.cvv = cvv_decrypted
        customers_decrypted.append(customer)
    return render_template('clientes.html', clientes=customers_decrypted)

@app.post('/registrar-mensaje')
def registrar_mensaje():
    data = request.json
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    mensaje = data.get('mensaje')
    # TODO: Validar los datos

    mensaje_encrypted = rsa_encrypt.encrypt(mensaje)
    try:
        nuevo_mensaje = Mensaje(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            mensaje=mensaje_encrypted
        )
        db.session.add(nuevo_mensaje)
        db.session.commit()
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error al registrar el mensaje'}), 500

    return jsonify({'message': 'Mensaje registrado exitosamente'}), 201

@app.route('/mensajes')
def mostrar_mensajes():
    try:
        mensajes = Mensaje.query.all()
        for mensaje in mensajes:
            try:
                mensaje.mensaje = rsa_encrypt.decrypt(mensaje.mensaje)
            except Exception as decrypt_error:
                print(f'Error al desencriptar el mensaje ID {mensaje.id}: {decrypt_error}')
                mensaje.mensaje = f"Error al desencriptar el mensaje: {str(decrypt_error)}"  
        return render_template('mensajes.html', mensajes=mensajes)
    except Exception as e:
        print(f'Error al consultar mensajes: {e}')
        return jsonify({'error': str(e)}), 500

@app.route('/mensajes/form')
def mensajes_form():
    return render_template('formMensaje.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8000)
