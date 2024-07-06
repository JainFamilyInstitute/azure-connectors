from dataclasses import dataclass

@dataclass(frozen=True)
class EnvConfig:
    ENV_FILE: str = ".env"
    AZURE_SQL_PREFIX: str = "AZURE_SQL_"
    CREDENTIALS_PREFIX: str = "AZURE_CREDENTIALS_"

    def __new__(cls, *args, **kwargs):
        raise TypeError(f"{cls.__name__} is not meant to be instantiated. Usage: {cls.__name__}.ENV_FILE.")