import logging as lg
import pandas as pd
import sqlalchemy as sa

from utils.logger import Logger
from utils.settings import AppSettings
from models.bairro_oficial import BairroOficial


class BairrosSilver():
    def __init__(self):
        self.settings = AppSettings()
        self.bairros_table = BairroOficial()
        self.logger: lg.Logging = Logger().get_logger(__name__)
        self.required_args = ["filename"]


    def run(self, args):
        self.logger.info("Running Bairros Silver Service")

        missing_args = [
            arg for arg in self.required_args
            if getattr(args, arg, None) is None
        ]

        if missing_args:
            self.logger.error(f"Missing required arguments: {', '.join(missing_args)}")
            raise

        filename: str = args.filename

        try:
            self.logger.info("Creating table")
            engine: sa.Engine = sa.create_engine(self.settings.get_database_url())
            self.bairros_table.__table__.create(engine, checkfirst=True)

            self.logger.info("Fetching bairros bronze data from minio")
            df_bronze: pd.DataFrame = pd.read_csv(
                f"s3://bronze/{filename}.csv",
                storage_options=self.settings.get_storage_options(),
                dtype=str
            )

            self.logger.info("Processing bairros bronze data")
            df_bronze.columns = df_bronze.columns.str.lower()
            for column in df_bronze.columns:
                df_bronze[column] = df_bronze[column].str.lower().str.strip()

            cols_to_int = ["id_bac", "codigo"]
            df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

            cols_to_float = ["area_km2", "perimetr_m"]
            df_bronze[cols_to_float] = df_bronze[cols_to_float].fillna(0).astype(float)

            self.logger.info("Writing to silver.bairros table")
            # I learnt that polygon can be saved as multipolygon
            # In this case when I save to the database, sqlalchemy will convert for me
            df_bronze.to_sql(
                self.bairros_table.__tablename__,
                con=engine,
                schema=self.bairros_table.__table__.schema,
                if_exists="delete_rows",
                index=False
            )

            self.logger.info("Saving as parquet too")
            # During my research I found that BH is UTM S23 and has SRID 31983
            # I can use geopandas to convert and save as parquet to optimize
            # I won't do this know because this is a mvp of sorts
            df_bronze.to_parquet(
                f"s3://silver/{filename}.parquet",
                engine="pyarrow",
                storage_options=self.settings.get_storage_options()
            )

            self.logger.info("Ran Bairros Silver Service")

        except Exception as e:
            self.logger.error(f"Failed to process: {e}", exc_info=True)
            raise
