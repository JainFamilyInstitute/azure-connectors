from enum import Enum


class EnvPrefix(Enum):
    AZURE_SQL = "AZURE_SQL_"
    AZURE_TABLES = "AZURE_TABLES_"
    AZURE_CREDENTIAL = "AZURE_CREDENTIAL_"


class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
    AZURE_TABLES = "https://storage.azure.com/.default"
