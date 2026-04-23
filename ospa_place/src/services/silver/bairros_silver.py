import logging
import pandas as pd
import sqlalchemy as sa

from settings import AppSettings
from models.bairro_oficial import BairroOficial


logger = logging.getLogger(__name__)


class BairrosSilver():
    def __init__(self):
        pass

    def run(self, args: dict[str, str]):
        logger.info("Running Bairros Silver Service")

        settings = AppSettings()
        filename: str = args.filename
        bairros_table = BairroOficial()

        try:
            logger.info("Creating tables")
            engine: sa.Engine = sa.create_engine(settings.get_database_url())
            bairros_table.metadata.create_all(engine)

            logger.info("Fetching bairros bronze data from minio")
            df_bronze: pd.DataFrame = pd.read_csv(
                f"s3://bronze/{filename}.csv",
                storage_options= settings.get_storage_options(),
                dtype=str
            )

            logger.info("Processing bairros bronze data")
            df_bronze.columns = df_bronze.columns.str.lower()
            for column in df_bronze.columns:
                df_bronze[column] = df_bronze[column].str.lower().str.strip()

            cols_to_int = ["id_bac", "codigo"]
            df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

            cols_to_float = ["area_km2", "perimetr_m"]
            df_bronze[cols_to_float] = df_bronze[cols_to_float].fillna(0).astype(float)

            logger.info("Writing to silver.bairros table")
            # I learnt that polygon can be saved as multipolygon
            # In this case when I save to the database, sqlalchemy will convert for me
            df_bronze.to_sql(
                bairros_table.__tablename__,
                con=engine,
                schema=bairros_table.__table__.schema,
                if_exists="delete_rows",
                index=False
            )

            logger.info("Saving as parquet too")
            # During my research I found that BH is UTM S23 and has SRID 31983
            # I can use geopandas to convert and save as parquet to optimize
            # I won't do this know because this is a mvp of sorts
            df_bronze.to_parquet(
                f"s3://silver/{filename}.parquet",
                engine="pyarrow",
                storage_options= settings.get_storage_options()
            )

            logger.info("Ran Bairros Silver Service")

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            raise