'DDL (Data Definition Language): Criar e modificar tabelas.'
CREATE TABLE peso(
  id PRIMARY KEY UNIQUE,
  peso VARCHAR(100)
);
INSERT INTO peso VALUES
(5,'GLP 5 KG'),
(8,'GLP 8 KG'),
(13,'GLP 13 KG'),
(20,'GLP 20 KG'),
(45,'GLP 45 KG'),
(90,'GLP 90 KG');
SELECT * FROM peso;

CREATE TABLE marca(
  id PRIMARY KEY UNIQUE,
  marca VARCHAR(100)
);
INSERT INTO marca VALUES
(1,'GasBrás'),
(2,'MinasGás'),
(3,'LiquiGás');
SELECT * FROM marca;

CREATE TABLE gas(
  id PRIMARY KEY UNIQUE,
  peso INT,
  marca INT,
  endereco VARCHAR(100),
  qtd INT,
  preco DECIMAL(10, 2),
  total DECIMAL(10, 2) GENERATED ALWAYS AS (ROUND(qtd * preco, 2)) STORED,
  FOREIGN KEY (peso) REFERENCES peso(id),
  FOREIGN KEY (marca) REFERENCES marca(id)
);
INSERT INTO gas (id, peso, marca, endereco, qtd, preco)VALUES
(1,5,1,'Rua 15, 35, Castelo São Manoel',5,55),
(2,8,1,'Rua 6, 350, Castelo São Manoel',3,82),
(3,13,3,'Rua 1, 31, Castelo São Manoel',2,120),
(4,20,2,'Rua A, 3500, Nogueira',1,150),
(5,45,2,'Rua Indaiá, 350, São Sebastião',4,300),
(6,90,3,'Rua General Rondon, 1000, Quitandinha',6,480);
SELECT * FROM gas;

'DML (Data Manipulation Language): Inserir, atualizar e possivelmente excluir dados de exemplo.'
'Consultas Básicas: SELECT, FROM, WHERE, ORDER BY.'
INSERT INTO gas (id, peso, marca, endereco, qtd, preco)VALUES
(7,13,1,'Rua 15, 35, Castelo São Manoel',1,120),
(8,13,1,'Rua 6, 350, Castelo São Manoel',4,120);
SELECT * FROM gas;
SELECT * FROM gas ORDER BY marca;
DELETE FROM gas WHERE id = 7;
SELECT * FROM gas WHERE marca = 1;

'Funções de Agregação: COUNT(), SUM(), AVG(), MIN(), MAX()'
SELECT COUNT(marca=1) as Liquigas FROM gas;
SELECT COUNT(marca=2) as Minasgas FROM gas;
SELECT COUNT(marca=3) as Gasbras FROM gas;
SELECT sum(qtd) as TotalQuantidade FROM gas;
SELECT sum(preco) as TotalPreco FROM gas;
SELECT sum(Total) as TotalGeral FROM gas;
SELECT round(avg(preco),2) as MediaPreco FROM gas; 
SELECT round(avg(total),2) as MediaTotal FROM gas; 
SELECT round(avg(qtd),0) as MediaQuantidade FROM gas;
SELECT max(qtd) as QuantidadeMaisAlta FROM gas;
SELECT min(qtd) as QuantidadeMaisBaixa FROM gas;
SELECT max(preco) as PrecoMaisAlto FROM gas;
SELECT min(preco) as PrecoMaisBaixo FROM gas;
SELECT max(id) as PesoMaisAlto FROM peso;
SELECT min(id) as PesoMaisBaixo FROM peso;



