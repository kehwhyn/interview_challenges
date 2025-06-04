import re
import time
import requests
import pandas as pd
from sqlalchemy import create_engine


INPUT: str = "data/dados_iniciais.csv"
OUTPUT: str = "data/dados_finais.csv"
API: str = "https://receitaws.com.br/v1/cnpj/"
DB_URL: str = "mysql+pymysql://mysqlUser:mysqlPW@maxters-db:3306/mysqlDB"
extract_numbers: str = lambda x: re.sub(r"[^0-9]", "", x)


def main():
    df: pd.DataFrame = pd.read_csv(INPUT, parse_dates=["data_inicial"])

    save_to_db(df)

    cnpjs: list[str] = df["cnpj"].tolist()
    for index, cnpj in enumerate(cnpjs):

        if index % 3 == 0:
            time.sleep(65)

        url: str = API + extract_numbers(cnpj)
        response: requests.Response = requests.get(url)

        data: dict = response.json()
        df.loc[df['cnpj'] == cnpj, "abertura"] = data["abertura"]
        df.loc[df['cnpj'] == cnpj, "nome"] = data["nome"]
        df.loc[df['cnpj'] == cnpj, "atividade_principal"] = extract_numbers(data["atividade_principal"][0]["code"])
        df.loc[df['cnpj'] == cnpj, "atividades_secundarias"] = extract_numbers(data["atividades_secundarias"][0]["code"])
        df.loc[df['cnpj'] == cnpj, "ultima_atualizacao"] = data["ultima_atualizacao"]
        df.loc[df['cnpj'] == cnpj, "capital_social"] = data["capital_social"]

    df.to_csv(OUTPUT, sep=";", index=False)


def save_to_db(df: pd.DataFrame):
    engine = create_engine(DB_URL)
    df.to_sql("empresas", con=engine, if_exists='replace', index=False)


if __name__ == "__main__":
        main()
