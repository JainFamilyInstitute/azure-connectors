from enum import Enum


class EnvPrefix(Enum):
    AZURE_SQL = "AZURE_SQL_"
    AZURE_TABLES = "AZURE_TABLES_"
    AZURE_BLOB = "AZURE_BLOB_"
    AZURE_DATALAKE = "AZURE_DATALAKE_"
    AZURE_CREDENTIAL = "AZURE_CREDENTIAL_"


class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
    AZURE_TABLES = "https://storage.azure.com/.default"
    AZURE_BLOB = "https://storage.azure.com/.default"
    AZURE_DATALAKE = "https://storage.azure.com/.default"
