class AppSettings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppSettings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.MINIO_ROOT_USER: str = "minioadmin"
        self.MINIO_ROOT_PASSWORD: str = "minioadmin"
        self.MINIO_VOLUMES: str = "data_lake/mnt/data"
        self.MINIO_HOST: str = "minio1:9000"
        self.MINIO_API: str = "http://" + self.MINIO_HOST

        # PostgreSQL configuration
        self.POSTGRES_HOST: str = "postgres-db"
        self.POSTGRES_PORT: int = 5432
        self.POSTGRES_USER: str = "postgres"
        self.POSTGRES_PASSWORD: str = "admin"
        self.POSTGRES_DB: str = "dop"

        self._initialized = True

    def get_storage_options(self) -> dict:
        return {
            "key": self.MINIO_ROOT_USER,
            "secret": self.MINIO_ROOT_PASSWORD,
            "client_kwargs": {
                "endpoint_url": self.MINIO_API
            }
        }

    def get_database_url(self) -> str:
        """Return PostgreSQL connection URL."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
