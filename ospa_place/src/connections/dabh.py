import json
from urllib import request as rq


class PortalBH():
    def __init__(self):
        self.BASE_URL: str = "https://ckan.pbh.gov.br/api/3/action"
        self.HEADERS: dict[str, str] = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

    def get_url(self, dataset_name: str, filename: str) -> str:
        search_url: str = f"{self.BASE_URL}/package_search?q={dataset_name}"
        request: rq.Request = rq.Request(search_url, headers=self.HEADERS)

        with rq.urlopen(request) as response:
            search_data: dict = json.loads(response.read().decode())

        results: list = search_data["result"]["results"]

        dataset: dict | None = None
        for result in results:
            if result["name"] == dataset_name:
                dataset = result
                break

        download_url: str | None = None
        for resource in dataset["resources"]:
            if resource["name"] == filename:
                download_url = resource["url"]
                break

        return download_url
