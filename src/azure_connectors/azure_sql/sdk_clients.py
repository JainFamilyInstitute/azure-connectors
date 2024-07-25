from azure.mgmt.sql import SqlManagementClient as AzSqlManagementClient

from azure_connectors.azure_sql.settings import SqlManagementClientSettings
from azure_connectors.client_factory import SqlManagementClientFactory
from azure_connectors.config import CredentialScope

SqlManagementClient = SqlManagementClientFactory(
    AzSqlManagementClient,
    settings_class=SqlManagementClientSettings,
    scope=CredentialScope.AZURE_SQL,
).client
