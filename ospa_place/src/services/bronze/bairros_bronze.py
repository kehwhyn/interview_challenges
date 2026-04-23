import logging
import pandas as pd
from urllib import request as rq

from settings import AppSettings
from connections.dabh import PortalBH


# Create module-level logger - will inherit root logger configuration
logger = logging.getLogger(__name__)


class BairrosBronze():
    def __init__(self):
        pass

    def run(self, args):
        # Just use the logger - it's already configured!
        logger.info("Starting Bairros Bronze service")
        logger.info(f"Dataset: {args.dataset}, Filename: {args.filename}")

        dataset_name: str = args.dataset
        filename: str = args.filename

        settings = AppSettings()
        portal: PortalBH = PortalBH()

        try:
            logger.info(f"Fetching data...")
            download_url = portal.get_url(dataset_name, filename)
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
            req: rq.Request = rq.Request(download_url, headers=headers)
            with rq.urlopen(req) as response:
                if response.status == 200:
                    df: pd.DataFrame = pd.read_csv(response, dtype=str)

                    logger.info(f"Saving file to s3://bronze/{filename}.csv")
                    df.to_csv(
                        f"s3://bronze/{filename}.csv",
                        storage_options=settings.get_storage_options(),
                        index=False
                    )

            logger.info("Ran Bairros Bronze Service")

        except Exception as e:
            logger.error(f"Failed to process: {e}", exc_info=True)
            raise
