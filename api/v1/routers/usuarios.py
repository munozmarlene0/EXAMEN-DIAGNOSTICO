from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verify_api_key
from schemas.usuario import UsuarioResponse, UsuarioUpdate
from models.usuario import Usuario
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Verificar que tengan la API Key
def verificar_api_key(api_key: str = Header(None)):
    if not verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="API KEY inválida")

# --- TRAER TODOS ---
@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db), api_key: str = Header(None)):
    """GET /usuarios/ - Trae todos los usuarios"""
    verificar_api_key(api_key)
    usuarios = db.query(Usuario).all()
    return usuarios

# --- TRAER UNO POR ID ---
@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db), api_key: str = Header(None)):
    """GET /usuarios/1 - Trae un usuario por su ID"""
    verificar_api_key(api_key)
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# --- MODIFICAR ---
@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, 
                       db: Session = Depends(get_db), api_key: str = Header(None)):
    """PUT /usuarios/1 - Actualiza los datos de un usuario"""
    verificar_api_key(api_key)
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar solo lo que enviaron
    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

# --- ELIMINAR ---
@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), api_key: str = Header(None)):
    """DELETE /usuarios/1 - Elimina un usuario"""
    verificar_api_key(api_key)
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"ok": True, "mensaje": f"Usuario {usuario_id} eliminado"}
