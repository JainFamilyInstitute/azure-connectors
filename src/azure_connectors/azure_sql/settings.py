from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class AzureSqlSettings(BaseSettings):
    """
    Represents the settings for connecting to Azure SQL.
    Settings not passed in will be read from from the environment or the ".env" file,
    assuming the prefix "AZURE_SQL_".

    Attributes:
        server (str): The server name.
        database (str): The database name.
        driver (str): The driver name.
        SQL_COPT_SS_ACCESS_TOKEN (int): The access token for SQL Server.
 
    """

    server: str = Field(default=None) # default=None prevents type complaints when using env settings.
    database: str = Field(default=None)
    driver: str = Field(default=None)
    SQL_COPT_SS_ACCESS_TOKEN: int = 1256

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AZURE_SQL_",  # field env vars are prefixed with "AZURE_SQL_"
        extra="ignore",  # don't throw error for unrelated items in .env
        hide_input_in_errors=True,  # don't display any secrets in .env on ValidationError
    )

    @computed_field
    @property
    def connection_string(self) -> str:
        """
        Generates the connection string based on the provided settings.

        Returns:
            The connection string.
        """
        return f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};"
 
    @classmethod
    def from_env(cls, **kwargs) -> 'AzureSqlSettings':
   # def from_env(cls, server: Optional[str]=None, database: Optional[str] = None, driver: Optional[str] = None) -> 'AzureSqlSettings':
        """
        Create an instance by reading settings from the environment variables and .env file.
        Provided for consistency with dependent classes' from_env methods.

        Returns:
            AzureSqlSettings: An instance of AzureSqlSettings with the settings loaded from the environment.

        """
        return cls(**kwargs)