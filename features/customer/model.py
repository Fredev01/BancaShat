from sqlalchemy import Column, Integer, Text, Boolean, String, Float, Enum, DateTime
from features import db


class Customer(db.Model):

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(50), nullable=False)
    genero = Column(Enum('Masculino', 'Femenino', 'Otro'), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(15))
    numero_tarjeta = Column(String(255), nullable=False)  # Almacenar como texto
    fecha_expiracion = Column(String(100), nullable=False)  # MM/AA
    cvv = Column(String(100), nullable=False)  # Almacenar como texto
    fecha_registro = Column(DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Cliente nombre={self.nombre} apellidos={self.apellidos} genero={self.genero} correo={self.correo} telefono={self.telefono} numero_tarjeta={self.numero_tarjeta} fecha_expiracion={self.fecha_expiracion} cvv={self.cvv}>'

class Mensaje(db.Model):
    __tablename__ = 'mensajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)