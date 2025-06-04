# Desafio técnico Appmax


## Enunciado

O objetivo deste teste é validar os conhecimentos e habilidades técnicas e a capacidade de resolver problemas.

Anexamos um [CSV](data/dados_iniciais.csv) com 20 CNPJs, ele é o nosso ponto de partida. Precisamos que esses CNPJs sejam enriquecidos em uma api. Optamos pela api aberta da [receitaws](https://developers.receitaws.com.br/#/operations/queryCNPJFree) por possuir uma camada gratuita. Com o resultado da consulta, vamos gerar um arquivo tabulado contendo os seguintes dados: **CNPJ**, **data de abertura**, **nome**, **atividade_principal**, **atividade_secundaria** (caso tenha, e
caso tenha mais de uma armazenar apenas a primeira), **ultima_atualizacao** e **capital_social**. Precisamos que sejam armazenados nos campos atividade_principal e atividade_secundaria **apenas os números e não os títulos**, removendo as pontuações. O resultado dessa consulta deve ser armazenado em um arquivo CSV na mesma estrutura, utilizando o `;` como separador.

Partindo do CSV original contendo os CNPJs, supondo que o CSV seja a tabela empresas em um banco de dados relacional, qual das datas que mais aparece? Precisamos que seja elaborada uma consulta SQL que atribua uma posição ou classificação a cada linha, com base na quantidade de datas, ordenando as de forma decrescente.

Enviar o resultado e o código gerado para realizar a consulta da API e a consulta SQL, anexando no e-mail direto pasta zipada ou o via link de repositório git aberto para o email indicado.


## Como rodar

No **root** do projeto deve ser criada um dir `data` que deverá ter o arquivo `.csv` disponibilizado para o desafio. Após completar a execução um novo arquivo `dados_finais.csv` vai ser gerado na mesma pasta com as novas colunas adicionadas, além do separador exigido.

No terminal dentro da pasta clonada do github digite `docker compose up`. Testei tanto no windows quanto no linux.

Criei um [docker compose](docker-compose.yml) que cria dois containeres, um sobe o banco MySQL e o outro executa o código do desafio e cria os dados para rodar a query no banco. Para se conectar ao banco, recomendo o MySQL Workbench. A query está inclusa no repositório.


## Desenvolvimento


### Análise do enunciado

Após ler o enunciado separei o que precisava fazer por etapas:
1. Entender a API. Quais dados tenho que enviar para o endpoint? Que dados vou extrair dali? Tem alguma restrição?
2. Adicionar novas colunas ao `df` e salvar ele com um novo separador
3. Escrever uma query baseada no arquivo original ordenando as datas por ordem de frequência e atribuindo posições


### Solução

Utilizei a biblioteca `requests` para lidar com a parte da API e `pandas` para a manipulação dos dados. No início do arquivo declarei variáveis que iriam me ajudar no desenvolvimento como, por exemplo: `INPUT`, `OUTPUT`, `API` etc.

Primeiro li o arquivo inicial e executei o código responsável por popular o banco com a tabela `empresas`, para poder realizar a consulta exigida pelo desafio.
```python
df: pd.DataFrame = pd.read_csv(INPUT, parse_dates=["data_inicial"])

def save_to_db(df: pd.DataFrame):
    engine = create_engine(DB_URL)
    df.to_sql("empresas", con=engine, if_exists='replace', index=False)
```

Optei por criar uma lista de CNPJs para assim poder iterar e fazer chamadas para a API. Iterei sobre a lista e a cada três chamadas realizava uma pausa, devido a restrição da API. Utilizei uma função auxiliar que utiliza **regex** para extrair só os números do CNPJ como string.
```python
cnpjs: list[str] = df["cnpj"].tolist()
for index, cnpj in enumerate(cnpjs):

    if index % 3 == 0:
        time.sleep(65)

    url: str = API + extract_numbers(cnpj)
    response: requests.Response = requests.get(url)
    data: dict = response.json()
```

Em seguida peguei os dados da API, filtrei pelo CNPJ e adicionei as novas colunas no `df` e, fora do loop, salvei o arquivo no formato requisitado.
```python
df.loc[df['cnpj'] == cnpj, "abertura"] = data["abertura"]
df.loc[df['cnpj'] == cnpj, "nome"] = data["nome"]
df.loc[df['cnpj'] == cnpj, "atividade_principal"] = extract_numbers(data["atividade_principal"][0]["code"])
df.loc[df['cnpj'] == cnpj, "atividades_secundarias"] = extract_numbers(data["atividades_secundarias"][0]["code"])
df.loc[df['cnpj'] == cnpj, "ultima_atualizacao"] = data["ultima_atualizacao"]
df.loc[df['cnpj'] == cnpj, "capital_social"] = data["capital_social"]

df.to_csv(OUTPUT, sep=";", index=False)
```

Assim o programa termina a execução criando um novo arquivo `dados_finais.csv` na dir `data`.

Sobre a parte da consulta, não foi específicado como fazer o desempate de datas que fiquem na mesma posição, utilizando algum critério como: da data mais antiga a mais recente, por exemplo. A query para ordenar as datas por ordem de frequência e atribuindo posições é a seguinte:
```sql
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
```


### Conclusões

Após análise, decidi por manter a simplicidade. Não adicionei complexidade desnecessária, levando em conta o contexto. Podia ter criando algo com spark, hive e pyspark. Abstraido a questão do banco e criado uma classe para a tabela de empresas e pedir para escrever. Mas no meu atual momento precisaria de um pouco mais de tempo.

A questão da API é um blocker que limita o tempo. Entendo que tenha outras formas de acelerar o processo, como criar uma pool de requests que randomiza e faz um bypass.

Fiquei em dúvidas sobre a parte da query, pois não entendi muito bem se era para ordenar pela `quantidade DESC` ou `posicao`. Achei melhor deixar ordenada pela quantidade e incluir a coluna de posição que ficaria na ordem correta.
