-- ------------------------------------------------------------------------
-- cria schema e usuário
-- ------------------------------------------------------------------------
create database if not exists IA;
USE IA;
create user if not exists 'iasys'@'localhost' identified by '123';
grant select, insert, delete, update on ia.* to iasys@'localhost';

-- DROP TABLE sugerir;
-- DROP TABLE produto;

-- ------------------------------------------------------------------------
-- PRODUTO
-- ------------------------------------------------------------------------
CREATE TABLE produto(
      prd_id                varchar(256) NOT NULL PRIMARY KEY
);

-- ------------------------------------------------------------------------
-- SUGERIR
-- ------------------------------------------------------------------------
CREATE TABLE sugerir (
      sug_percept			 VARCHAR(256) NOT NULL PRIMARY KEY
    , sug_sugestao		 VARCHAR(256) NOT NULL
    , constraint sugerir_sugestao_fk FOREIGN KEY (sug_sugestao) REFERENCES produto(prd_id)
);





