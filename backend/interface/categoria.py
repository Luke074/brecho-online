
from pydantic import BaseModel
from typing import Optional

class CategoriaCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
