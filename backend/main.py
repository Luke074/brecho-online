import shutil
import sqlite3
import os
import uvicorn
from typing import Any, List

from interface.pessoa import PessoaCreate
from interface.produto import ProdutoCreate  # Corrected import path
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

os.makedirs('/images', exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

os.makedirs('db', exist_ok=True)
db_path = os.path.join("db", "brecho_db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def resposta_padrao(sucesso: bool, mensagem: str, data: Any = None):
    return {
        "sucesso": sucesso,
        "mensagem": mensagem,
        "data": data
    }


@app.get("/")
async def root():
    create_structure_database()
    # connection.execute('Select * from produtos')
    # connection.commit()
    # connection.close()
    return {"message": "Bem vindo ao Brecho Online!"}

def create_structure_database():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100),
            email VARCHAR(100),
            senha VARCHAR(100),
            celular VARCHAR(20),
            endereco VARCHAR(255),
            documento VARCHAR(20)
        )
    ''')
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS doacoes (
            id_doacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pessoa INTEGER REFERENCES pessoas(id_pessoa),
            nome VARCHAR(100),
            email VARCHAR(100),
            celular VARCHAR(20),
            endereco VARCHAR(255)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100),
            descricao TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doacao INTEGER REFERENCES doacoes(id_doacao),
            id_categoria INTEGER REFERENCES categorias(id_categoria),
            imagem VARCHAR(255),
            descricao VARCHAR(255),
            marca VARCHAR(100),
            tamanho VARCHAR(50),
            preco DECIMAL(10.2)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estoque (
            id_estoque INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER REFERENCES produtos(id_produto),
            quantidade INTEGER,
            secao VARCHAR(50),
            prateleira VARCHAR(50),
            data_ultima_atualizacao DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venda (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pessoa INTEGER REFERENCES pessoas(id_pessoa),
            data_venda DATE,
            valor_total DECIMAL(10.2)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto_venda (
            id_produto_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER REFERENCES produtos(id_produto),
            id_venda INTEGER REFERENCES venda(id_venda),
            valor_venda DECIMAL(10.2),
            UNIQUE(id_produto, id_venda)
        )
    ''')
    
    connection.commit()
    connection.close()
    
    

@app.post("/login")
async def login(usuario: str, senha: str):
    # Aqui você pode implementar a lógica de autenticação
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM pessoas WHERE email = ? AND senha = ?
    ''', (usuario, senha))
    usuario = cursor.fetchone()
    connection.close()
    
    if not usuario:
        return resposta_padrao(False, "Usuário ou senha inválidos")

    # Por enquanto, vamos apenas retornar uma mensagem de sucesso
    return resposta_padrao(True, "Login realizado com sucesso", {
        "id_pessoa": usuario["id_pessoa"],
        "nome": usuario["nome"],
        "email": usuario["email"]
    })
    
@app.post("/pessoas")
async def adicionar_pessoa(pessoa: PessoaCreate):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Verifica se já tem o email ou documento no banco
    cursor.execute('''
        SELECT * FROM pessoas WHERE email = ? OR documento = ?
    ''', (pessoa.email, pessoa.documento))
    existente = cursor.fetchone()

    if existente:
        connection.close()
        return resposta_padrao(False, "Já existe uma pessoa com este e-mail ou documento.")

    # Insere nova pessoa
    cursor.execute('''
        INSERT INTO pessoas (nome, email, celular, endereco, documento, senha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        pessoa.nome,
        pessoa.email,
        pessoa.celular,
        pessoa.endereco,
        pessoa.documento,
        pessoa.senha
    ))
    connection.commit()
    pessoa_id = cursor.lastrowid
    connection.close()

    return resposta_padrao(True, "Pessoa cadastrada com sucesso", {
        "id_pessoa": pessoa_id,
        "nome": pessoa.nome,
        "email": pessoa.email
    })
    
@app.get("/produtos")
async def listar_produtos():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT p.id_produto, p.id_categoria, p.imagem, p.descricao, p.marca, p.tamanho, p.preco,
                d.nome AS nome_doacao, c.nome AS categoria
            FROM produtos AS p
            LEFT JOIN doacoes AS d ON p.id_doacao = d.id_doacao
            INNER JOIN categorias AS c ON p.id_categoria = c.id_categoria
        ''')
        produtos = cursor.fetchall()
        connection.close()

        produtos_dict = [dict(p) for p in produtos]
        return resposta_padrao(True, "Produtos encontrados com sucesso.", produtos_dict)
    except sqlite3.Error as e:
        return resposta_padrao(False, "Erro ao listar produtos: " + str(e))

@app.get("/categorias")
async def listar_categorias():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categorias')
        categorias = cursor.fetchall()
        connection.close()

        categorias_dict = [dict(cat) for cat in categorias]
        return resposta_padrao(True, "Categorias encontradas com sucesso.", categorias_dict)
    except sqlite3.Error as e:
        return resposta_padrao(False, "Erro ao listar categorias: " + str(e))

@app.post("/produtos")
async def adicionar_produto(
    id_doacao: int = Form(...),
    id_categoria: int = Form(...),
    descricao: str = Form(...),
    marca: str = Form(...),
    tamanho: str = Form(...),
    preco: float = Form(...),
    imagem: UploadFile = File(...)
):
    try:
        imagem_filename = imagem.filename
        imagem_path = os.path.join("images", imagem_filename)
        with open(imagem_path, "wb") as buffer:
            shutil.copyfileobj(imagem.file, buffer)

        # Adjust the path to include "backend/images/..."
        imagem_db_path = os.path.join("backend", imagem_path)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO produtos (id_doacao, id_categoria, imagem, descricao, marca, tamanho, preco)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_doacao, id_categoria, imagem_db_path, descricao, marca, tamanho, preco))
        connection.commit()
        produto_id = cursor.lastrowid
        connection.close()

        return resposta_padrao(True, "Produto cadastrado com sucesso", {
            "id_produto": produto_id,
            "imagem": imagem_filename
        })
    except sqlite3.Error as e:
        return resposta_padrao(False, "Erro ao adicionar produto: " + str(e))
    except Exception as ex:
        return resposta_padrao(False, "Erro inesperado: " + str(ex))
