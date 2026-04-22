import pandas as pd
import sqlalchemy as sa

from settings import AppSettings
from models.atividade_economica import AtividadeEconomica


class EmpresasSilver():
    def __init__(self):
        pass

    def run(self, args: dict[str, str]):
        print("Running Empresas Silver Service")

        settings = AppSettings()
        filename: str = args.filename
        empresas_table = AtividadeEconomica()
        engine: sa.Engine = sa.create_engine(settings.get_database_url())

        empresas_table.metadata.create_all(engine)

        print(f"Reading file from s3://bronze/{filename}.csv")
        df_bronze: pd.DataFrame = pd.read_csv(
            f"s3://bronze/{filename}.csv",
            storage_options= settings.get_storage_options(),
            dtype=str
        )

        print("Cleaning and Parsing data")
        df_bronze.columns = df_bronze.columns.str.lower()
        for column in df_bronze.columns:
            df_bronze[column] = df_bronze[column].str.lower().str.strip()

        cols_to_int = ["id_ativ_econ_estabelecimento", "numero_imovel"]
        df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

        df_bronze["area_utilizada"] = df_bronze["area_utilizada"].astype(float)

        cols_to_bool = ["ind_simples", "ind_mei", "ind_possui_alvara"]
        df_bronze[cols_to_bool] = df_bronze[cols_to_bool].map(
            {"sim": True, "s": True, "não": False, "n": False}
        )

        print("Saving file to database and s3://silver/")
        # I learnt that polygon can be saved as multipolygon
        # In this case when I save to the database, sqlalchemy will convert for me
        df_bronze.to_sql(
            empresas_table.__tablename__,
            con=engine,
            schema=empresas_table.__table__.schema,
            if_exists="delete_rows",
            chunksize=100,
            index=False
        )

        # During my research I found that BH is UTM S23 and has SRID 31983
        # I can use geopandas to convert and save as parquet to optimize
        # I won't do this know because this is a mvp of sorts
        df_bronze.to_parquet(
            f"s3://silver/{filename}.parquet",
            engine="pyarrow",
            storage_options= settings.get_storage_options()
        )

        print("Ran Empresas Silver Service")
