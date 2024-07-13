from typing import Any, Type

from azure_connectors.client_factory.utils import split_kwargs
from azure_connectors.config import CredentialScope
from azure_connectors.credential import AzureCredential
from azure_connectors.credential.types import BaseCredential

from typing import Protocol


class SettingsClass(Protocol):

    @property
    def client_settings(self) -> dict[str, Any]:
        ...




def create_azure_client_class(
    base_class: Type[Any],
    settings_class: Type[SettingsClass],
    scope: CredentialScope,
):
    class DynamicAzureClient(base_class):
        @classmethod
        def from_env(cls, *args, **kwargs):
            # find settable parameters for settings class

            settings_kwargs, base_kwargs = split_kwargs(settings_class, kwargs)
            credential_provider = AzureCredential.from_env(scope=scope)

            # any kwargs passed that apply to settings go to settings

            settings = settings_class(**settings_kwargs)

            client_settings = settings.client_settings

            client_settings.update(base_kwargs)
            credential = credential_provider.get_credential()

            return base_class(*args, credential=credential, **client_settings)

    DynamicAzureClient.__name__ = base_class.__name__
    return DynamicAzureClient
