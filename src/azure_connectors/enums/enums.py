from enum import Enum

class CredentialSource(Enum):
    CLI = "cli"
    DEFAULT = "default"

class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
