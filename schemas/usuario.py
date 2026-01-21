from pydantic import BaseModel, EmailStr
from typing import Optional

# Modelo base con datos comunes
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    edad: int
    sexo: str
    direccion: str
    telefono: str
    email: EmailStr
    nombre_usuario: str

# Para crear usuario
class UsuarioCreate(UsuarioBase):
    contrasena: str

# Para actualizar 
class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    sexo: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None

# Respuesta (lo que devuelve la API)
class UsuarioResponse(UsuarioBase):
    id: int
    
    model_config = {"from_attributes": True}

# Login simple
class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str

