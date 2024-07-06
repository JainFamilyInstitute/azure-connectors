from typing import Union
from enum import Enum
from azure.identity import DefaultAzureCredential, AzureCliCredential

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]

class CredentialSource(Enum):
    CLI = "cli"
    DEFAULT = "default"

class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
