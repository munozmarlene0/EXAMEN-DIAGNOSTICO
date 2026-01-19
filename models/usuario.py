#la carpeta MODELS ME AYUDA A DEFINAR ESTRUCTURA DE LA TABLA DE LABASE DE DATOS

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String(20), nullable=False)
    direccion = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True, index=True)
    contrasena = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
