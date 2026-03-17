import logging
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import UsuarioBase, Login  # Importamos el esquema de entrada
from psycopg.rows import dict_row
from utils import obtener_hash_password, crear_token, verificar_password
from psycopg import errors
from fastapi.security import OAuth2PasswordRequestForm

# Definimos el router
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")  # CAMBIO: Usamos 'router' en lugar de 'app'
async def ver_usuarios(db = Depends(get_db)):
    try:
        async with db.cursor(row_factory=dict_row) as cur:
            await cur.execute("SELECT nombre, id FROM usuarios")
            filas = await cur.fetchall()
            if not filas:
                raise HTTPException(status_code=404, detail="No hay usuarios")
            return {"usuarios": filas}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error al ver usuarios: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.post("/crear") # CAMBIO: Usamos 'router'
async def crear_usuario(usuario: UsuarioBase, db = Depends(get_db)):
    try:
        async with db.transaction():
            async with db.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    "INSERT INTO usuarios (nombre, email, hashed_password) VALUES (%s, %s, %s)", 
                    (usuario.nombre, usuario.email, obtener_hash_password(usuario.password))
                )


            
        return {"mensaje": "Usuario creado satisfactoriamente"}
    except errors.UniqueViolation:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    except Exception as e:
        logging.error(f"Error al crear usuario {usuario.email}: {e}")
        raise HTTPException(status_code=500, detail="No se pudo crear el usuario")
    

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    try:
        
        async with db.cursor(row_factory=dict_row) as cur:
            sql="""
            Select usuarios.hashed_password as password, usuarios.administrador
            from usuarios
            where %s = usuarios.nombre
            """

            await cur.execute(sql, (form_data.username,))

            Info = await cur.fetchone()

            if Info == None:
                raise HTTPException(status_code=404, detail="El usuario o la contraseña son erronios")

            if not verificar_password(form_data.password, Info["password"]):
                raise HTTPException(status_code=401, detail="El usuario o la contraseña son erronios")
                
            sql="""
            select usuarios.administrador, usuarios.id
            from usuarios
            where %s = usuarios.nombre
            """

            await cur.execute(sql, (form_data.username,))

            Info = await cur.fetchone()
            
            token = crear_token({"sub": form_data.username, "admin": Info["administrador"], "ID": Info["id"]})

            return {"access_token":token, "token_type": "bearer"}
            
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logging.error(f"Error al conectar con el servidor{e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

