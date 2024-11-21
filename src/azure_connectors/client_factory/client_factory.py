from abc import ABC
from typing import Any, Optional, Type

from azure_connectors.config import CredentialScope
from azure_connectors.credential import AzureCredential, CredentialAdapter
from azure_connectors.utils import get_parameters, update_dict_from_object_properties

from .typing import ClientSettingsProtocol, CredentialAdapterProtocol, TokenCredential
from .utils import get_client_kwargs_from_settings

# from .typing import DynamicAzureClientWithFromEnv, AzureSDKClient


def add_fromenv_method(
    base_class: Type[Any],
    settings_class: Type[ClientSettingsProtocol],
    credential_adapter_class: Type[CredentialAdapterProtocol] = CredentialAdapter,
) -> Type[Any]:
    class DynamicAzureClient(base_class):  # type: ignore
        def __new__(cls, *args, credential: TokenCredential, **kwargs):
            """
            Direct initialization of the return class should pass through to the base Azure SDK Client class.
            """
            return base_class(*args, credential=credential, **kwargs)  # type: ignore

        @classmethod
        def from_env(cls, *args, **kwargs):  # -> AzureSDKClient:
            """
            The `from_env` method should return an instance of the base Azure SDK Client class with settings
            generated from coherently combining any passed arguments with those read from the environment.
            """
            client_kwargs = get_client_kwargs_from_settings(kwargs, settings_class)
            credential_provider = AzureCredential.from_env(
                scope=settings_class.default_credential_scope
            )
            credential_kwargs = credential_adapter_class(credential=credential_provider)
            client_kwargs = update_dict_from_object_properties(
                client_kwargs, credential_provider, cred_param_map
            )
            return base_class(*args, **client_kwargs)

    return DynamicAzureClient


class BaseClientFactory(ABC):
    """
    Base class for client factories.

    Client factories are used to create client instances for Azure services. They supplement Azure SDK Client
    classes with a `from_env` class method that can be used to create a client instance with settings given by
    environment variables or .env files.

    The base class provides common logic for this; subclasses should specify the cred_param_map attribute to
    map properties of an AzureCredential object to parameter names expected by the Azure SDK Client class.

    Attributes:
        base_class (Type[AzureAPIClient]): The base class for the client.
        settings_class (Type[SettingsClass]): The class for the settings.
        scope (CredentialScope): The credential scope.
        cred_param_map (CredParamMap): A mapping of credential properties to client parameter names.


    """

    base_class: Type[Any]
    settings_class: Type[ClientSettingsProtocol]
    scope: CredentialScope
    cred_param_map: ParamMap

    def __init__(
        self,
        base_class: Type[Any],
        settings_class: Type[ClientSettingsProtocol],
        scope: CredentialScope,
    ):
        self.base_class = base_class
        self.settings_class = settings_class
        self.scope = scope

    @property
    def client(self):  # -> Type[DynamicAzureClientWithFromEnv]:  # type: ignore
        """
        The main factory function for creating a client class by providing an Azure SDK Client class
        with a `from_env` class method. The client classes are perfect shadows: any (attempted) initialization
        of them, either directly or through the `from_env` method, actually initializes and returns an instance
        of the underlying Azure SDK Client class.

        Returns:
            Type[DynamicAzureClientWithFromEnv]: A dynamically created client class with a `from_env` class method.

        """
        base_class = self.base_class

        class DynamicAzureClient(base_class):  # type: ignore
            def __new__(cls, *args, credential: TokenCredential, **kwargs):
                """
                Direct initialization of the return class should pass through to the base Azure SDK Client class.
                """
                return base_class(*args, credential=credential, **kwargs)  # type: ignore

            @classmethod
            def from_env(cls, *args, **kwargs):  # -> AzureSDKClient:
                """
                The `from_env` method should return an instance of the base Azure SDK Client class with settings
                generated from coherently combining any passed arguments with those read from the environment.
                """
                client_kwargs = self._get_client_kwargs(kwargs)
                client_kwargs = self._update_client_kwargs_with_credential(
                    client_kwargs
                )
                return base_class(*args, **client_kwargs)

        return DynamicAzureClient

    def _get_client_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        """
        Logic for sensible handling of passed kwargs for from_env:
            - any keyword arguments that match Settings class properties are passed to the settings class.
            - Settings class is initialized with those properties and used to generate client settings.
            - Remaining keyword arguments are treated as client settings arguments; if they match any keywords from
              settings generated by the Settings class, they override the generated settings.

        Args:
            kwargs: Passed keyword arguments for from_env.

        Returns:
            dict[str, Any]: The keyword arguments to pass on to the client class constructor.
        """
        settings_kwargs, base_kwargs = self._split_settings_kwargs(kwargs)
        settings = self.settings_class(**settings_kwargs)
        client_settings = settings.model_dump()
        client_settings.update(base_kwargs)

        return client_settings

    def _split_settings_kwargs(
        self, kwargs: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Splits a dictionary of keyword arguments into two dictionaries:
        those used in initializing the settings class, and the remainder.

        Args:
            kwargs (dict[str, Any]): The keyword arguments to be split.

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: A tuple containing two dictionaries. The first dictionary
                contains the keyword arguments that match the initializer for the settings class, and the second
                contains the remaining keyword arguments.

        """

        settings_parameters = get_parameters(self.settings_class)
        settings_kwargs = {k: v for k, v in kwargs.items() if k in settings_parameters}
        remaining_kwargs = {
            k: v for k, v in kwargs.items() if k not in settings_parameters
        }
        return settings_kwargs, remaining_kwargs

    def _update_client_kwargs_with_credential(
        self, client_kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Updates the client_kwargs dictionary with credentials obtained from the AzureCredential provider.

        Args:
            client_kwargs (dict[str, Any]): The client_kwargs dictionary to be updated.

        Returns:
            dict[str, Any]: The updated client_kwargs dictionary.
        """
        credential_provider = AzureCredential.from_env(scope=self.scope)
        for credential_property, param_name in self.cred_param_map.items():
            if param_name not in client_kwargs.keys():
                client_kwargs.update(
                    {param_name: getattr(credential_provider, credential_property)}
                )

        return client_kwargs


class ClientFactory(BaseClientFactory):
    cred_param_map: ParamMap = {"base_credential": "credential"}


class SqlManagementClientFactory(BaseClientFactory):
    cred_param_map: ParamMap = {
        "base_credential": "credential",
        "subscription_id": "subscription_id",
    }
