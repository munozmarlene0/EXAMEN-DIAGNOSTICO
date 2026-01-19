#core es una carpeta que me sirve para configurar la conexion a mysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.usuario import Base
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de MySQL desde variables de entorno
db_password = os.getenv("DATABASE_PASSWORD", "")
DATABASE_URL = f"mysql+pymysql://root:{db_password}@localhost/usuarios_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency para obtener sesión de BD"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Crea las tablas en la BD"""
    Base.metadata.create_all(bind=engine)
