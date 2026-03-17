import logging
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from psycopg.rows import dict_row
from fastapi.security import OAuth2PasswordBearer
from utils import ALGORITHM, SECRET_KEY, get_current_admin, get_current_user
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


router = APIRouter(prefix="/registro", tags=["registro"])

@router.get("/registro_fondos_nuevos")
async def ver_nuevos_fondos(
    Maximo: int, 
    db = Depends(get_db),
    admin: dict = Depends(get_current_admin)
    
    

    
):
    try:
        # 1. Validamos el token (opcional si solo quieres saber quién es)
        
        
        
        
        async with db.cursor(row_factory=dict_row) as cur:
            sql="""
            Select historial_fondos.usuario as Usuario_id, usuarios.nombre as Usuario, historial_fondos.cantidad as Cantidad, historial_fondos.fecha as Fecha, historial_fondos.Realizador as Realizador
            from historial_fondos
            join usuarios on usuarios.id = historial_fondos.usuario
            limit %s
            """

            await cur.execute(sql, (Maximo,))

            filas = await cur.fetchall()


            return{"mensaje":f"{filas}"}
        
    except HTTPException as e:
        raise e
        
    except Exception as e:
        logging.error(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
    



