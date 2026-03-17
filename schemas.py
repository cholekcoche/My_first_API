from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    id: int

class AgregarFondosBase(BaseModel):
    cantidad: int = Field(gt=9)

    
class A_F_Admin(AgregarFondosBase):
    id_usuario: int






class PedidosCreate(BaseModel):
    
    item: int = Field(description="Identificador del titulo deseado")
    cantidad: int = Field(gt=0, description="Cantidad deseada del producto")

class PedidosResponse(PedidosCreate):
    id: int


class Login(BaseModel):
    user: str
    password: str
