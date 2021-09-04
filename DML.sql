-- ------------------------------------------------------------------------
-- PRODUTO
-- ------------------------------------------------------------------------
DELETE FROM sugerir WHERE 1=1;
DELETE FROM produto WHERE 1=1;

INSERT INTO produto (prd_id) VALUES ('café');
INSERT INTO produto (prd_id) VALUES ('leite');
INSERT INTO produto (prd_id) VALUES ('pão');
COMMIT;

-- Se comprar café sugerir leite
INSERT INTO sugerir (sug_percept,sug_sugestao) VALUES ('leite','café');
-- Se comprar café e leite sugerir pão
INSERT INTO sugerir (sug_percept,sug_sugestao) VALUES ('café,leite','pão');

COMMIT;				  

 
SELECT * FROM sugerir;
SELECT * FROM produto;
