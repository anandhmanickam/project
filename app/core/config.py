from pathlib import Path
from sys import modules

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    """Application settings."""

    ENV: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    _BASE_URL: str = f"https://{HOST}:{PORT}"
    # quantity of workers for uvicorn
    WORKERS_COUNT: int = 1
    # Enable uvicorn reloading
    RELOAD: bool = False
    # Database settings
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "test5"
    DB_PASS: str = "M/lwbF(qHZN(VHe9"
    _DB_BASE: str = "test5"
    DB_ECHO: bool = False

    @property
    def DB_BASE(self):
        return self._DB_BASE

    @property
    def BASE_URL(self) -> str:
        return self._BASE_URL if self._BASE_URL.endswith("/") else f"{self._BASE_URL}/"

    @property
    def DB_URL(self) -> str:
        """
        Assemble Database URL from settings.

        :return: Database URL.
        """

        # return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASE}"
        # return "mysql++asyncmy://root@127.0.0.1:3306/test4"
        
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASE}"
        
        
    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"
        fields = { 
            "_BASE_URL": {
                "env": "BASE_URL",
            },
            "_DB_BASE": {
                "env": "DB_BASE",
            },
        }


class TestSettings(Settings):
    @property
    def DB_BASE(self):
        return f"{super().DB_BASE}_test"


settings = TestSettings() if "pytest" in modules else Settings()
