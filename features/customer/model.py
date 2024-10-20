from sqlalchemy import Column, Integer, Text, Boolean, String, Float, Enum, DateTime
from features import db


class Cliente(db.Model):
    __tablename__ = 'clientes'
    
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
        return f'<Cliente {self.nombre} {self.apellidos}>'

