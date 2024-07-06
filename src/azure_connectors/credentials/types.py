from typing import Union
from enum import Enum
from azure.identity import DefaultAzureCredential, AzureCliCredential
from pydantic import UrlConstraints
from pydantic_core import Url
from typing import Annotated

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]

class CredentialSource(Enum):
    CLI = "cli"
    DEFAULT = "default"

class CredentialScope(Enum):
    AZURE_SQL = "https://database.windows.net/.default"
