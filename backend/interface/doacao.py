from pydantic import BaseModel
from typing import Optional

class DoacaoCreate(BaseModel):
    id_pessoa: int
    nome: str
    email: str
    celular: str
    endereco: str
