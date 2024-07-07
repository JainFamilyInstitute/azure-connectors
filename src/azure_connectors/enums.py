from enum import Enum


class EnvPrefix(Enum):
    AZURE_SQL = "AZURE_SQL_"
    AZURE_TABLES = "AZURE_TABLES_"
    CREDENTIALS = "AZURE_CREDENTIALS_"

class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
    AZURE_TABLES = "https://storage.azure.com/.default"
