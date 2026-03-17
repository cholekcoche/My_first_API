from fastapi import FastAPI
from database import lifespan
from routes import usuarios, pedidos, fondos, registro # Suponiendo que hagas pedidos.py igual

app = FastAPI(title="Mi API Profesional", lifespan=lifespan)

# Incluimos las rutas de los diferentes módulos
app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(fondos.router)
app.include_router(registro.router)
# app.include_router(pedidos.router)

@app.get("/")
async def inicio():
    return {"mensaje": "API funcionando correctamente"}