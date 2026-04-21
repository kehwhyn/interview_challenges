import minio
import pandas as pd
import sqlalchemy as sa

from settings import AppSettings
from models.bairro_oficial import BairroOficial


class BairrosSilver():
    def __init__(self):
        pass

    def run(self, args: dict[str, str]):
        print("Running Bairros Silver Service")

        settings = AppSettings()
        filename: str = args.filename
        bairros_table = BairroOficial()
        engine: sa.Engine = sa.create_engine(settings.get_database_url())

        bairros_table.metadata.create_all(engine)

        df_bronze: pd.DataFrame = pd.read_csv(
            f"s3://bronze/{filename}.csv",
            storage_options= settings.get_storage_options(),
            dtype=str
        )

        df_bronze.columns = df_bronze.columns.str.lower()
        for column in df_bronze.columns:
            df_bronze[column] = df_bronze[column].str.lower().str.strip()

        cols_to_int = ["id_bac", "codigo"]
        df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

        cols_to_float = ["area_km2", "perimetr_m"]
        df_bronze[cols_to_float] = df_bronze[cols_to_float].fillna(0).astype(float)

        # I learnt that polygon can be saved as multipolygon
        # In this case when I save to the database, sqlalchemy will convert for me
        df_bronze.to_sql(
            bairros_table.__tablename__,
            con=engine,
            schema=bairros_table.__table__.schema,
            if_exists="delete_rows",
            index=False
        )

        # During my research I found that BH is UTM S23 and has SRID 31983
        # I can use geopandas to convert and save as parquet to optimize
        # I won't do this know because this is a mvp of sorts
        client = minio.Minio(
            settings.MINIO_HOST,
            settings.MINIO_ROOT_USER,
            settings.MINIO_ROOT_PASSWORD,
            secure=False
        )
        if not client.bucket_exists("silver"):
            client.make_bucket("silver")

        df_bronze.to_parquet(
            f"s3://silver/{filename}.parquet",
            engine="pyarrow",
            storage_options= settings.get_storage_options()
        )

        print("Ran Bairros Silver Service")
