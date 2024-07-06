from dataclasses import dataclass
from functools import cached_property

import pyodbc
import sqlalchemy

from azure_connectors.credentials import AzureCredentials
from azure_connectors.credentials.types import AnyHttpsUrl
from .settings import AzureSqlSettings


@dataclass(frozen=True)
class AzureSqlConnection:
    """
    Represents a connection to an Azure SQL database.

    Attributes:
        settings (AzureSqlSettings): The settings for the Azure SQL connection.
        credential (AzureSqlCredential): The credential for the Azure SQL connection.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine for the Azure SQL connection.
    """

    settings: AzureSqlSettings
    credentials: AzureCredentials
    SQLALCHEMY_PREFIX = "mssql://"
    CREDENTIAL_SCOPE = AnyHttpsUrl("https://database.windows.net/.default")

    @classmethod
    def from_env(cls) -> "AzureSqlConnection":
        """
        Create an AzureSqlConnection instance using the settings and credential from the environment.

        Returns:
            AzureSqlConnection: An instance of AzureSqlConnection.
        """
        settings = AzureSqlSettings.from_env()
        credentials = AzureCredentials.from_env(scope=cls.CREDENTIAL_SCOPE)
        return cls(settings=settings, credentials=credentials)

    @cached_property
    def engine(self) -> sqlalchemy.engine.base.Engine:
        """
        Get the SQLAlchemy engine for the Azure SQL connection, using self._connect as connection function.

        Returns:
            sqlalchemy.engine.base.Engine: The SQLAlchemy engine.
        """
        engine = sqlalchemy.create_engine(self.SQLALCHEMY_PREFIX, creator=self._connect)
        return engine

    def _connect(self) -> pyodbc.Connection:
        """
        Connect to the Azure SQL database using the connection string and access token.

        Returns:
            pyodbc.Connection: The pyodbc connection object.
        """
        token = self.credentials.token.get_secret_value()
        return pyodbc.connect(self.settings.connection_string, attrs_before={self.settings.SQL_COPT_SS_ACCESS_TOKEN: token})
