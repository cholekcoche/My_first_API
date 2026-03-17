import logging
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import AgregarFondosBase, A_F_Admin
from psycopg.rows import dict_row
from psycopg import errors
from utils import get_current_admin, get_current_user


router = APIRouter(prefix="/fondos", tags=["fondos"])

@router.put("/Agregar_fondos_Admin")
async def Agregar_fondos_Admin(Fondos: A_F_Admin, admin: dict = Depends(get_current_admin), user_info: dict = Depends(get_current_user),db = Depends(get_db)):
    try:
        if Fondos.cantidad > 500 or Fondos.cantidad % 10 != 0:
            raise HTTPException(status_code=400, detail="Solo se admiten múltiplos de 10, entre 10 y 500.")

        async with db.transaction():
            async with db.cursor(row_factory=dict_row) as cur:


                
                sql="""
                Update Usuarios
                set fondos = fondos+%s
                where id = %s
                """

                await cur.execute(sql, (Fondos.cantidad, Fondos.id_usuario))

                if cur.rowcount == 0:
                    raise HTTPException(status_code=400, detail="No se ha encontrado el usuario")
                
                sql="""
                insert into historial_fondos (usuario, cantidad, Realizador)
                values (%s, %s, %s)
                """

                await cur.execute(sql, (Fondos.id_usuario, Fondos.cantidad, user_info["ID"]))

        return{"mensaje":"Fondos añadidos correctamente"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logging.error(f"Error al añadir fondos al usuario {Fondos.id_usuario} : {e}")
        raise HTTPException(status_code=500, detail=("Error interno del servidor"))
    


@router.get("/Consulta_saldo_Admin")
async def  Consulta_saldo_Admin(usuario: int, admin: dict = Depends(get_current_admin), db = Depends(get_db)):
    try:
        async with db.transaction():
            async with db.cursor(row_factory=dict_row) as cur:

                sql="""
                Select fondos
                from usuarios
                where usuarios.id = %s
                """

                await cur.execute(sql, (usuario,))

                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="No encontrado")

                Info = await cur.fetchone()

                return{"mensaje":f"Tiene un saldo de {Info['fondos']}"}
            
    except HTTPException as e:
        raise e
    

    except Exception as e:
        logging.error(f"Error al consultar el saldo del usuario {usuario}: {e}")
        raise HTTPException(status_code=500, detail="Se ha producido un error")


@router.get("/Consulta_saldo_User")
async def  Consulta_saldo_User(user_info: dict = Depends(get_current_user), db = Depends(get_db)):
    try:
        async with db.transaction():
            async with db.cursor(row_factory=dict_row) as cur:

                sql="""
                Select fondos
                from usuarios
                where usuarios.id = %s
                """

                await cur.execute(sql, (user_info["ID"],))

                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="No encontrado")

                Info = await cur.fetchone()

                return{"mensaje":f"Tienes un saldo de {Info['fondos']}"}
            
    except HTTPException as e:
        raise e
    

    except Exception as e:
        logging.error(f"Error al consultar el saldo del usuario {user_info["ID"]}: {e}")
        raise HTTPException(status_code=500, detail="Se ha producido un error")

@router.put("/Agregar_fondos_User")
async def Agregar_fondos_User(Fondos: AgregarFondosBase, user_info: dict = Depends(get_current_user),db = Depends(get_db)):
    try:
        if Fondos.cantidad > 500 or Fondos.cantidad % 10 != 0:
            raise HTTPException(status_code=400, detail="Solo se admiten múltiplos de 10, entre 10 y 500.")

        async with db.transaction():
            async with db.cursor(row_factory=dict_row) as cur:


                
                sql="""
                Update Usuarios
                set fondos = fondos+%s
                where id = %s
                """

                await cur.execute(sql, (Fondos.cantidad, user_info["ID"]))

                if cur.rowcount == 0:
                    raise HTTPException(status_code=400, detail="No se ha encontrado el usuario")
                
                sql="""
                insert into historial_fondos (usuario, cantidad, Realizador)
                values (%s, %s, %s)
                """

                await cur.execute(sql, (user_info["ID"], Fondos.cantidad, user_info["ID"]))

        return{"mensaje":"Fondos añadidos correctamente"}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logging.error(f"Error al añadir fondos al usuario {user_info["ID"]} : {e}")
        raise HTTPException(status_code=500, detail=("Error interno del servidor"))
    
