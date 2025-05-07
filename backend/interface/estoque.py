from pydantic import BaseModel
from typing import Optional

class EstoqueCreate(BaseModel):
    id_produto: int
    quantidade: int
    secao: Optional[str] = None
    prateleira: Optional[str] = None
    data_ultima_atualizacao: Optional[str]  # Use formato ISO: "YYYY-MM-DD"
