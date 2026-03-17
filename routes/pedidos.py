import logging
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import PedidosCreate
from psycopg.rows import dict_row
from psycopg import errors
from utils import get_current_admin, get_current_user

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/ver_pedidos_Admin")
async def ver_pedidos_Admin(admin: dict = Depends(get_current_admin), db = Depends(get_db)):

    

    try:
        async with db.cursor(row_factory=dict_row) as cur:
            sql="""
            Select usuarios.nombre as usuario, videojuegos.titulo as titulo, sum(pedidos.cantidad) as cantidad from pedidos
            join usuarios on usuarios.id = pedidos.who
            join videojuegos on videojuegos.id = pedidos.item
            group by usuarios.nombre, videojuegos.titulo
            """
            await cur.execute(sql)
            filas = await cur.fetchall()

            if not filas:
                raise HTTPException(status_code=404, detail="No hay pedidos actualmente")
            return{"Pedidos":filas}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error al ver los pedidos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.post("/Agregar_pedido")
async def Agregar_pedido(pedido: PedidosCreate, usuario_info: dict = Depends(get_current_user), db = Depends(get_db)):
    
    try:
        async with db.transaction():
            
            async with db.cursor(row_factory=dict_row) as cur:
                
                sql_update = """
                UPDATE videojuegos
                SET stock = stock - %s
                WHERE id = %s AND stock >= %s
                """
                await cur.execute(sql_update, (pedido.cantidad, pedido.item, pedido.cantidad))

                if cur.rowcount == 0:
                    raise HTTPException(status_code=400, detail="Stock insuficiente o juego no existe")
                

                sql="""
                select precio
                from videojuegos
                where id = %s
                """

                await cur.execute(sql, (pedido.item,))

                precio = await cur.fetchone()

                sql="""
                Update usuarios
                set fondos = fondos - %s*%s
                where id = %s and fondos >= %s*%s
                """

                await cur.execute(sql, (precio['precio'], pedido.cantidad, usuario_info["ID"], precio['precio'], pedido.cantidad))
                
                if cur.rowcount == 0:
                    raise HTTPException(status_code=400, detail="El usuario no existe o no tiene fondos")
                sql_insert = """
                INSERT INTO pedidos (who, item, cantidad)
                VALUES (%s, %s, %s)
                """
                await cur.execute(sql_insert, (usuario_info["ID"], pedido.item, pedido.cantidad))
                
                return {"mensaje": "Pedido creado con éxito y stock actualizado"}

    except HTTPException as e:
        raise e
    except errors.ForeignKeyViolation:
        raise HTTPException(status_code=400, detail="El usuario o el videojuego no existen")

    except Exception as e:
        logging.error(f"Error crítico en la transacción: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    



@router.get("/ver_pedidos_User")
async def ver_pedidos_User(user_info: dict = Depends(get_current_user), db = Depends(get_db)):

    

    try:
        async with db.cursor(row_factory=dict_row) as cur:
            sql="""
            Select videojuegos.titulo as titulo, sum(pedidos.cantidad) as cantidad
            from pedidos
            join videojuegos on videojuegos.id = pedidos.item 
            where pedidos.who = %s
            group by videojuegos.titulo
            """
            await cur.execute(sql, (user_info["ID"], ))
            filas = await cur.fetchall()

            if not filas:
                raise HTTPException(status_code=404, detail="No hay pedidos actualmente")
            return{"Pedidos":filas}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error al ver los pedidos: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
