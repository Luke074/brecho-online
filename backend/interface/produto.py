
from pydantic import BaseModel
from typing import Optional

class ProdutoCreate(BaseModel):
    id_doacao: Optional[int]
    id_categoria: Optional[int]
    descricao: str
    marca: Optional[str]
    tamanho: Optional[str]
    preco: float