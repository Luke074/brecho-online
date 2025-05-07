from pydantic import BaseModel
from typing import Optional

class VendaCreate(BaseModel):
    id_pessoa: int
    data_venda: Optional[str]  # "YYYY-MM-DD"
    valor_total: float
