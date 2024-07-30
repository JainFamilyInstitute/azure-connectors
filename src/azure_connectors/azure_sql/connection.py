from dataclasses import dataclass
from functools import cached_property

import pyodbc
import sqlalchemy

from azure_connectors.credential import AzureCredential

from .constants import SQL_COPT_SS_ACCESS_TOKEN, SQLALCHEMY_PREFIX
from .settings import AzureSqlSettings


@dataclass(frozen=True)
class AzureSqlConnection:
    """
    Represents a connection to an Azure SQL database.

    Attributes:
        settings (AzureSqlSettings): The settings for the Azure SQL connection.
        credential (AzureCredential): The credential for the Azure SQL connection.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine for the Azure SQL connection.
    """

    settings: AzureSqlSettings
    credential: AzureCredential

    @classmethod
    def from_env(cls) -> "AzureSqlConnection":
        """
        Create an AzureSqlConnection instance using the settings and credential from the environment.

        Returns:
            AzureSqlConnection: An instance of AzureSqlConnection.
        """
        settings = AzureSqlSettings()
        credential = AzureCredential.from_env(scope=settings.default_credential_scope)
        return cls(settings=settings, credential=credential)

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
        token = self.credential.token.get_secret_value()
        return pyodbc.connect(
            self.settings.connection_string,
            attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token},
        )
