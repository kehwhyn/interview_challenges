import logging as lg
from urllib import request as rq

import pandas as pd

from utils.dabh import PortalBH
from utils.logger import Logger
from utils.settings import AppSettings


class EmpresasBronze():
    def __init__(self):
        self.logger: lg.Logging = Logger().get_logger(__name__)
        self.required_args = ["dataset", "filename"]


    def run(self, args):
        missing_args = [
            arg for arg in self.required_args
            if getattr(args, arg, None) is None
        ]

        if missing_args:
            self.logger.error(f"Missing required arguments: {', '.join(missing_args)}")
            raise

        dataset: str = args.dataset
        filename: str = args.filename

        self.logger.info("Starting Empresas Bronze service")
        self.logger.info(f"Dataset: {dataset}, Filename: {filename}")

        settings = AppSettings()
        portal: PortalBH = PortalBH()

        try:
            self.logger.info(f"Fetching data...")
            download_url = portal.get_url(dataset, filename)
            req: rq.Request = rq.Request(download_url, headers=portal.HEADERS)
            with rq.urlopen(req) as response:
                if response.status == 200:
                    df: pd.DataFrame = pd.read_csv(response, dtype=str, sep=";")

                    self.logger.info(f"Saving file to s3://bronze/{filename}.csv")
                    df.to_csv(
                        f"s3://bronze/{filename}.csv",
                        storage_options=settings.get_storage_options(),
                        index=False
                    )

            self.logger.info("Ran Empresas Bronze Service")

        except Exception as e:
            self.logger.error(f"Failed to process: {e}", exc_info=True)
            raise
