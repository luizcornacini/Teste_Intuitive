-- Criar o banco de dados
CREATE DATABASE ans_db;
USE ans_db;

-- Criar tabela operadoras
CREATE TABLE operadoras (
    id_operadora INT PRIMARY KEY,
    nome VARCHAR(255),
    registro_ans VARCHAR(50),
    cnpj VARCHAR(20),
    modalidade VARCHAR(100),
    uf CHAR(2),
    municipio VARCHAR(100),
    telefone VARCHAR(50),
    email VARCHAR(255)
);

-- Criar tabela demonstrativos_contabeis
CREATE TABLE demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    id_operadora INT,
    ano INT,
    trimestre INT,
    evento_sinistros DECIMAL(15,2),
    FOREIGN KEY (id_operadora) REFERENCES operadoras(id_operadora)
);

-- Importar os dados das operadoras (⚠️ Verifique se o CSV está no formato correto)
LOAD DATA INFILE 'C:\\Users\\Luiz\\Desktop\\teste\\Banco\\Relatorio_cadop.csv'
INTO TABLE operadoras
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Importar os dados contábeis (⚠️ Certifique-se de que há um CSV adequado para isso)
LOAD DATA INFILE 'C:\\Users\\Luiz\\Desktop\\teste\\Banco\\2024\\demonstrativos_contabeis.csv'
INTO TABLE demonstrativos_contabeis
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Consulta: 10 operadoras com maiores despesas no último trimestre
SELECT o.nome, d.ano, d.trimestre, SUM(d.evento_sinistros) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.id_operadora = o.id_operadora
WHERE d.ano = (SELECT MAX(ano) FROM demonstrativos_contabeis)
AND d.trimestre = (SELECT MAX(trimestre) FROM demonstrativos_contabeis WHERE ano = (SELECT MAX(ano) FROM demonstrativos_contabeis))
GROUP BY o.nome, d.ano, d.trimestre
ORDER BY total_despesas DESC
LIMIT 10;

-- Consulta: 10 operadoras com maiores despesas no último ano
SELECT o.nome, d.ano, SUM(d.evento_sinistros) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o ON d.id_operadora = o.id_operadora
WHERE d.ano = (SELECT MAX(ano) FROM demonstrativos_contabeis)
GROUP BY o.nome, d.ano
ORDER BY total_despesas DESC
LIMIT 10;




