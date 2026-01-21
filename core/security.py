#este nos sirve para manejar las funciones para el control de la seguridad 
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

# API KEY desde variable de entorno
API_KEY = os.getenv("API_KEY", "default_key")

def hash_password(password: str) -> str:
    """Encripta una contraseña con bcrypt (límite 72 bytes)"""
    # Convertir a bytes y truncar si es necesario
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    # Convertir a bytes y truncar si es necesario
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Verificar
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

def verify_api_key(api_key: str) -> bool:
    """Verifica que la API KEY sea válida"""
    return api_key == API_KEY

