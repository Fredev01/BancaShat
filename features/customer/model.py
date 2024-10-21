from sqlalchemy import Column, Integer, Text, Boolean, String, Float, Enum, DateTime, BLOB
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
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(100), nullable=False) 
    telefono = Column(String(15))  
    mensaje = Column(BLOB, nullable=False)

    def __repr__(self):
        return f'<Mensaje nombre={self.nombre} correo={self.correo} telefono={self.telefono} mensaje={self.mensaje}>'
