from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Assuming these are defined in your library
from azure_connectors.config import CredentialScope
from azure_connectors.credential import AzureCredential

class AzureClientFactory:
    def __init__(self, credential_provider):
        self.credential_provider = credential_provider

    def create_client(self, client_class, *args, **kwargs):
        credential = self.credential_provider.get_credential()
        return client_class(*args, credential=credential, **kwargs)

class AzureConnectors:
    def __init__(self, credential: AzureCredential, client_factory: AzureClientFactory):
        self.credential = credential
        self.client_factory = client_factory

    @classmethod
    def from_env(cls): 
        try:
            credential = AzureCredential.from_env(scope=CredentialScope.AZURE_BLOB)
            client_factory = AzureClientFactory(credential)
            return cls(credential, client_factory)
        except Exception as e:
            raise EnvironmentError("Failed to initialize Azure credentials from environment") from e

    def __getattr__(self, client_class_name):
        client_class = globals().get(client_class_name)
        if client_class is None:
            raise AttributeError(f"{client_class_name} is not a valid Azure client class.")
        
        def client_initializer(*args, **kwargs):
            return self.client_factory.create_client(client_class, *args, **kwargs)
        
        return client_initializer

# Example usage:
if __name__ == "__main__":
    azure_connectors = AzureConnectors.from_env()
    BlobServiceClient = azure_connectors.BlobServiceClient

    # Initialize the BlobServiceClient
    blob_service_client = BlobServiceClient(account_url="https://your_account.blob.core.windows.net")

    # Test the connection by listing containers (optional)
    containers = blob_service_client.list_containers()
    for container in containers:
        print(container.name)
