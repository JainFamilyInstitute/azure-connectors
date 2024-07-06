import re

from pydantic import Field, computed_field, field_validator
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

    server: str = Field(
        default=None
    )  # default=None prevents type complaints when using env settings.
    database: str = Field(default="ODBC Driver 18 for SQL Server")
    driver: str = Field(default=None)
    SQL_COPT_SS_ACCESS_TOKEN: int = 1256

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AZURE_SQL_",  # field env vars are prefixed with "AZURE_SQL_"
        extra="ignore",  # don't throw error for unrelated items in .env
        hide_input_in_errors=True,  # don't display any secrets in .env on ValidationError
    )

    @field_validator("server")
    @classmethod
    def server_must_be_valid_azure(cls, v: str) -> str:
        if not v.lower().endswith(".database.windows.net"):
            raise ValueError("Server must be a valid Azure SQL server.")
        return v.lower()

    @field_validator("database")
    @classmethod
    def database_must_be_valid_mssql_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Database name must not be empty.")
        if len(v) > 128:
            raise ValueError("Database name must be 128 characters or fewer.")
        if not v[0].isalpha():
            raise ValueError("Database name start with an alphabetic character.")
        if " " in v:
            raise ValueError("Database name must not contain spaces.")
        if re.search(r'[\\/\:*?"<>|]', v):
            raise ValueError("Database name contains invalid characters.")
        return v

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
    def from_env(
        cls,
        server: Optional[str] = None,
        database: Optional[str] = None,
        driver: Optional[str] = None,
    ) -> "AzureSqlSettings":
        """
        Create an instance of AzureSqlSettings by reading the settings not passed explicitly
        from the environment variables and .env file.

        Provided for consistency with dependent classes' from_env methods.

        Args:
            server (Optional[str]): The server name for the Azure SQL connection. If not provided, it will be read from the environment.
            database (Optional[str]): The database name for the Azure SQL connection. If not provided, it will be read from the environment.
            driver (Optional[str]): The driver name for the Azure SQL connection. If not provided, it will be read from the environment.

        Returns:
            AzureCredentialSettings: An instance of AzureCredentialSettings with the settings loaded from the environment.

        """
        pass_kwargs = {
            k: v for k, v in locals().items() if v is not None and k != "cls"
        }
        return cls(**pass_kwargs)
