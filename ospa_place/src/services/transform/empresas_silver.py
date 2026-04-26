import logging as lg
import pandas as pd
import sqlalchemy as sa

from utils.logger import Logger
from utils.settings import AppSettings
from models.atividade_economica import AtividadeEconomica


class EmpresasSilver():
    def __init__(self):
        self.settings = AppSettings()
        self.empresas_table = AtividadeEconomica()
        self.logger: lg.Logging = Logger().get_logger(__name__)
        self.required_args = ["filename"]

    def run(self, args):
        self.logger.info("Running Empresas Silver Service")

        missing_args = [
            arg for arg in self.required_args
            if getattr(args, arg, None) is None
        ]

        if missing_args:
            self.logger.error(f"Missing required arguments: {', '.join(missing_args)}")
            raise

        filename: str = args.filename

        try:
            self.logger.info("Creating tables")
            engine: sa.Engine = sa.create_engine(self.settings.get_database_url())
            self.empresas_table.__table__.create(engine, checkfirst=True)

            self.logger.info(f"Reading file from s3://bronze/{filename}.csv")
            df_bronze: pd.DataFrame = pd.read_csv(
                f"s3://bronze/{filename}.csv",
                storage_options=self.settings.get_storage_options(),
                dtype=str
            )

            self.logger.info("Cleaning and Parsing data")
            df_bronze.columns = df_bronze.columns.str.lower()
            for column in df_bronze.columns:
                df_bronze[column] = df_bronze[column].str.lower().str.strip()

            cols_to_int = ["id_ativ_econ_estabelecimento", "numero_imovel"]
            df_bronze[cols_to_int] = df_bronze[cols_to_int].fillna(0).astype(int)

            df_bronze["area_utilizada"] = df_bronze["area_utilizada"].astype(float)

            cols_to_bool = ["ind_simples", "ind_mei", "ind_possui_alvara"]
            df_bronze[cols_to_bool] = df_bronze[cols_to_bool].replace(
                {"sim": True, "s": True, "não": False, "n": False}
            )

            self.logger.info("Saving file to database and s3://silver/")
            # I learnt that polygon can be saved as multipolygon
            # In this case when I save to the database, sqlalchemy will convert for me
            df_bronze.to_sql(
                self.empresas_table.__tablename__,
                con=engine,
                schema=self.empresas_table.__table__.schema,
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
                storage_options=self.settings.get_storage_options()
            )

            self.logger.info("Ran Empresas Silver Service")

        except Exception as e:
            self.logger.error(f"Failed to process: {e}", exc_info=True)
            raise