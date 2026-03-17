# My_first_API
# API de Gestión de Pedidos y Usuarios

Esta es una API profesional desarrollada con **FastAPI** que implementa un sistema de gestión de usuarios, manejo de saldos (fondos) y procesamiento de pedidos. Utiliza una arquitectura asíncrona y estándares de seguridad de alto nivel.

## Características Técnicas

* Framework:** FastAPI (Asíncrono).
* **Base de Datos:** PostgreSQL utilizando `psycopg_pool` para una gestión eficiente de conexiones. 
* **Seguridad:** * Hasheo de contraseñas con **Argon2id** (vía `argon2-cffi`).
    * Autenticación mediante **JWT (JSON Web Tokens)**. 
    * Protección de rutas con OAuth2 y validación de roles (User/Admin).
* **Validación:** Modelos de datos estrictos con **Pydantic**. 
* **Gestión de Ciclo de Vida:** Uso de `lifespan` para inicializar y cerrar el pool de conexiones de forma segura.

## Estructura del Proyecto

* `main.py`: Punto de entrada y configuración de rutas.
* `database.py`: Configuración del pool de conexiones a PostgreSQL.
* `schemas.py`: Definición de modelos Pydantic (Data Transfer Objects). 
* `utils.py`: Utilidades de seguridad, hashing y gestión de tokens.
* `routes/`: Módulos de rutas (usuarios, pedidos, fondos, registro).

## Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-proyecto.git](https://github.com/tu-usuario/tu-proyecto.git)
    cd tu-proyecto
    ```

2.  **Crea e inicia un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install fastapi uvicorn psycopg[pool] python-dotenv argon2-cffi python-jose[cryptography] python-multipart
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz con los siguientes campos:
    ```env
    DB_HOST=tu_host
    DB_NAME=tu_db
    DB_USER=tu_usuario
    DB_PASS=tu_password
    SECRET_KEY=tu_clave_secreta_super_segura
    ALGORITHM=HS256
    ```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
