from typing import Any, Protocol, runtime_checkable

from azure.core.credentials import TokenCredential

CredParamMap = dict[str, str]


class SettingsClass(Protocol):
    """Interface for various AzureXYZSettings classes."""

    @property
    def client_settings(self) -> dict[str, Any]: ...


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
