from dataclasses import dataclass
from functools import cached_property

import pyodbc
import sqlalchemy

from azure_connectors.credentials import AzureCredentials
from azure_connectors.enums import CredentialScope

from .constants import SQL_COPT_SS_ACCESS_TOKEN, SQLALCHEMY_PREFIX
from .settings import AzureSqlSettings


@dataclass(frozen=True)
class AzureSqlConnection:
    """
    Represents a connection to an Azure SQL database.

    Attributes:
        settings (AzureSqlSettings): The settings for the Azure SQL connection.
        credentials (AzureCredentials): The credentials for the Azure SQL connection.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine for the Azure SQL connection.
    """

    settings: AzureSqlSettings
    credentials: AzureCredentials

    CREDENTIAL_SCOPE: CredentialScope = CredentialScope.AZURE_SQL
  

    @classmethod
    def from_env(cls) -> "AzureSqlConnection":
        """
        Create an AzureSqlConnection instance using the settings and credential from the environment.

        Returns:
            AzureSqlConnection: An instance of AzureSqlConnection.
        """
        settings = AzureSqlSettings()
        credentials = AzureCredentials.from_env(scope=cls.CREDENTIAL_SCOPE)
        return cls(settings=settings, credentials=credentials)

    @cached_property
    def engine(self) -> sqlalchemy.engine.base.Engine:
        """
        Get the SQLAlchemy engine for the Azure SQL connection, using self._connect as connection function.

        Returns:
            sqlalchemy.engine.base.Engine: The SQLAlchemy engine.
        """
        engine = sqlalchemy.create_engine(SQLALCHEMY_PREFIX, creator=self._connect)
        return engine

    def _connect(self) -> pyodbc.Connection:
        """
        Connect to the Azure SQL database using the connection string and access token.

        Returns:
            pyodbc.Connection: The pyodbc connection object.
        """
        token = self.credentials.token.get_secret_value()
        return pyodbc.connect(
            self.settings.connection_string,
            attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token},
        )
