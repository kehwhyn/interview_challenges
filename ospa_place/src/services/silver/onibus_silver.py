import pandas as pd
import sqlalchemy as sa

from settings import AppSettings
from models.ponto_onibus import PontoOnibus


class OnibusSilver():
    def __init__(self):
        pass

    def run(self, args: dict[str, str]):
        print("Running Onibus Silver Service")

        settings = AppSettings()
        filename: str = args.filename
        onibus_table = PontoOnibus()
        engine: sa.Engine = sa.create_engine(settings.get_database_url())

        onibus_table.metadata.create_all(engine)

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

        cols_to_int = ["id_ponto_onibus_linha", "identificador_ponto_onibus"]
        df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

        print("Saving file to database and s3://silver/")
        # I learnt that polygon can be saved as multipolygon
        # In this case when I save to the database, sqlalchemy will convert for me
        df_bronze.to_sql(
            onibus_table.__tablename__,
            con=engine,
            schema=onibus_table.__table__.schema,
            if_exists="delete_rows",
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

        print("Ran Onibus Silver Service")
