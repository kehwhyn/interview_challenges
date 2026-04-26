import os


class AppSettings:
    def __init__(self):
        # DABH
        self.DABH_API: str = os.environ.get("DABH_API")

        # MinIO
        self.MINIO_ROOT_USER: str = os.environ.get("MINIO_ROOT_USER")
        self.MINIO_ROOT_PASSWORD: str = os.environ.get("MINIO_ROOT_PASSWORD")
        self.MINIO_API_URL: str = os.environ.get("MINIO_API_URL")

        # PostGIS
        self.POSTGIS_HOST: str = os.environ.get("POSTGIS_HOST")
        self.POSTGIS_PORT: int = os.environ.get("POSTGIS_PORT")
        self.POSTGIS_USER: str = os.environ.get("POSTGIS_USER")
        self.POSTGIS_PASSWORD: str = os.environ.get("POSTGIS_PASSWORD")
        self.POSTGIS_DB: str = os.environ.get("POSTGIS_DB")


    def get_storage_options(self) -> dict:
        return {
            "key": self.MINIO_ROOT_USER,
            "secret": self.MINIO_ROOT_PASSWORD,
            "client_kwargs": {
                "endpoint_url": self.MINIO_API_URL
            }
        }


    def get_database_url(self) -> str:
        """Return PostgreSQL connection URL."""
        return f"postgresql://{self.POSTGIS_USER}:{self.POSTGIS_PASSWORD}@{self.POSTGIS_HOST}:{self.POSTGIS_PORT}/{self.POSTGIS_DB}"
