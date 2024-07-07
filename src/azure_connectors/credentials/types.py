from typing import Union

from azure.identity import AzureCliCredential, DefaultAzureCredential

BaseCredential = Union[DefaultAzureCredential, AzureCliCredential]

