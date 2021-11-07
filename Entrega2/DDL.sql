-- ------------------------------------------------------------------------
-- cria schema e usuário
-- ------------------------------------------------------------------------
create database if not exists IA;
USE IA;
create user if not exists 'iasys'@'localhost' identified by '123';
grant select, insert, delete, update on ia.* to iasys@'localhost';

DROP TABLE IF EXISTS sugerir;
DROP TABLE IF EXISTS transacao;
DROP TABLE IF EXISTS produto;

-- ------------------------------------------------------------------------
-- PRODUTO
-- ------------------------------------------------------------------------
CREATE TABLE produto(
      prd_id                varchar(256) NOT NULL PRIMARY KEY
    , prd_sup					 double
);

-- ------------------------------------------------------------------------
-- TRANSAÇÕES
-- ------------------------------------------------------------------------
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
      sug_percept			 VARCHAR(256) NOT NULL 
    , sug_sugestao		 VARCHAR(256) NOT NULL
    , sug_sup			    DOUBLE
    , sug_conf			    DOUBLE
    , constraint sugerir_percept_fk  FOREIGN KEY (sug_percept)  REFERENCES produto(prd_id)
    , constraint sugerir_sugestao_fk FOREIGN KEY (sug_sugestao) REFERENCES produto(prd_id)
);
CREATE INDEX sugerir_idx_01 ON sugerir (sug_percept, sug_conf DESC);

SELECT * FROM produto;
SELECT * FROM sugerir;
SELECT * FROM transacao;

