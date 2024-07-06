from typing import Union
from enum import Enum
from azure.identity import DefaultAzureCredential, AzureCliCredential
from pydantic import UrlConstraints
from pydantic_core import Url
from typing import Annotated

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]
AnyHttpsUrl = Annotated[Url, UrlConstraints(allowed_schemes=["https"])]


class CredentialSource(Enum):
    CLI = "cli"
    DEFAULT = "default"


