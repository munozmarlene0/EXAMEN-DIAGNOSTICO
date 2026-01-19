#este nos sirve para manejar las funciones para el control de la seguridad 
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# API KEY desde variable de entorno
API_KEY = os.getenv("API_KEY", "default_key")

# Contexto para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Encripta una contraseña con bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def verify_api_key(api_key: str) -> bool:
    """Verifica que la API KEY sea válida"""
    return api_key == API_KEY
