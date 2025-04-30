TRUNCATE TABLE IF EXISTS produto_venda CASCADE;
TRUNCATE TABLE IF EXISTS venda CASCADE;
TRUNCATE TABLE IF EXISTS estoque CASCADE;
TRUNCATE TABLE IF EXISTS produtos CASCADE;
TRUNCATE TABLE IF EXISTS categorias CASCADE;
TRUNCATE TABLE IF EXISTS doacoes CASCADE;
TRUNCATE TABLE IF EXISTS pessoas CASCADE;

-- Inserindo pessoas (um deles com CNPJ)
INSERT INTO pessoas (nome, email, celular, endereco, documento) VALUES
('João Silva', 'joao@gmail.com', '11999990000', 'Rua A, 123', '12345678900'),  -- CPF
('Maria Oliveira', 'maria@gmail.com', '11988887777', 'Av. B, 456', '98765432100'),  -- CPF
('Instituto Luz', 'contato@institutoluz.org', '1133332222', 'Av. das ONGs, 1000', '12345678000199');  -- CNPJ

-- Inserindo doacoes
INSERT INTO doacoes (id_pessoa, nome, email, celular, endereco) VALUES
(1, 'João Silva', 'joao@gmail.com', '11999990000', 'Rua A, 123'),
(2, 'Maria Oliveira', 'maria@gmail.com', '11988887777', 'Av. B, 456'),
(3, 'Instituto Luz', 'contato@institutoluz.org', '1133332222', 'Av. das ONGs, 1000');

-- Inserindo categorias
INSERT INTO categorias (nome, descricao) VALUES
('Roupas', 'Vestuário em geral'),
('Calçados', 'Sapatos, tênis e sandálias'),
('Acessórios', 'Bolsas, cintos, chapéus e mais');

-- Inserindo produtos
INSERT INTO produtos (id_doacao, id_categoria, descricao, marca, tamanho, preco) VALUES
(1, 1, 'Camiseta estampada', 'Zara', 'M', 25.00),
(2, 2, 'Tênis esportivo', 'Nike', '42', 120.00),
(3, 3, 'Bolsa de couro', 'Guess', 'Único', 80.00);

-- Inserindo estoque
INSERT INTO estoque (id_produto, quantidade, secao, prateleira, data_ultima_atualizacao) VALUES
(1, 10, 'A1', 'P1', '2025-04-01'),
(2, 5, 'B2', 'P2', '2025-04-01'),
(3, 2, 'C3', 'P3', '2025-04-01');

-- Inserindo vendas
INSERT INTO venda (id_pessoa, data_venda, valor_total) VALUES
(1, '2025-04-15', 25.00),
(2, '2025-04-20', 120.00),
(3, '2025-04-25', 80.00);

-- Inserindo produto_venda
INSERT INTO produto_venda (id_produto, id_venda, valor_venda) VALUES
(1, 1, 25.00),
(2, 2, 120.00),
(3, 3, 80.00);
