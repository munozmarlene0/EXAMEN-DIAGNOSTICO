from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import auth, usuarios
from core.database import init_db

app = FastAPI(
    title="API Gestión de Usuarios",
    version="1.0"
)

# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Al iniciar, crea las tablas
@app.on_event("startup")
def startup():
    init_db()
    print(f"\n✓ Base de datos lista")
    print(f"✓ Servidor iniciado correctamente\n")

# Incluir routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")

# Endpoint raíz
@app.get("/")
def root():
    return {"mensaje": "API de usuarios - Usa /docs para ver los endpoints"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
