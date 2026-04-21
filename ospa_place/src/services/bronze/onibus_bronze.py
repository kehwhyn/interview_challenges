import pandas as pd
from urllib import request as rq

from settings import AppSettings
from connections.dabh import PortalBH

class OnibusBronze():
    def __init__(self):
        pass

    def run(self, args):
        print("Running Onibus Bronze Service")
        dataset_name: str = args.dataset
        filename: str = args.filename

        settings = AppSettings()
        portal: PortalBH = PortalBH()

        print(f"Fetching data...")
        download_url = portal.get_url(dataset_name, filename)
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        req: rq.Request = rq.Request(download_url, headers=headers)
        with rq.urlopen(req) as response:
            if response.status == 200:
                df: pd.DataFrame = pd.read_csv(response, dtype=str, sep=";")

                print(f"Saving file to s3://bronze/{filename}.csv")
                df.to_csv(
                    f"s3://bronze/{filename}.csv",
                    storage_options=settings.get_storage_options(),
                    index=False
                )

        print("Ran Onibus Bronze Service")
