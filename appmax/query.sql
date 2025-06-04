-- Active: 1746132939145@@localhost@3306@mysqlDB
WITH contagem_dias AS (
    SELECT
        DATE(data_inicial) AS dia,
        COUNT(*) AS quantidade
    FROM empresas
    GROUP BY dia
),
ranked AS (
    SELECT
        dia,
        quantidade,
        (SELECT COUNT(*) FROM contagem_dias cd2 WHERE cd2.quantidade > cd1.quantidade) + 1 AS posicao
    FROM contagem_dias cd1
)
SELECT *
FROM ranked
ORDER BY quantidade DESC;
