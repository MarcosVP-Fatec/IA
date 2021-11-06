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
-- TRANSAÇÕES
-- ------------------------------------------------------------------------
DROP TABLE transacao;
CREATE TABLE transacao (
      tran_id      		 VARCHAR(256) NOT NULL
    , tran_prod   		 VARCHAR(256) NOT NULL
    , tran_date_time		 DATETIME	  NOT NULL
    , tran_period_day	 VARCHAR(10)  NOT NULL
    , tran_week_day_end  VARCHAR(7)   NOT NULL
    , CONSTRAINT transacoes_prod_fk FOREIGN KEY (tran_prod) REFERENCES produto(prd_id)
);

-- ------------------------------------------------------------------------
-- SUGERIR
-- ------------------------------------------------------------------------
CREATE TABLE sugerir (
      sug_percept			 VARCHAR(256) NOT NULL PRIMARY KEY
    , sug_sugestao		 VARCHAR(256) NOT NULL
    , constraint sugerir_sugestao_fk FOREIGN KEY (sug_sugestao) REFERENCES produto(prd_id)
);




