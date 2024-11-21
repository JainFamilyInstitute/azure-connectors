from typing import Any, Protocol, runtime_checkable

from azure.core.credentials import TokenCredential

from azure_connectors.config import CredentialScope

class ModelProtocol(Protocol):
    """Interface for classes with a model_dump method."""

    def model_dump(self) -> dict[str, Any]: ...

class ClientSettingsProtocol(ModelProtocol):
    """Interface for various AzureXYZSettings classes."""

    default_credential_scope: CredentialScope


class CredentialAdapterProtocol(ModelProtocol):
    """Interface for credential adapters."""

    def __init__(self, credential): ...


@runtime_checkable
class AzureSDKClient(Protocol):
    """Interface for various Azure SDK classes."""

    def __init__(self, *args: Any, credential: TokenCredential, **kwargs: Any): ...


@runtime_checkable
class ClientWithFromEnv(Protocol):
    """Interface for classes with a from_env class method."""

    @classmethod
    def from_env(cls, *args: Any, **kwargs: Any) -> AzureSDKClient: ...


@runtime_checkable
class DynamicAzureClientWithFromEnv(AzureSDKClient, ClientWithFromEnv, Protocol):
    """Interface for dynamically created Azure SDK wrapper classes with a from_env class method."""

    ...
