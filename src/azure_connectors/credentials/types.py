from typing import Union
from azure.identity import DefaultAzureCredential, AzureCliCredential

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]

