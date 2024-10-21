from sqlalchemy import Column, Integer, Text, Boolean, String, Float
from features import db


class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.Enum('Masculino', 'Femenino', 'Otro'), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(15))
    numero_tarjeta = db.Column(db.String(50), nullable=False)  # Almacenar como texto
    fecha_expiracion = db.Column(db.String(7), nullable=False)  # MM/AA
    cvv = db.Column(db.String(4), nullable=False)  # Almacenar como texto
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellidos}>'

class Mensaje(db.Model):
    __tablename__ = 'mensajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)