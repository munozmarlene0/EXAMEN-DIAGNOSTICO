from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import hash_password, verify_password, verify_api_key
from schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- REGISTRARSE ---
@router.post("/registro", response_model=UsuarioResponse)
def registrar(usuario: UsuarioCreate, api_key: str = Header(None), db: Session = Depends(get_db)):
    """POST /auth/registro - Crear una cuenta nueva"""
    
    if not verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="API KEY inválida")
    
    # Ver si ya existe
    existe = db.query(Usuario).filter(
        (Usuario.email == usuario.email) | (Usuario.nombre_usuario == usuario.nombre_usuario)
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="El email o usuario ya están registrados")
    
    # Crear el usuario
    nuevo = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        edad=usuario.edad,
        sexo=usuario.sexo,
        direccion=usuario.direccion,
        telefono=usuario.telefono,
        email=usuario.email,
        nombre_usuario=usuario.nombre_usuario,
        contrasena=hash_password(usuario.contrasena)  # Encriptar
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# --- LOGIN ---
@router.post("/login")
def login(credenciales: UsuarioLogin, api_key: str = Header(None), db: Session = Depends(get_db)):
    """POST /auth/login - Iniciar sesión"""
    
    if not verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="API KEY inválida")
    
    # Buscar el usuario
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == credenciales.nombre_usuario).first()
    
    # Validar que exista y la contraseña sea correcta
    if not usuario or not verify_password(credenciales.contrasena, usuario.contrasena):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    # Login exitoso
    return {
        "ok": True,
        "usuario_id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "nombre": f"{usuario.nombre} {usuario.apellido}"
    }




