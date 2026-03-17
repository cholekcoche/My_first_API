import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()


# Configuración de Logs
logging.basicConfig(
    filename="errores_db.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DATABASE_URL = f"host={os.getenv('DB_HOST')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')}"

# Creamos el pool global
pool = AsyncConnectionPool(conninfo=DATABASE_URL, open=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()

async def get_db():
    async with pool.connection() as conn:
        yield conn