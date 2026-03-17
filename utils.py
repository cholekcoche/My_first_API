from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

raiz_del_proyecto = Path(__file__).resolve().parent.parent
ruta_env = raiz_del_proyecto / ".env"
load_dotenv(dotenv_path=ruta_env)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")



# Inicializamos el hasher (usa valores seguros por defecto)
ph = PasswordHasher()

def obtener_hash_password(password: str) -> str:
    """Genera un hash Argon2id (el estándar más alto actual)."""
    return ph.hash(password)

def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    """Verifica la contraseña y maneja errores de forma segura."""
    try:
        return ph.verify(password_hasheado, password_plano)
    except VerifyMismatchError:
        return False
    except Exception:
        # Cualquier otro error (hash corrupto, etc.) se trata como fallo
        return False

# Prueba
nuevo_hash = obtener_hash_password("1234")
print(f"Hash profesional (Argon2): {nuevo_hash}")






def crear_token(data: dict):
    expira = datetime.utcnow() + timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(token: str):
    # Esta función la usaremos después para proteger rutas
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])




def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decodificas el token aquí
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload # Devuelve el dict con 'sub' y 'admin'
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
def get_current_admin(current_user: dict = Depends(get_current_user)):
    if not current_user.get("admin"):
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user