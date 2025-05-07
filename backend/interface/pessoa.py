from pydantic import BaseModel
from typing import Optional

class PessoaCreate(BaseModel):
    nome: str
    email: str
    celular: str
    endereco: str
    documento: str
    senha: str