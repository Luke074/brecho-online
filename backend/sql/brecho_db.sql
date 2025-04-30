DROP DATABASE IF EXISTS brecho_db;
CREATE DATABASE brecho_db;
use brecho_db;

CREATE TABLE pessoas (
    id_pessoa SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    celular VARCHAR(20),
    endereco VARCHAR(255),
    documento VARCHAR(20)
);

CREATE TABLE doacoes (
    id_doacao SERIAL PRIMARY KEY,
    id_pessoa INTEGER REFERENCES pessoas(id_pessoa),
    nome VARCHAR(100),
    email VARCHAR(100),
    celular VARCHAR(20),
    endereco VARCHAR(255)
);

CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT
);

CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    id_doacao INTEGER REFERENCES doacoes(id_doacao),
    id_categoria INTEGER REFERENCES categorias(id_categoria),
    descricao VARCHAR(255),
    marca VARCHAR(100),
    tamanho VARCHAR(50),
    preco DECIMAL(10, 2)
);

CREATE TABLE estoque (
    id_estoque SERIAL PRIMARY KEY,
    id_produto INTEGER REFERENCES produtos(id_produto),
    quantidade INTEGER,
    secao VARCHAR(50),
    prateleira VARCHAR(50),
    data_ultima_atualizacao DATE
);

CREATE TABLE venda (
    id_venda SERIAL PRIMARY KEY,
    id_pessoa INTEGER REFERENCES pessoas(id_pessoa),
    data_venda DATE,
    valor_total DECIMAL(10, 2)
);

CREATE TABLE produto_venda (
    id_produto_venda SERIAL PRIMARY KEY,
    id_produto INTEGER REFERENCES produtos(id_produto),
    id_venda INTEGER REFERENCES venda(id_venda),
    valor_venda DECIMAL(10, 2),
    UNIQUE(id_produto, id_venda)
);

