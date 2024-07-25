from azure.identity import AzureCliCredential, DefaultAzureCredential

BaseCredential = DefaultAzureCredential | AzureCliCredential
