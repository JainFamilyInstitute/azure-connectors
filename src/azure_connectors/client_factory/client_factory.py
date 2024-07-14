from abc import ABC, abstractmethod
from typing import Any, Protocol, Type


from azure.core.credentials import TokenCredential
from azure_connectors.config import CredentialScope
from azure_connectors.credential import AzureCredential
from azure_connectors.utils import get_parameters


class SettingsClass(Protocol):
    @property
    def client_settings(self) -> dict[str, Any]: ...


class AzureAPIClient(Protocol):
    def __init__(self, *args: Any, credential: TokenCredential, **kwargs: Any): ...

class BaseClientFactory(ABC):
    base_class: Type[AzureAPIClient]
    settings_class: Type[SettingsClass]
    scope: CredentialScope

    @property
    @abstractmethod
    def client(self) -> Type[Any]: ...

    def _get_common_client_kwargs(self, **kwargs) -> dict[str, Any]:
        settings_kwargs, base_kwargs = self._split_settings_kwargs(kwargs)
        credential_provider = AzureCredential.from_env(scope=self.scope)
        settings = self.settings_class(**settings_kwargs)
        client_settings = settings.client_settings
        client_settings.update(base_kwargs)
        credential = credential_provider.base_credential
        return {"credential": credential, **client_settings}

    def _split_settings_kwargs(
        self, kwargs: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Splits a dictionary of keyword arguments into two dictionaries:
        those used in initializing the settings class, and the remainder.

        Args:
            settings_class (Type[Any])): A class.
            kwargs (dict[str, Any]): The keyword arguments to be split.

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: A tuple containing two dictionaries. The first dictionary
                contains the keyword arguments that match initializer for the specified class, and the second dictionary
                contains the remaining keyword arguments.

        """

        settings_parameters = get_parameters(self.settings_class)
        settings_kwargs = {k: v for k, v in kwargs.items() if k in settings_parameters}
        remaining_kwargs = {
            k: v for k, v in kwargs.items() if k not in settings_parameters
        }
        return settings_kwargs, remaining_kwargs


class ClientFactory(BaseClientFactory):
    def __init__(
        self,
        base_class: Type[Any],
        settings_class: Type[SettingsClass],
        scope: CredentialScope,
    ):
        self.base_class = base_class
        self.settings_class = settings_class
        self.scope = scope

    @property
    def client(self) -> Type[Any]:
        class DynamicAzureClient(self.base_class):
            @classmethod
            def from_env(cls, *args, **kwargs):
                client_kwargs = self._get_common_client_kwargs(**kwargs)
                return self.base_class(*args, **client_kwargs)

        DynamicAzureClient.__name__ = self.base_class.__name__
        return DynamicAzureClient


class SqlManagementClientFactory(ClientFactory):
    @property
    def client(self) -> Type[Any]:
        class DynamicAzureClient(self.base_class):
            @classmethod
            def from_env(cls, *args, **kwargs):
                client_kwargs = self._get_common_client_kwargs(**kwargs)
                credential_provider = AzureCredential.from_env(scope=self.scope)
                subscription_id = credential_provider.subscription_id
                client_kwargs.update(subscription_id=subscription_id)

                return self.base_class(*args, **client_kwargs)

        DynamicAzureClient.__name__ = self.base_class.__name__
        return DynamicAzureClient
