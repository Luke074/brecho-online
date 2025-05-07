from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from typing import List

# Defini aqui o caminho do banco de dados
os.makedirs('db', exist_ok=True)
db_path = os.path.join("db", "brecho_db")

app = FastAPI()

# Pydantic model pra requisição de um novo produto
class ProdutoCreate(BaseModel):
    id_doacao: int
    id_categoria: int
    descricao: str
    marca: str
    tamanho: str
    preco: float

# Função que conecta ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Rota o GET para listar todos os produtos
@app.get("/produtos", response_model=List[dict])
async def listar_produtos():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT p.id_produto, p.descricao, p.marca, p.tamanho, p.preco,
               d.nome AS nome_doacao, c.nome AS categoria
        FROM produtos p
        JOIN doacoes d ON p.id_doacao = d.id_doacao
        JOIN categorias c ON p.id_categoria = c.id_categoria
    ''')
    produtos = cursor.fetchall()
    connection.close()
    
    return [dict(produto) for produto in produtos]

# Rota o POST para adicionar um novo produto
@app.post("/produtos")
async def adicionar_produto(produto: ProdutoCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Insere o novo produto
    cursor.execute('''
        INSERT INTO produtos (id_doacao, id_categoria, descricao, marca, tamanho, preco)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (produto.id_doacao, produto.id_categoria, produto.descricao, produto.marca, produto.tamanho, produto.preco))
    
    connection.commit()
    connection.close()
    
    return {"message": "Produto adicionado com sucesso!"}


"""
Pra rodar esse código é só instalar o fastapi, uvicorn e sqlite3 usando o pip install
"""
